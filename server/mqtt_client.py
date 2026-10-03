"""MQTT client module - bridges broker messages to SQLite and WebSocket broadcast."""

import json
import time
import asyncio
import logging
import traceback
import socket
import threading
from typing import Callable, Awaitable

import paho.mqtt.client as mqtt

from models import (
    upsert_device, update_device_telemetry, set_device_offline,
    save_command_log, get_all_devices,
)
from exporter import (
    append_telemetry, append_command, append_message, write_devices_snapshot,
)

logger = logging.getLogger("mqtt")

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 1883
TOPIC_TELEMETRY = "esp32/+/telemetry"
TOPIC_STATUS = "esp32/+/status"
TOPIC_LIP_TEXT = "lip_reading/src_text"

_client: mqtt.Client | None = None
_broadcast: Callable[[str, dict], Awaitable[None]] | None = None
_connect_fail_count = 0
_main_loop = None
MAX_CONNECT_FAIL_LOG = 5

def set_broadcast(fn):
    global _broadcast
    _broadcast = fn

async def _emit(event, data):
    try:
        if _broadcast:
            await _broadcast(event, data)
    except Exception as e:
        logger.error(f"WebSocket broadcast failed [{event}]: {e}")

def _extract_device_id(topic):
    parts = topic.split("/")
    return parts[1] if len(parts) >= 3 else "unknown"

def on_connect(client, userdata, flags, reason_code, properties=None):
    global _connect_fail_count
    if reason_code == 0:
        _connect_fail_count = 0
        logger.info(f"MQTT connected -> {BROKER_HOST}:{BROKER_PORT}")
        for topic in [TOPIC_TELEMETRY, TOPIC_STATUS]:
            result, mid = client.subscribe(topic, qos=0)
            if result == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"Subscribed {topic}")
    else:
        _connect_fail_count += 1
        logger.error(f"MQTT connect failed: rc={reason_code}")

def on_disconnect(client, userdata, flags, reason_code=0, properties=None):
    global _connect_fail_count
    _connect_fail_count += 1
    if _connect_fail_count <= MAX_CONNECT_FAIL_LOG:
        logger.warning(f"MQTT disconnected (rc={reason_code})")

def on_message(client, userdata, msg):
    topic = msg.topic
    device_id = _extract_device_id(topic)
    try:
        payload_str = msg.payload.decode("utf-8", errors="replace")
    except Exception as e:
        logger.error(f"[{device_id}] decode failed: {e}")
        return
    if _main_loop is None:
        return
    loop = _main_loop

    if topic.endswith("/telemetry"):
        try:
            data = json.loads(payload_str)
        except json.JSONDecodeError:
            return
        t = data.get("temperature")
        h = data.get("humidity")
        if t is None or h is None:
            return
        try:
            asyncio.run_coroutine_threadsafe(update_device_telemetry(device_id, t, h), loop)
        except Exception as e:
            logger.error(f"[{device_id}] DB write error: {e}")
        auto_rgb = data.get("auto_rgb", True)
        rgb_state = data.get("rgb_state", "")
        append_telemetry(device_id, t, h, auto_rgb, rgb_state)
        asyncio.run_coroutine_threadsafe(
            _emit("telemetry", {"device_id": device_id, "temperature": t, "humidity": h, "auto_rgb": auto_rgb, "rgb_state": rgb_state}), loop)

    elif topic.endswith("/status"):
        status = payload_str.strip().lower()
        logger.info(f"[{device_id}] status: {status}")
        if status == "online":
            asyncio.run_coroutine_threadsafe(upsert_device(device_id, "online"), loop)
        else:
            asyncio.run_coroutine_threadsafe(set_device_offline(device_id), loop)
        asyncio.run_coroutine_threadsafe(_emit("status", {"device_id": device_id, "status": status}), loop)
        asyncio.run_coroutine_threadsafe(_snapshot_devices(), loop)


_last_lip_text = ""
_last_lip_time = 0.0
LIP_DEBOUNCE_SEC = 6.0


def publish_lip_src_text(text: str) -> None:
    """把识别纯文本转发给眼镜显示/TTS（眼镜仍订阅 lip_reading/src_text）。"""
    if _client is None or not text:
        return
    try:
        info = _client.publish(TOPIC_LIP_TEXT, text, qos=0)
        if info.rc == mqtt.MQTT_ERR_SUCCESS:
            logger.info("-> glasses src_text: %s", text[:50])
    except Exception as e:
        logger.error("publish src_text failed: %s", e)


