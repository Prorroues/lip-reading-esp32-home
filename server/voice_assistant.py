"""
语音助手模块 — STT + AI 指令解析 + TTS
- STT: faster-whisper 本地服务 (localhost:5003)
- AI: DeepSeek API 解析自然语言 → JSON 指令
- TTS: MiniMax API 云端合成 (<500ms)
"""

import json
import logging
import aiohttp
from models import get_config

logger = logging.getLogger("voice")

# ═══════════ 系统提示词 ═══════════
SYSTEM_PROMPT = """你是一个 IoT 智能家居控制助手。用户会用自然语言描述需求，你需要解析成 JSON 指令。

可用控制指令：
- 风扇: 启动=cmd1, 停止=cmd2
- RGB氛围灯: 暖色=cmd6, 关闭=cmd7, 自动模式=cmd20
- 房间灯光 (偶数=开, 奇数=关):
  柜子灯=8/9, 床后灯=10/11, 床下前灯=12/13, 床头灯=14/15, 上左灯=16/17, 厕所灯=18/19
- 场景: home=一键回家, away=一键离家

主控板设备ID: esp32_lipreading_iot

返回格式 (严格JSON, 不要markdown):
{
  "actions": [
    {"type": "command", "device": "esp32_lipreading_iot", "cmd": 1, "desc": "打开风扇"},
    {"type": "light", "device": "esp32_lipreading_iot", "cmd": 8, "desc": "打开柜子灯"},
    {"type": "rgb", "device": "esp32_lipreading_iot", "r": 1023, "g": 0, "b": 0, "desc": "红色氛围灯"},
    {"type": "scene", "scene": "home", "desc": "回家场景"}
  ],
  "reply": "好的，已为您打开风扇"
}

注意：
- 只返回JSON，不要有任何其他文字
- reply 用口语化中文
- 如果用户问查询类问题，actions 放 query 类型
- 多个操作放在 actions 数组里"""


