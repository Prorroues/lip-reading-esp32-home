"""AI 分析引擎 — 本地统计 + 异常检测 + (可选) 大模型 API 深度分析"""

import json
import os
import logging
import traceback
from datetime import datetime, timedelta
from collections import defaultdict

from models import (
    get_all_devices,
    get_telemetry_history,
    save_ai_report,
    get_ai_report,
    get_ai_reports,
)

logger = logging.getLogger("ai")

AI_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "ai_config.json")

# ── 阈值 ──
TEMP_HIGH  = 35.0
TEMP_LOW   = 10.0
HUM_HIGH   = 95.0
CO2_HIGH   = 2000
CO2_WARN   = 1500
LIGHT_LOW  = 500   # 光照过低（暗）


def _load_config() -> dict:
    try:
        with open(AI_CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {"enabled": False, "api_base": "", "api_key": "", "model": ""}


# ═══════════════ 本地统计 ═══════════════

def generate_summary_report() -> dict:
    """生成今日统计摘要 — 纯本地计算，不调 AI。"""
    today = datetime.now().strftime("%Y-%m-%d")
    summary = {
        "date": today,
        "generated": datetime.now().isoformat(timespec="seconds"),
        "devices": [],
        "stats": {},
        "alerts": [],
    }

    # 从 CSV 统计（始终从 CSV 读取，避免 async-in-sync 问题）
    import csv
    import os as _os
    data_dir = _os.path.join(_os.path.dirname(__file__), "..", "data")
    telemetry_csv = _os.path.join(data_dir, "telemetry.csv")

    all_temp, all_hum = [], []
    device_data: dict[str, list[dict]] = defaultdict(list)
    if _os.path.exists(telemetry_csv):
        try:
            with open(telemetry_csv, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ts = row.get("timestamp", "")
                    if ts.startswith(today):
                        did = row.get("device_id", "?")
                        try:
                            t = float(row["temperature"]) if row.get("temperature") else None
                            h = float(row["humidity"]) if row.get("humidity") else None
                        except (ValueError, TypeError):
                            continue
                        if t is not None and h is not None:
                            device_data[did].append({"t": t, "h": h, "ts": ts})
                            all_temp.append(t)
                            all_hum.append(h)
        except Exception as e:
            logger.error(f"读取遥测 CSV 失败: {e}")

    # 每个设备统计
    for did, records in device_data.items():
        temps = [r["t"] for r in records]
        hums  = [r["h"] for r in records]
        if temps:
            summary["devices"].append({
                "device_id": did,
                "records": len(temps),
                "avg_temp": round(sum(temps) / len(temps), 1),
                "max_temp": round(max(temps), 1),
                "min_temp": round(min(temps), 1),
                "avg_hum": round(sum(hums) / len(hums), 1),
                "max_hum": round(max(hums), 1),
                "min_hum": round(min(hums), 1),
            })

    # 全局统计
    if all_temp:
        summary["stats"] = {
            "avg_temp": round(sum(all_temp) / len(all_temp), 1),
            "max_temp": round(max(all_temp), 1),
            "min_temp": round(min(all_temp), 1),
            "avg_hum": round(sum(all_hum) / len(all_hum), 1),
            "max_hum": round(max(all_hum), 1),
            "min_hum": round(min(all_hum), 1),
            "total_records": len(all_temp),
        }

    # 异常检测
    anomalies = detect_anomalies(device_data)
    summary["alerts"] = anomalies
    summary["anomaly_count"] = len(anomalies)

    return summary


# ═══════════════ 异常检测 ═══════════════

def detect_anomalies(device_data: dict[str, list[dict]] = None) -> list[dict]:
    """基于规则引擎检测异常。返回异常事件列表。"""
    anomalies = []

    if device_data is None:
        # 无数据时不报异常
        return anomalies

    today = datetime.now().strftime("%Y-%m-%d")

    for did, records in device_data.items():
        if not records:
            continue

        # 温度越界检测
        high_temps = [r for r in records if r["t"] >= TEMP_HIGH]
        low_temps  = [r for r in records if r["t"] <= TEMP_LOW]
        if high_temps:
            anomalies.append({
                "device_id": did,
                "type": "temp_high",
                "severity": "warning",
                "message": f"温度过高: 最高 {max(r['t'] for r in high_temps)}°C (阈值 {TEMP_HIGH}°C)",
                "count": len(high_temps),
                "first_at": high_temps[0]["ts"],
            })
        if low_temps:
            anomalies.append({
                "device_id": did,
                "type": "temp_low",
                "severity": "info",
                "message": f"温度过低: 最低 {min(r['t'] for r in low_temps)}°C (阈值 {TEMP_LOW}°C)",
                "count": len(low_temps),
                "first_at": low_temps[0]["ts"],
            })

        # 湿度越界
        high_hums = [r for r in records if r["h"] >= HUM_HIGH]
        if high_hums:
            anomalies.append({
                "device_id": did,
                "type": "hum_high",
                "severity": "warning",
                "message": f"湿度过高: 最高 {max(r['h'] for r in high_hums)}% (阈值 {HUM_HIGH}%)",
                "count": len(high_hums),
                "first_at": high_hums[0]["ts"],
            })

    # 从 commands.csv 检测异常开门
    import csv
    import os as _os
    data_dir = _os.path.join(_os.path.dirname(__file__), "..", "data")
    commands_csv = _os.path.join(data_dir, "commands.csv")

    # 从 access_log 表中检测（如果有的话）

    return anomalies


# ═══════════════ AI API 分析 ═══════════════

async def ai_analyze(force: bool = False) -> dict:
    """触发 AI 深度分析。先从 DB 读 API Key，没有则用文件配置。
    AI 返回分析 + 建议列表。
    """
    today = datetime.now().strftime("%Y-%m-%d")

    # 缓存检查
    if not force:
        cached = await get_ai_report(today)
        if cached:
            return {
                "date": today,
                "cached": True,
                "content": cached["content"],
                "anomalies": json.loads(cached.get("anomalies", "[]")),
            }

    # 获取 API Key：优先数据库配置，其次文件配置
    api_key = None
    api_base = None
    model = None
    try:
        from models import get_config as _get_config
        db_key = await _get_config("ai_api_key")
        if db_key:
            api_key = db_key
            db_base = await _get_config("ai_api_base")
            api_base = db_base or "https://api.deepseek.com/v1"
            db_model = await _get_config("ai_api_model")
            model = db_model or "deepseek-chat"
    except Exception:
        pass

    if not api_key:
        file_cfg = _load_config()
        if file_cfg.get("enabled") and file_cfg.get("api_key"):
            api_key = file_cfg["api_key"]
            api_base = file_cfg.get("api_base", "https://api.deepseek.com/v1")
            model = file_cfg.get("model", "deepseek-chat")
        else:
            summary = generate_summary_report()
            return {
                "date": today,
                "ai_enabled": False,
                "summary": summary,
                "anomalies": summary.get("alerts", []),
                "message": "AI 分析未启用。请在下方填入 DeepSeek API Key 后重试。",
            }

    summary = generate_summary_report()
    cfg = {"api_base": api_base or "https://api.deepseek.com/v1", "api_key": api_key, "model": model or "deepseek-chat"}

    prompt = _build_analysis_prompt(summary)
    ai_response = await _call_ai_api(cfg, prompt)

    if ai_response:
        # 解析建议部分
        recommendations = _extract_recommendations(ai_response)
        await save_ai_report(today, "daily", ai_response, json.dumps(summary.get("alerts", []), ensure_ascii=False))
        return {
            "date": today, "ai_enabled": True,
            "content": ai_response,
            "recommendations": recommendations,
            "anomalies": summary.get("alerts", []),
        }
    else:
        return {
            "date": today, "ai_enabled": True,
            "error": "AI API 调用失败，请检查网络和 API Key",
            "summary": summary,
            "anomalies": summary.get("alerts", []),
        }


def _extract_recommendations(text: str) -> list[str]:
    """从 AI 返回的文本中提取建议列表。"""
    lines = text.split("\n")
    recs = []
    in_rec = False
    for line in lines:
        line = line.strip()
        if "建议" in line and (line.startswith("#") or line.startswith("##") or len(line) < 8):
            in_rec = True
            continue
        if in_rec and line and (line[0].isdigit() or line.startswith("-")):
            clean = line.lstrip("0123456789.-) ").strip()
            if clean and len(clean) > 3:
                recs.append(clean)
    return recs if recs else []


def _build_analysis_prompt(summary: dict) -> str:
    """构建发给大模型的提示词。"""
    stats = summary.get("stats", {})
    devices = summary.get("devices", [])
    alerts = summary.get("alerts", [])

    prompt = f"""你是一个智能家居数据分析师。请根据以下今日环境数据，用中文给出简要分析（200字以内）：

日期: {summary.get('date')}

全局统计:
- 平均温度: {stats.get('avg_temp', 'N/A')}°C
- 最高温度: {stats.get('max_temp', 'N/A')}°C
- 最低温度: {stats.get('min_temp', 'N/A')}°C
- 平均湿度: {stats.get('avg_hum', 'N/A')}%
- 总记录数: {stats.get('total_records', 0)}

异常事件 ({len(alerts)} 条):
"""
    for a in alerts[:10]:
        prompt += f"- [{a.get('severity','')}] {a.get('message','')}\n"

    prompt += """
请给出:
1. 今日环境概况（一句话）
2. 温湿度是否在舒适范围
3. 节能建议（如有）
4. 明日预警（如需）

## 建议
然后用编号列表列出 3-5 条具体可操作的建议。

用简洁、口语化的中文回复。"""
    return prompt


async def _call_ai_api(config: dict, prompt: str) -> str | None:
    """调用 OpenAI 兼容 API。"""
    import aiohttp

    url = f"{config['api_base']}/chat/completions"
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
    }
    body = {
        "model": config.get("model", "gpt-4o-mini"),
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.7,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers, timeout=30) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    error = await resp.text()
                    logger.error(f"AI API 返回 {resp.status}: {error[:200]}")
                    return None
    except Exception as e:
        logger.error(f"AI API 调用异常: {e}\n{traceback.format_exc()}")
        return None


# ═══════════════ 舒适度评分 ═══════════════

def comfort_score(temperature: float, humidity: float, co2_ppm: int = None) -> dict:
    """计算舒适度评分 0-100。
    - 温度 18-26°C 最舒适
    - 湿度 40-70% 最舒适
    - CO2 < 1000 良好
    """
    score = 100

    # 温度扣分
    if temperature < 15:
        score -= (15 - temperature) * 5
    elif temperature > 30:
        score -= (temperature - 30) * 6
    elif temperature < 18:
        score -= (18 - temperature) * 3
    elif temperature > 26:
        score -= (temperature - 26) * 3

    # 湿度扣分
    if humidity < 30:
        score -= (30 - humidity) * 1.5
    elif humidity > 80:
        score -= (humidity - 80) * 2
    elif humidity < 40:
        score -= (40 - humidity) * 0.5
    elif humidity > 70:
        score -= (humidity - 70) * 0.5

    # CO2 扣分
    if co2_ppm:
        if co2_ppm > 2000:
            score -= 30
        elif co2_ppm > 1500:
            score -= 20
        elif co2_ppm > 1000:
            score -= 10

    score = max(0, min(100, round(score)))
    level = "优秀" if score >= 85 else "良好" if score >= 70 else "一般" if score >= 50 else "较差"

    return {"score": score, "level": level}
