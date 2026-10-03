"""REST API routes for ESP32 IoT server."""

import json
import os
import time
import logging
import traceback
from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel

from models import (
    get_all_devices,
    get_device,
    get_telemetry_history,
    get_device_messages,
    save_message,
    get_config,
    set_config,
    get_all_config,
    get_ai_report,
    get_ai_reports,
)
from mqtt_client import publish_command, publish_message

logger = logging.getLogger("api")
router = APIRouter(prefix="/api")


# ── Pydantic schemas ──────────────────────────

class CommandBody(BaseModel):
    cmd: int  # 1-21


class MessageBody(BaseModel):
    from_device: str
    text: str


# ── Helpers ────────────────────────────────────

_request_times: dict[str, float] = {}

def _log_request(request: Request, extra: str = ""):
    """Log incoming HTTP request with client IP + timing."""
    client = request.client.host if request.client else "?"
    msg = f"{request.method} {request.url.path}"
    rid = f"{client}:{request.url.path}"
    _request_times[rid] = time.time()
    if extra:
        msg += f" | {extra}"
    logger.info(f"[{client}] {msg}")

def _log_response(request: Request, status: int):
    """Log response with elapsed time."""
    client = request.client.host if request.client else "?"
    rid = f"{client}:{request.url.path}"
    elapsed = time.time() - _request_times.pop(rid, time.time())
    level = logging.WARNING if status >= 400 else logging.DEBUG
    logger.log(level, f"[{client}] → {status} ({elapsed*1000:.0f}ms)")


# ── Devices ────────────────────────────────────

@router.get("/devices")
async def list_devices(request: Request):
    """Return all known ESP32 devices with online status and latest telemetry."""
    _log_request(request)
    try:
        devices = await get_all_devices()
        logger.debug(f"返回 {len(devices)} 个设备")
        return {"devices": devices, "count": len(devices)}
    except Exception as e:
        logger.error(f"设备列表接口异常: {e}\n{traceback.format_exc()}")
        raise HTTPException(500, f"服务器内部错误: {e}")


@router.get("/devices/{device_id}")
async def device_detail(device_id: str, request: Request):
    """Return a single device's detail."""
    _log_request(request, f"device={device_id}")
    try:
        dev = await get_device(device_id)
        if dev is None:
            logger.warning(f"设备不存在: {device_id}")
            raise HTTPException(404, f"设备 '{device_id}' 不存在")
        return dev
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"设备详情接口异常 [{device_id}]: {e}\n{traceback.format_exc()}")
        raise HTTPException(500, f"服务器内部错误: {e}")


# ── Telemetry history ──────────────────────────

@router.get("/devices/{device_id}/history")
async def device_history(device_id: str, hours: int = Query(24, ge=1, le=720), request: Request = None):
    """Return telemetry history for a device (default 24h, max 30 days)."""
    _log_request(request, f"device={device_id} hours={hours}")
    try:
        dev = await get_device(device_id)
        if dev is None:
            raise HTTPException(404, f"设备 '{device_id}' 不存在")
        rows = await get_telemetry_history(device_id, hours)
        logger.debug(f"返回 [{device_id}] {len(rows)} 条遥测记录 ({hours}h)")
        return {"device_id": device_id, "hours": hours, "records": rows, "count": len(rows)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"遥测历史接口异常 [{device_id}]: {e}\n{traceback.format_exc()}")
        raise HTTPException(500, f"服务器内部错误: {e}")


# ── Commands ───────────────────────────────────

class RgbBody(BaseModel):
    r: int = 0
    g: int = 0
    b: int = 0

