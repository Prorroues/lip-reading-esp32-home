"""Data exporter — writes telemetry, commands, messages to CSV/JSON files for AI analysis."""

import os
import csv
import json
import logging
import traceback
import asyncio
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger("export")

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# File paths
TELEMETRY_CSV   = os.path.join(DATA_DIR, "telemetry.csv")
TELEMETRY_HOURLY= os.path.join(DATA_DIR, "telemetry_hourly.csv")
COMMANDS_CSV    = os.path.join(DATA_DIR, "commands.csv")
MESSAGES_CSV    = os.path.join(DATA_DIR, "messages.csv")
DEVICES_JSON    = os.path.join(DATA_DIR, "devices.json")
SUMMARY_JSON    = os.path.join(DATA_DIR, "summary.json")
# 传感器专用文件
SENSOR_LIGHT_CSV  = os.path.join(DATA_DIR, "sensor_light.csv")
SENSOR_DIST_CSV   = os.path.join(DATA_DIR, "sensor_distance.csv")
SENSOR_CO2_CSV    = os.path.join(DATA_DIR, "sensor_co2.csv")
SENSOR_RFID_CSV   = os.path.join(DATA_DIR, "sensor_rfid.csv")
SENSOR_PRESENCE_CSV = os.path.join(DATA_DIR, "sensor_presence.csv")

# CSV headers
TELEMETRY_HEADER   = ["timestamp", "device_id", "temperature", "humidity", "auto_rgb", "rgb_state"]
TELEMETRY_HOURLY_H = ["hour", "device_id", "avg_temp", "max_temp", "min_temp", "avg_hum", "max_hum", "min_hum", "record_count"]
COMMANDS_HEADER    = ["timestamp", "device_id", "cmd", "cmd_name", "source"]
MESSAGES_HEADER    = ["timestamp", "from_device", "to_device", "text"]

# Hourly aggregation buffer: {device_id: [(temp, hum, ts), ...]}
_hourly_buffer: dict[str, list] = defaultdict(list)
_last_hourly_flush: str = ""


def _ensure_header(path: str, header: list[str]):
    """Write CSV header if file doesn't exist."""
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
        logger.info(f"创建数据文件: {os.path.basename(path)}")

def _ensure_sensor_header(path: str, header: list[str]):
    """Write sensor CSV header if file doesn't exist."""
    _ensure_header(path, header)


def _append_csv(path: str, row: list):
    """Append a single row to CSV file."""
    if "sensor_light" in path:
        _ensure_header(path, SENSOR_LIGHT_HEADER)
    elif "sensor_distance" in path:
        _ensure_header(path, SENSOR_DIST_HEADER)
    elif "sensor_co2" in path:
        _ensure_header(path, SENSOR_CO2_HEADER)
    elif "sensor_rfid" in path:
        _ensure_header(path, SENSOR_RFID_HEADER)
    elif "sensor_presence" in path:
        _ensure_header(path, SENSOR_PRESENCE_HEADER)
    else:
        _ensure_header(path, TELEMETRY_HEADER if "telemetry" in path else
                             TELEMETRY_HOURLY_H if "hourly" in path else
                             COMMANDS_HEADER if "command" in path else
                             MESSAGES_HEADER)
    try:
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)
    except PermissionError as e:
        logger.error(f"CSV 写入权限不足 [{path}]: {e}")
    except OSError as e:
        logger.error(f"CSV 写入磁盘错误 [{path}]: {e} (磁盘满?)")
    except Exception as e:
        logger.error(f"CSV 写入失败 [{path}]: {e}\n{traceback.format_exc()}")


# ── Telemetry ──────────────────────────────────