def dispatch_lip_text(text: str) -> dict:
    """匹配唇语文本并下发家居数字指令。未命中则不发 MQTT。"""
    global _last_lip_text, _last_lip_time
    from lip_matcher import match_lip_text, HOME_DEVICE_ID

    result = match_lip_text(text)
    now = time.time()
    if (
        result.get("matched")
        and text == _last_lip_text
        and now - _last_lip_time < LIP_DEBOUNCE_SEC
    ):
        logger.info("Lip debounce skip: %r", text)
        result = dict(result)
        result["debounced"] = True
        return result

    if result.get("matched"):
        _last_lip_text = text
        _last_lip_time = now
        device_id = result.get("device_id", HOME_DEVICE_ID)
        for cmd in result.get("commands", []):
            publish_command(device_id, cmd, caller="lip")
        logger.info("Lip match: %r -> %s (%s)", text, result.get("commands"), result.get("reply"))
    else:
        logger.info("Lip unmatched: %r", text)
    if _main_loop is not None:
        try:
            asyncio.run_coroutine_threadsafe(_emit("lip_command", result), _main_loop)
        except Exception as e:
            logger.error(f"lip_command broadcast failed: {e}")
    return result


_energy_stats = {}
_energy_lock = threading.Lock()

FAN_CMDS = {1, 2, 3, 4}
LIGHT_ON_CMDS = {8, 10, 12, 14, 16, 18}

def _track_energy(device_id, cmd):
    today = time.strftime("%Y-%m-%d")
    with _energy_lock:
        if today not in _energy_stats:
            _energy_stats[today] = {"fan_starts": 0, "light_on_count": 0, "fan_last_on": 0.0}
        s = _energy_stats[today]
        if cmd in FAN_CMDS and cmd % 2 == 1:
            s["fan_starts"] += 1
            s["fan_last_on"] = time.time()
        if cmd in LIGHT_ON_CMDS:
            s["light_on_count"] += 1

def get_energy_stats(date=None):
    if date is None: date = time.strftime("%Y-%m-%d")
    with _energy_lock:
        s = _energy_stats.get(date, {"fan_starts": 0, "light_on_count": 0, "fan_last_on": 0.0})
        fan_runtime = int(time.time() - s["fan_last_on"]) if s.get("fan_last_on", 0) > 0 else 0
        return {"date": date, "fan_starts": s.get("fan_starts", 0), "light_on_count": s.get("light_on_count", 0),
                "fan_runtime_seconds": fan_runtime, "estimated_kwh": round((fan_runtime / 3600) * 0.05 + s.get("fan_starts", 0) * 0.001, 3)}

async def load_thresholds_from_config():
    logger.info("传感器阈值加载已跳过（传感器板已移除）")

def start_mqtt():
    global _client, _connect_fail_count, _main_loop
    _connect_fail_count = 0
    try:
        _main_loop = asyncio.get_event_loop()
    except RuntimeError:
        _main_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_main_loop)
    _client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    _client.on_connect = on_connect
    _client.on_disconnect = on_disconnect
    _client.on_message = on_message
    try:
        _client.connect_async(BROKER_HOST, BROKER_PORT, keepalive=60)
        _client.loop_start()
        logger.info(f"MQTT client started -> {BROKER_HOST}:{BROKER_PORT}")
    except Exception as e:
        logger.error(f"MQTT start failed: {e}\n{traceback.format_exc()}")
        raise

def publish_command(device_id, cmd, caller="internal"):
    if _client is None:
        raise RuntimeError("MQTT client not started")
    topic = f"esp32/{device_id}/command"
    payload = str(cmd)
    try:
        info = _client.publish(topic, payload, qos=0)
        if info.rc == mqtt.MQTT_ERR_SUCCESS:
            CMD_NAMES = {1:"fan_on",2:"fan_off",6:"rgb_warm",7:"rgb_off",20:"rgb_auto"}
            logger.info(f"-> [{device_id}] cmd: {cmd} ({CMD_NAMES.get(cmd,'')})")
            try:
                loop = asyncio.get_event_loop()
                asyncio.run_coroutine_threadsafe(save_command_log(device_id, cmd, CMD_NAMES.get(cmd, str(cmd))), loop)
                append_command(device_id, cmd)
            except RuntimeError:
                pass
            _track_energy(device_id, cmd)
    except Exception as e:
        logger.error(f"-> [{device_id}] publish error: {e}")

def publish_message(to_device, from_device, text):
    if _client is None:
        raise RuntimeError("MQTT client not started")
    topic = f"esp32/{to_device}/message"
    payload = json.dumps({"from": from_device, "text": text}, ensure_ascii=False)
    try:
        info = _client.publish(topic, payload, qos=0)
        if info.rc == mqtt.MQTT_ERR_SUCCESS:
            logger.info(f"-> [{to_device}] msg from [{from_device}]: {text[:50]}")
            append_message(from_device, to_device, text)
    except Exception as e:
        logger.error(f"-> [{to_device}] msg error: {e}")

async def _snapshot_devices():
    try:
        devices = await get_all_devices()
        write_devices_snapshot(devices)
    except Exception as e:
        logger.error(f"Snapshot error: {e}")

def stop_mqtt():
    global _client
    if _client:
        try:
            _client.loop_stop()
            _client.disconnect()
            logger.info("MQTT client stopped")
        except Exception as e:
            logger.error(f"MQTT stop error: {e}")
        _client = None