@router.post("/devices/{device_id}/rgb")
async def set_rgb(device_id: str, body: RgbBody, request: Request):
    """Set custom RGB color via MQTT."""
    _log_request(request, f"device={device_id} r={body.r} g={body.g} b={body.b}")
    try:
        payload = json.dumps({"cmd": 21, "r": body.r, "g": body.g, "b": body.b})
        from mqtt_client import _client
        if _client:
            _client.publish(f"esp32/{device_id}/command", payload, qos=0)
        return {"device_id": device_id, "r": body.r, "g": body.g, "b": body.b, "status": "sent"}
    except Exception as e:
        logger.error(f"RGB设置失败: {e}")
        raise HTTPException(500, f"RGB设置失败: {e}")

@router.post("/devices/{device_id}/command")
async def send_command(device_id: str, body: CommandBody, request: Request):
    """Send a control command (1-19) to an ESP32 via MQTT."""
    _log_request(request, f"device={device_id} cmd={body.cmd}")
    try:
        dev = await get_device(device_id)
        if dev is None:
            raise HTTPException(404, f"设备 '{device_id}' 不存在")
        if not 1 <= body.cmd <= 21:
            logger.warning(f"非法指令: [{device_id}] cmd={body.cmd}")
            raise HTTPException(400, "指令必须在 1-19 之间")
        publish_command(device_id, body.cmd)
        return {"device_id": device_id, "cmd": body.cmd, "status": "sent"}
    except HTTPException:
        raise
    except RuntimeError as e:
        logger.error(f"MQTT 发布异常 [{device_id}]: {e}")
        raise HTTPException(503, f"MQTT 服务不可用: {e}")
    except Exception as e:
        logger.error(f"指令接口异常 [{device_id}]: {e}\n{traceback.format_exc()}")
        raise HTTPException(500, f"服务器内部错误: {e}")


# ── Device-to-device messages ──────────────────

@router.post("/devices/{device_id}/message")
async def send_message(device_id: str, body: MessageBody, request: Request):
    """Send a text message from one device to another."""
    _log_request(request, f"to={device_id} from={body.from_device}")
    try:
        to_dev = await get_device(device_id)
        if to_dev is None:
            raise HTTPException(404, f"目标设备 '{device_id}' 不存在")
        publish_message(device_id, body.from_device, body.text)
        await save_message(body.from_device, device_id, body.text)
        return {
            "from": body.from_device,
            "to": device_id,
            "text": body.text,
            "status": "sent",
        }
    except HTTPException:
        raise
    except RuntimeError as e:
        logger.error(f"MQTT 消息发布异常 [{device_id}]: {e}")
        raise HTTPException(503, f"MQTT 服务不可用: {e}")
    except Exception as e:
        logger.error(f"消息接口异常 [{device_id}]: {e}\n{traceback.format_exc()}")
        raise HTTPException(500, f"服务器内部错误: {e}")


@router.get("/devices/{device_id}/messages")
async def list_messages(device_id: str, limit: int = Query(50, le=200), request: Request = None):
    """Return messages sent to/from a device."""
    _log_request(request, f"device={device_id} limit={limit}")
    try:
        rows = await get_device_messages(device_id, limit)
        return {"device_id": device_id, "messages": rows, "count": len(rows)}
    except Exception as e:
        logger.error(f"消息列表接口异常 [{device_id}]: {e}\n{traceback.format_exc()}")
        raise HTTPException(500, f"服务器内部错误: {e}")


# ── Config ──────────────────────────────────────

@router.get("/config")
async def list_config():
    """获取所有自动化开关配置。"""
    config = await get_all_config()
    return {"config": config}


@router.post("/config")
async def update_config(request: Request):
    """更新自动化开关配置。推送到 ESP32。"""
    body = await request.json()
    for key, value in body.items():
        await set_config(key, str(value))
    # 推送配置到所有在线设备
    try:
        payload = json.dumps(body)
        from mqtt_client import _client
        if _client:
            for did in ["esp32_lipreading_iot"]:
                _client.publish(f"esp32/{did}/config", payload, qos=0)
    except Exception:
        pass
    return {"status": "ok", "updated": list(body.keys())}


# ── Scheduled Tasks ────────────────────────────