# ═══════════ STT: faster-whisper ═══════════
async def stt_transcribe(audio_bytes: bytes, filename: str = "audio.webm") -> str:
    """发送音频到 faster-whisper STT 服务，返回识别文字。"""
    stt_url = "http://localhost:5003/stt"
    try:
        form = aiohttp.FormData()
        form.add_field("audio", audio_bytes, filename=filename, content_type="audio/webm")
        async with aiohttp.ClientSession() as session:
            async with session.post(stt_url, data=form, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    text = (data.get("text") or "").strip()
                    logger.info(f"[STT] 识别: {text}")
                    return text
                else:
                    logger.error(f"[STT] HTTP {resp.status}")
                    return ""
    except Exception as e:
        logger.error(f"[STT] 错误: {e}")
        return ""


# ═══════════ AI: DeepSeek 指令解析 ═══════════
async def ai_parse_command(text: str) -> dict:
    """调用 DeepSeek API 将自然语言解析为 JSON 指令。"""
    # 获取 API Key
    api_key = await get_config("ai_api_key")
    if not api_key:
        # 降级到文件配置
        try:
            with open("ai_config.json", "r") as f:
                cfg = json.load(f)
            api_key = cfg.get("api_key", "")
            api_base = cfg.get("api_base", "https://api.deepseek.com/v1")
            model = cfg.get("model", "deepseek-chat")
        except Exception:
            api_key = ""
            api_base = "https://api.deepseek.com/v1"
            model = "deepseek-chat"
    else:
        api_base = await get_config("ai_api_base") or "https://api.deepseek.com/v1"
        model = await get_config("ai_api_model") or "deepseek-chat"

    if not api_key or api_key == "sk-your-deepseek-api-key":
        return {
            "actions": [],
            "reply": "AI 未配置，请先在设置页面配置 DeepSeek API Key",
            "ai_enabled": False,
        }

    url = f"{api_base}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        "max_tokens": 500,
        "temperature": 0.1,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    content = data["choices"][0]["message"]["content"]
                    # 尝试解析 JSON
                    content = content.strip()
                    if content.startswith("```"):
                        content = content.split("```")[1]
                        if content.startswith("json"):
                            content = content[4:]
                        content = content.strip()
                    parsed = json.loads(content)
                    logger.info(f"[AI] 解析: {len(parsed.get('actions', []))} 条指令")
                    return parsed
                else:
                    error = await resp.text()
                    logger.error(f"[AI] HTTP {resp.status}: {error[:200]}")
                    return {"actions": [], "reply": "AI 解析失败，请重试", "ai_enabled": True}
    except json.JSONDecodeError as e:
        logger.error(f"[AI] JSON解析失败: {e}")
        return {"actions": [], "reply": "AI 返回格式异常", "ai_enabled": True}
    except Exception as e:
        logger.error(f"[AI] 错误: {e}")
        return {"actions": [], "reply": f"AI 服务异常: {e}", "ai_enabled": True}


# ═══════════ TTS: MiniMax API ═══════════
async def tts_synthesize(text: str) -> str | None:
    """调用 MiniMax API 合成语音，返回 base64 音频。"""
    minimax_key = await get_config("minimax_api_key")
    if not minimax_key:
        try:
            with open("ai_config.json", "r") as f:
                cfg = json.load(f)
            minimax_key = cfg.get("minimax_api_key", "")
        except Exception:
            minimax_key = ""

    if not minimax_key:
        logger.warning("[TTS] MiniMax API Key 未配置")
        return None

    voice_id = await get_config("tts_voice_id") or "qiaopi_mengmei"

    url = "https://api.minimaxi.com/v1/t2a_v2"
    headers = {
        "Authorization": f"Bearer {minimax_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": "speech-2.8-hd",
        "text": text,
        "stream": False,
        "voice_setting": {"voice_id": voice_id, "speed": 1.0, "vol": 1.0, "pitch": 0},
        "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1},
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    import base64
                    raw = await resp.text()
                    data = json.loads(raw)
                    hex_audio = data.get("data", {}).get("audio")
                    if hex_audio:
                        audio_bytes = bytes.fromhex(hex_audio)
                        b64 = base64.b64encode(audio_bytes).decode("utf-8")
                        logger.info(f"[TTS] MiniMax OK | {len(audio_bytes)} bytes")
                        return b64
                    else:
                        logger.error("[TTS] MiniMax 无音频数据")
                        return None
                else:
                    error = await resp.text()
                    logger.error(f"[TTS] MiniMax HTTP {resp.status}: {error[:200]}")
                    return None
    except Exception as e:
        logger.error(f"[TTS] MiniMax 错误: {e}")
        return None


# ═══════════ 执行指令 ═══════════
async def execute_actions(actions: list) -> list:
    """执行 AI 解析出的指令列表，返回执行结果。"""
    from mqtt_client import publish_command
    from models import get_device
    import aiohttp

    results = []
    for action in actions:
        atype = action.get("type", "")
        desc = action.get("desc", "")
        device = action.get("device", "esp32_lipreading_iot")

        try:
            if atype == "command":
                cmd = int(action.get("cmd", 0))
                publish_command(device, cmd)
                results.append({"action": desc, "status": "sent", "cmd": cmd})

            elif atype == "light":
                cmd = int(action.get("cmd", 0))
                publish_command(device, cmd)
                results.append({"action": desc, "status": "sent", "cmd": cmd})

            elif atype == "rgb":
                r = int(action.get("r", 0))
                g = int(action.get("g", 0))
                b = int(action.get("b", 0))
                async with aiohttp.ClientSession() as session:
                    await session.post(
                        f"http://localhost:8000/api/devices/{device}/rgb",
                        json={"r": r, "g": g, "b": b},
                    )
                results.append({"action": desc, "status": "sent", "rgb": [r, g, b]})

            elif atype == "scene":
                scene = action.get("scene", "")
                async with aiohttp.ClientSession() as session:
                    await session.post(f"http://localhost:8000/api/scene/{scene}")
                results.append({"action": desc, "status": "sent", "scene": scene})

            elif atype == "query":
                query = action.get("query", "")
                # 查询当前设备状态
                dev = await get_device(device)
                if dev:
                    if query == "temperature":
                        val = dev.get("temperature", "--")
                        results.append({"action": desc, "status": "query", "value": f"{val}°C"})
                    elif query == "humidity":
                        val = dev.get("humidity", "--")
                        results.append({"action": desc, "status": "query", "value": f"{val}%"})
                    else:
                        results.append({"action": desc, "status": "query", "value": "暂无数据"})
                else:
                    results.append({"action": desc, "status": "error", "msg": "设备未找到"})

        except Exception as e:
            results.append({"action": desc, "status": "error", "msg": str(e)})

    return results