def append_telemetry(device_id: str, temperature: float, humidity: float,
                     auto_rgb: bool = True, rgb_state: str = ""):
    """Append a telemetry record to CSV + hourly buffer."""
    now = datetime.now()
    ts = now.isoformat(timespec="seconds")
    row = [ts, device_id, str(temperature), str(humidity),
           "1" if auto_rgb else "0", rgb_state or ""]
    _append_csv(TELEMETRY_CSV, row)

    # Hourly aggregation buffer
    hour_key = now.strftime("%Y-%m-%dT%H:00:00")
    _hourly_buffer[(device_id, hour_key)].append((temperature, humidity))
    logger.debug(f"遥测归档: [{device_id}] {temperature}°C / {humidity}%")


def flush_hourly():
    """Aggregate buffer into hourly CSV. Called every hour."""
    global _last_hourly_flush
    if not _hourly_buffer:
        return

    _ensure_header(TELEMETRY_HOURLY, TELEMETRY_HOURLY_H)
    rows = []
    now = datetime.now()

    for (device_id, hour_key), values in _hourly_buffer.items():
        if not values:
            continue
        temps = [v[0] for v in values]
        hums  = [v[1] for v in values]
        rows.append([
            hour_key, device_id,
            round(sum(temps) / len(temps), 1),
            round(max(temps), 1),
            round(min(temps), 1),
            round(sum(hums) / len(hums), 1),
            round(max(hums), 1),
            round(min(hums), 1),
            len(values),
        ])

    try:
        with open(TELEMETRY_HOURLY, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
    except Exception as e:
        logger.error(f"小时聚合写入失败: {e}")

    _hourly_buffer.clear()
    _last_hourly_flush = now.isoformat(timespec="seconds")
    logger.info(f"小时聚合完成: {len(rows)} 条记录")


# ── Commands ───────────────────────────────────

CMD_NAMES = {
    1: "风扇启动", 2: "风扇停止", 3: "风扇强开", 4: "风扇强关",
    5: "刷新温湿度", 6: "RGB暖色", 7: "RGB关闭",
    8: "柜子灯开", 9: "柜子灯关", 10: "床后灯开", 11: "床后灯关",
    12: "床下前灯开", 13: "床下前灯关", 14: "床头灯开", 15: "床头灯关",
    16: "上左灯开", 17: "上左灯关", 18: "厕所灯开", 19: "厕所灯关",
    20: "RGB自动模式",
}


def append_command(device_id: str, cmd: int, source: str = "web"):
    """Log a control command."""
    now = datetime.now()
    ts = now.isoformat(timespec="seconds")
    cmd_name = CMD_NAMES.get(cmd, f"未知指令{cmd}")
    row = [ts, device_id, str(cmd), cmd_name, source]
    _append_csv(COMMANDS_CSV, row)
    logger.debug(f"指令归档: [{device_id}] {cmd} ({cmd_name})")


# ── Sensor Data (per type) ──────────────────────

SENSOR_LIGHT_HEADER   = ["timestamp", "device_id", "light"]
SENSOR_DIST_HEADER    = ["timestamp", "device_id", "distance_cm"]
SENSOR_CO2_HEADER     = ["timestamp", "device_id", "co2_ppm"]
SENSOR_RFID_HEADER    = ["timestamp", "device_id", "card_uid"]
SENSOR_PRESENCE_HEADER= ["timestamp", "device_id", "motion"]

def append_sensor_light(device_id: str, light: int):
    now = datetime.now()
    row = [now.isoformat(timespec="seconds"), device_id, str(light)]
    _append_csv(SENSOR_LIGHT_CSV, row)
    logger.debug(f"光照归档: [{device_id}] {light}")

def append_sensor_distance(device_id: str, distance_cm: float):
    now = datetime.now()
    row = [now.isoformat(timespec="seconds"), device_id, str(distance_cm)]
    _append_csv(SENSOR_DIST_CSV, row)
    logger.debug(f"距离归档: [{device_id}] {distance_cm}cm")

def append_sensor_co2(device_id: str, co2_ppm: int):
    now = datetime.now()
    row = [now.isoformat(timespec="seconds"), device_id, str(co2_ppm)]
    _append_csv(SENSOR_CO2_CSV, row)
    logger.debug(f"CO2归档: [{device_id}] {co2_ppm}ppm")

def append_sensor_rfid(device_id: str, card_uid: str):
    now = datetime.now()
    row = [now.isoformat(timespec="seconds"), device_id, card_uid]
    _append_csv(SENSOR_RFID_CSV, row)
    logger.debug(f"RFID归档: [{device_id}] {card_uid}")

def append_sensor_presence(device_id: str, motion: bool):
    now = datetime.now()
    row = [now.isoformat(timespec="seconds"), device_id, "1" if motion else "0"]
    _append_csv(SENSOR_PRESENCE_CSV, row)
    logger.debug(f"红外归档: [{device_id}] {'有人' if motion else '无人'}")


# ── Messages ───────────────────────────────────

def append_message(from_device: str, to_device: str, text: str):
    """Log a device-to-device message."""
    now = datetime.now()
    ts = now.isoformat(timespec="seconds")
    row = [ts, from_device, to_device, text]
    _append_csv(MESSAGES_CSV, row)


# ── Device snapshot ─────────────────────────────

def write_devices_snapshot(devices: list[dict]):
    """Write current device states to JSON file."""
    try:
        with open(DEVICES_JSON, "w", encoding="utf-8") as f:
            json.dump({
                "updated": datetime.now().isoformat(timespec="seconds"),
                "devices": devices,
            }, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"设备快照写入失败: {e}")


# ── Daily summary (for AI) ─────────────────────

def generate_summary():
    """Generate a daily summary JSON for AI analysis."""
    try:
        from models import get_all_devices, get_telemetry_history
        import sqlite3
    except ImportError:
        return

    now = datetime.now()
    summary = {
        "generated": now.isoformat(timespec="seconds"),
        "date": now.strftime("%Y-%m-%d"),
        "devices": [],
        "stats": {},
    }

    # Read hourly CSV for daily stats
    if os.path.exists(TELEMETRY_HOURLY):
        daily_temps = []
        daily_hums = []
        today = now.strftime("%Y-%m-%d")
        try:
            with open(TELEMETRY_HOURLY, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("hour", "").startswith(today):
                        daily_temps.append(float(row["avg_temp"]))
                        daily_hums.append(float(row["avg_hum"]))
        except Exception:
            pass

        if daily_temps:
            summary["stats"] = {
                "avg_temperature": round(sum(daily_temps) / len(daily_temps), 1),
                "max_temperature": round(max(daily_temps), 1),
                "min_temperature": round(min(daily_temps), 1),
                "avg_humidity": round(sum(daily_hums) / len(daily_hums), 1),
                "max_humidity": round(max(daily_hums), 1),
                "min_humidity": round(min(daily_hums), 1),
                "hours_recorded": len(daily_temps),
            }

    # Count commands today
    if os.path.exists(COMMANDS_CSV):
        cmd_counts = defaultdict(int)
        today = now.strftime("%Y-%m-%d")
        try:
            with open(COMMANDS_CSV, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("timestamp", "").startswith(today):
                        cmd_counts[row.get("cmd_name", "?")] += 1
        except Exception:
            pass
        if cmd_counts:
            summary["command_counts"] = dict(cmd_counts)

    try:
        with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        logger.info(f"AI 摘要已生成: {SUMMARY_JSON}")
    except Exception as e:
        logger.error(f"摘要生成失败: {e}")

    return summary


# ── File listing ───────────────────────────────

def list_data_files() -> list[dict]:
    """Return metadata for all data files."""
    files = []
    for name in ["telemetry.csv", "telemetry_hourly.csv", "commands.csv",
                  "messages.csv", "devices.json", "summary.json",
                  "sensor_light.csv", "sensor_distance.csv", "sensor_co2.csv",
                  "sensor_rfid.csv", "sensor_presence.csv"]:
        path = os.path.join(DATA_DIR, name)
        if os.path.exists(path):
            size = os.path.getsize(path)
            mtime = datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
            files.append({
                "name": name,
                "size_bytes": size,
                "size_kb": round(size / 1024, 1),
                "updated": mtime,
            })
    return files