@router.get("/schedule")
async def list_schedules():
    """列出所有定时任务。"""
    raw = await get_config("schedules")
    tasks = json.loads(raw) if raw else []
    return {"schedules": tasks}


@router.post("/schedule")
async def add_schedule(request: Request):
    """添加定时任务。{"time":"23:00","cmd":7,"label":"关RGB"}"""
    body = await request.json()
    raw = await get_config("schedules")
    tasks = json.loads(raw) if raw else []
    tasks.append(body)
    await set_config("schedules", json.dumps(tasks, ensure_ascii=False))
    return {"schedules": tasks}


@router.delete("/schedule/{index}")
async def delete_schedule(index: int):
    """删除指定定时任务。"""
    raw = await get_config("schedules")
    tasks = json.loads(raw) if raw else []
    if 0 <= index < len(tasks):
        tasks.pop(index)
    await set_config("schedules", json.dumps(tasks, ensure_ascii=False))
    return {"schedules": tasks}


async def check_scheduled_tasks():
    """每分钟检查定时任务（由 main.py scheduler 调用）。"""
    raw = await get_config("schedules")
    if not raw:
        return
    try:
        tasks = json.loads(raw)
    except Exception:
        return
    now = __import__("datetime").datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")

    # 检查节假日
    holidays_raw = await get_config("holidays")
    is_holiday = False
    if holidays_raw:
        try:
            holidays = json.loads(holidays_raw)
            for h in holidays:
                if h.get("start", "") <= today_str <= h.get("end", ""):
                    is_holiday = True
                    break
        except Exception:
            logger.debug(f"节假日配置解析失败: {holidays_raw}")

    for task in tasks:
        task_time = task.get("time", "")
        if task_time == current_time:
            cmd = task.get("cmd")
            label = task.get("label", "")
            device_id = task.get("device_id", "esp32_lipreading_iot")
            if is_holiday and task.get("skip_holiday", False):
                logger.info(f"定时跳过(节假日): {label}")
                continue
            if cmd is not None:
                publish_command(device_id, int(cmd))
                logger.info(f"定时执行: {label} ({cmd})")


# ── Holidays ────────────────────────────────────

@router.get("/config/holidays")
async def get_holidays():
    raw = await get_config("holidays")
    return {"holidays": json.loads(raw) if raw else []}


@router.post("/config/holidays")
async def set_holidays(request: Request):
    body = await request.json()
    await set_config("holidays", json.dumps(body, ensure_ascii=False))
    return {"holidays": body}


# ── Scene Macros ────────────────────────────────

@router.post("/scene/home")
async def scene_home(request: Request):
    """一键回家：床头灯+柜子灯+RGB暖色。"""
    _log_request(request, "一键回家")
    try:
        publish_command("esp32_lipreading_iot", 14)
        publish_command("esp32_lipreading_iot", 8)
        publish_command("esp32_lipreading_iot", 6)
    except RuntimeError as e:
        logger.warning(f"回家场景部分失败 (MQTT): {e}")
    return {"scene": "home", "status": "executed"}


@router.post("/scene/away")
async def scene_away(request: Request):
    """一键离家：关所有灯+关风扇+关RGB。"""
    _log_request(request, "一键离家")
    try:
        for cmd in [9, 11, 13, 15, 17, 19]:
            publish_command("esp32_lipreading_iot", cmd)
        publish_command("esp32_lipreading_iot", 2)
        publish_command("esp32_lipreading_iot", 7)
    except RuntimeError as e:
        logger.warning(f"离家场景部分失败 (MQTT): {e}")
    return {"scene": "away", "status": "executed"}


# ── Today vs Yesterday ─────────────────────────

@router.get("/ai/compare")
async def daily_compare():
    """今日 vs 昨日对比。"""
    from datetime import datetime, timedelta
    import csv
    import os as _os

    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    data_dir = _os.path.join(_os.path.dirname(__file__), "..", "data")
    telemetry_csv = _os.path.join(data_dir, "telemetry.csv")

    today_temps, today_hums = [], []
    yest_temps, yest_hums = [], []

    if _os.path.exists(telemetry_csv):
        with open(telemetry_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts = row.get("timestamp", "")
                try:
                    t = float(row["temperature"])
                    h = float(row["humidity"])
                except (ValueError, TypeError):
                    continue
                if ts.startswith(today):
                    today_temps.append(t); today_hums.append(h)
                elif ts.startswith(yesterday):
                    yest_temps.append(t); yest_hums.append(h)

    def avg(lst): return round(sum(lst)/len(lst), 1) if lst else None

    return {
        "today": {"avg_temp": avg(today_temps), "avg_hum": avg(today_hums), "records": len(today_temps)},
        "yesterday": {"avg_temp": avg(yest_temps), "avg_hum": avg(yest_hums), "records": len(yest_temps)},
        "diff": {
            "temp": round(avg(today_temps) - avg(yest_temps), 1) if today_temps and yest_temps else None,
            "hum": round(avg(today_hums) - avg(yest_hums), 1) if today_hums and yest_hums else None,
        }
    }


# ── Energy ──────────────────────────────────────

from mqtt_client import get_energy_stats
from ai_analyzer import comfort_score

@router.get("/energy")
async def energy_stats():
    """能耗统计。"""
    return get_energy_stats()


@router.get("/comfort")
async def comfort_index():
    """舒适度评分。从最新遥测数据计算。"""
    dev = await get_device("esp32_lipreading_iot")
    t = dev.get("temperature") if dev else None
    h = dev.get("humidity") if dev else None
    if t is None or h is None:
        return {"score": None, "level": "无数据"}
    return comfort_score(t, h)


# ── AI Analysis ─────────────────────────────────

from ai_analyzer import generate_summary_report, ai_analyze, detect_anomalies

@router.get("/ai/summary")
async def ai_summary():
    """今日统计摘要。"""
    summary = generate_summary_report()
    return summary


@router.post("/ai/analyze")
async def ai_analyze_endpoint(request: Request = None):
    """触发 AI 深度分析。"""
    _log_request(request, "AI 分析")
    try:
        result = await ai_analyze(force=True)
        return result
    except Exception as e:
        logger.error(f"AI 分析失败: {e}\n{traceback.format_exc()}")
        raise HTTPException(500, f"AI 分析失败: {e}")


@router.get("/ai/anomalies")
async def ai_anomalies():
    """获取异常事件列表。"""
    summary = generate_summary_report()
    return {"anomalies": summary.get("alerts", [])}


@router.get("/ai/reports")
async def ai_reports_list():
    """历史 AI 报告列表。"""
    reports = await get_ai_reports()
    return {"reports": reports, "count": len(reports)}


@router.get("/ai/report/{date}")
async def ai_report_detail(date: str):
    """查看某天的 AI 报告。"""
    report = await get_ai_report(date)
    if report is None:
        raise HTTPException(404, f"无 {date} 的报告")
    return report


# ── Data files ──────────────────────────────────

from fastapi.responses import FileResponse
from exporter import list_data_files, generate_summary, DATA_DIR

@router.get("/data/files")
async def data_files():
    """List all data files available for download."""
    files = list_data_files()
    return {"files": files, "count": len(files)}


@router.get("/data/download/{filename}")
async def download_file(filename: str):
    """Download a data file."""
    allowed = ["telemetry.csv", "telemetry_hourly.csv", "commands.csv",
               "messages.csv", "devices.json", "summary.json",
               "sensor_light.csv", "sensor_distance.csv", "sensor_co2.csv",
               "sensor_rfid.csv", "sensor_presence.csv"]
    if filename not in allowed:
        raise HTTPException(400, f"文件名不允许: {filename}")
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(404, f"文件不存在: {filename}")
    return FileResponse(path, filename=filename,
                        media_type="application/octet-stream")


@router.post("/data/export")
async def export_data(request: Request):
    """Manually trigger full data export + daily summary."""
    _log_request(request, "manual export")
    try:
        summary = generate_summary()
        files = list_data_files()
        return {
            "status": "exported",
            "summary": summary,
            "files": files,
        }
    except Exception as e:
        logger.error(f"数据导出失败: {e}\n{traceback.format_exc()}")
        raise HTTPException(500, f"导出失败: {e}")


# ── Voice Assistant ─────────────────────────────

@router.post("/voice/control")
async def voice_control(request: Request):
    """语音控制接口：接收音频 → STT → AI解析 → 执行指令 → TTS回复"""
    from voice_assistant import stt_transcribe, ai_parse_command, tts_synthesize, execute_actions
    import base64 as _b64

    body = await request.json()
    audio_b64 = body.get("audio", "")

    if not audio_b64:
        return {"error": "no audio", "userText": "", "reply": "未收到音频", "audioBase64": None}

    try:
        audio_bytes = _b64.b64decode(audio_b64)
    except Exception:
        return {"error": "invalid audio", "userText": "", "reply": "音频格式错误", "audioBase64": None}

    # ① STT
    user_text = await stt_transcribe(audio_bytes)
    if not user_text:
        return {"userText": "", "reply": "没听清，请再说一遍", "audioBase64": None, "actions": [], "results": []}

    # ② AI 解析
    parsed = await ai_parse_command(user_text)
    actions = parsed.get("actions", [])
    reply = parsed.get("reply", "好的")

    # ③ 执行指令
    results = []
    if actions:
        results = await execute_actions(actions)

    # ④ TTS
    audio_base64 = await tts_synthesize(reply)

    return {
        "userText": user_text,
        "reply": reply,
        "audioBase64": audio_base64,
        "audioFormat": "mp3",
        "actions": actions,
        "results": results,
    }


@router.post("/voice/text")
async def voice_text_command(request: Request):
    """文字控制接口：词表匹配优先，未命中再走 AI 解析。"""
    from voice_assistant import ai_parse_command, tts_synthesize, execute_actions
    from mqtt_client import dispatch_lip_text

    body = await request.json()
    text = body.get("text", "").strip()

    if not text:
        return {"error": "no text", "reply": "请输入指令", "audioBase64": None}

    matched = dispatch_lip_text(text)
    if matched.get("matched"):
        reply = matched.get("reply", "好的")
        audio_base64 = await tts_synthesize(reply)
        results = [{"action": desc, "status": "sent"} for desc in matched.get("descs", [])]
        return {
            "userText": text,
            "reply": reply,
            "audioBase64": audio_base64,
            "audioFormat": "mp3",
            "matched": True,
            "commands": matched.get("commands", []),
            "actions": [],
            "results": results,
        }

    parsed = await ai_parse_command(text)
    actions = parsed.get("actions", [])
    reply = parsed.get("reply", "好的")

    results = []
    if actions:
        results = await execute_actions(actions)

    audio_base64 = await tts_synthesize(reply)

    return {
        "userText": text,
        "reply": reply,
        "audioBase64": audio_base64,
        "audioFormat": "mp3",
        "matched": False,
        "actions": actions,
        "results": results,
    }


@router.post("/lip/command")
async def lip_text_command(request: Request):
    """唇语纯文本控制：只做词表匹配，命中才发 MQTT 数字指令。"""
    from mqtt_client import dispatch_lip_text

    body = await request.json()
    text = body.get("text", "").strip()
    if not text:
        return {"error": "no text", "matched": False, "reply": "没有识别到文字"}

    result = dispatch_lip_text(text)
    _log_request(request, f"lip text={text[:40]}")
    return result


# ── Health ─────────────────────────────────────

@router.get("/health")
async def health():
    return {"status": "ok"}
