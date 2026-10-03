"""SQLite data models for ESP32 IoT server."""

import logging
import time
import aiosqlite
import traceback
from datetime import datetime

logger = logging.getLogger("db")

DB_PATH = "iot_data.db"


async def init_db():
    """Create tables if they don't exist."""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS devices (
                    device_id   TEXT PRIMARY KEY,
                    name        TEXT DEFAULT '',
                    status      TEXT DEFAULT 'offline',
                    temperature REAL,
                    humidity    REAL,
                    last_seen   TEXT
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS telemetry_log (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id   TEXT NOT NULL,
                    temperature REAL,
                    humidity    REAL,
                    timestamp   TEXT NOT NULL
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS commands (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id   TEXT NOT NULL,
                    cmd         INTEGER NOT NULL,
                    cmd_name    TEXT DEFAULT '',
                    source      TEXT DEFAULT 'web',
                    timestamp   TEXT NOT NULL
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS config (
                    key         TEXT PRIMARY KEY,
                    value       TEXT NOT NULL DEFAULT ''
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS access_log (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id   TEXT NOT NULL,
                    action      TEXT NOT NULL,
                    servo_angle INTEGER,
                    light       INTEGER,
                    source      TEXT DEFAULT 'web',
                    timestamp   TEXT NOT NULL
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS rfid_log (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id   TEXT NOT NULL,
                    card_uid    TEXT NOT NULL,
                    timestamp   TEXT NOT NULL
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS presence_log (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id   TEXT NOT NULL,
                    motion      INTEGER NOT NULL,
                    timestamp   TEXT NOT NULL
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS ai_reports (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_date TEXT NOT NULL,
                    report_type TEXT DEFAULT 'daily',
                    content     TEXT NOT NULL,
                    anomalies   TEXT DEFAULT '[]',
                    generated   TEXT NOT NULL
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_device TEXT NOT NULL,
                    to_device   TEXT NOT NULL,
                    text        TEXT NOT NULL,
                    timestamp   TEXT NOT NULL
                )
            """)
            await db.commit()
        logger.info(f"数据库初始化完成 ({DB_PATH})")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}\n{traceback.format_exc()}")
        raise


async def upsert_device(device_id: str, status: str = "online"):
    """Insert or update a device record."""
    now = datetime.now().isoformat()
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                """INSERT INTO devices (device_id, status, last_seen)
                   VALUES (?, ?, ?)
                   ON CONFLICT(device_id) DO UPDATE SET
                   status=excluded.status, last_seen=excluded.last_seen""",
                (device_id, status, now),
            )
            await db.commit()
        logger.debug(f"设备登记: {device_id} → {status}")
    except Exception as e:
        logger.error(f"设备登记失败 [{device_id}]: {e}\n{traceback.format_exc()}")


async def update_device_telemetry(device_id: str, temperature: float, humidity: float):
    """Update device latest telemetry + append to log."""
    now = datetime.now().isoformat()
    _t0 = time.time()
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                """UPDATE devices SET temperature=?, humidity=?, last_seen=?, status='online'
                   WHERE device_id=?""",
                (temperature, humidity, now, device_id),
            )
            await db.execute(
                """INSERT INTO telemetry_log (device_id, temperature, humidity, timestamp)
                   VALUES (?, ?, ?, ?)""",
                (device_id, temperature, humidity, now),
            )
            await db.commit()
        logger.debug(f"遥测入库: [{device_id}] {temperature}°C / {humidity}% ({time.time()-_t0:.3f}s)")
    except Exception as e:
        logger.error(f"遥测入库失败 [{device_id}]: {e}\n{traceback.format_exc()}")


async def set_device_offline(device_id: str):
    """Mark a device as offline."""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE devices SET status='offline' WHERE device_id=?",
                (device_id,),
            )
            await db.commit()
        logger.info(f"设备离线: {device_id}")
    except Exception as e:
        logger.error(f"设备离线标记失败 [{device_id}]: {e}\n{traceback.format_exc()}")


async def get_all_devices() -> list[dict]:
    """Return all devices with latest data."""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM devices ORDER BY last_seen DESC"
            )
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]
    except Exception as e:
        logger.error(f"设备列表查询失败: {e}\n{traceback.format_exc()}")
        return []


async def get_device(device_id: str) -> dict | None:
    """Return a single device."""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM devices WHERE device_id=?", (device_id,)
            )
            row = await cursor.fetchone()
            return dict(row) if row else None
    except Exception as e:
        logger.error(f"设备查询失败 [{device_id}]: {e}\n{traceback.format_exc()}")
        return None


async def get_telemetry_history(device_id: str, hours: int = 24) -> list[dict]:
    """Return telemetry history for a device."""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """SELECT * FROM telemetry_log
                   WHERE device_id=? AND timestamp >= datetime('now', ? || ' hours')
                   ORDER BY timestamp DESC LIMIT 2000""",
                (device_id, f"-{hours}"),
            )
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]
    except Exception as e:
        logger.error(f"遥测历史查询失败 [{device_id}]: {e}\n{traceback.format_exc()}")
        return []


async def save_message(from_device: str, to_device: str, text: str):
    """Save a device-to-device message."""
    now = datetime.now().isoformat()
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                """INSERT INTO messages (from_device, to_device, text, timestamp)
                   VALUES (?, ?, ?, ?)""",
                (from_device, to_device, text, now),
            )
            await db.commit()
        logger.debug(f"消息入库: [{from_device}] → [{to_device}]: {text[:50]}")
    except Exception as e:
        logger.error(f"消息入库失败 [{from_device}→{to_device}]: {e}\n{traceback.format_exc()}")


async def save_command_log(device_id: str, cmd: int, cmd_name: str = "", source: str = "web"):
    """Save a control command to the log."""
    now = datetime.now().isoformat()
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                """INSERT INTO commands (device_id, cmd, cmd_name, source, timestamp)
                   VALUES (?, ?, ?, ?, ?)""",
                (device_id, cmd, cmd_name, source, now),
            )
            await db.commit()
        logger.debug(f"指令入库: [{device_id}] {cmd} ({cmd_name})")
    except Exception as e:
        logger.error(f"指令入库失败 [{device_id}]: {e}\n{traceback.format_exc()}")


# ── Config ────────────────────────────────────

async def get_config(key: str) -> str | None:
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT value FROM config WHERE key=?", (key,))
            row = await cursor.fetchone()
            return row[0] if row else None
    except Exception as e:
        logger.error(f"配置读取失败 [{key}]: {e}")
        return None


async def set_config(key: str, value: str):
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)",
                (key, value),
            )
            await db.commit()
        logger.debug(f"配置更新: {key}={value}")
    except Exception as e:
        logger.error(f"配置写入失败 [{key}]: {e}")


async def get_all_config() -> dict[str, str]:
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT key, value FROM config")
            rows = await cursor.fetchall()
            return {r[0]: r[1] for r in rows}
    except Exception as e:
        logger.error(f"配置全量读取失败: {e}")
        return {}


# ── Access Log ────────────────────────────────

async def save_access_log(device_id: str, action: str, servo_angle: int = None,
                          light: int = None, source: str = "web"):
    now = datetime.now().isoformat()
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                """INSERT INTO access_log (device_id, action, servo_angle, light, source, timestamp)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (device_id, action, servo_angle, light, source, now),
            )
            await db.commit()
        logger.info(f"开门记录: [{device_id}] {action}")
    except Exception as e:
        logger.error(f"开门记录失败: {e}")


async def get_access_log(device_id: str = None, limit: int = 50) -> list[dict]:
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            if device_id:
                cursor = await db.execute(
                    "SELECT * FROM access_log WHERE device_id=? ORDER BY timestamp DESC LIMIT ?",
                    (device_id, limit),
                )
            else:
                cursor = await db.execute(
                    "SELECT * FROM access_log ORDER BY timestamp DESC LIMIT ?",
                    (limit,),
                )
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]
    except Exception as e:
        logger.error(f"开门记录查询失败: {e}")
        return []


# ── RFID Log ───────────────────────────────────

async def save_rfid_log(device_id: str, card_uid: str):
    now = datetime.now().isoformat()
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO rfid_log (device_id, card_uid, timestamp) VALUES (?, ?, ?)",
                (device_id, card_uid, now),
            )
            await db.commit()
        logger.info(f"RFID: [{device_id}] 卡号 {card_uid}")
    except Exception as e:
        logger.error(f"RFID 记录失败: {e}")


async def get_rfid_log(device_id: str = None, limit: int = 50) -> list[dict]:
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            if device_id:
                cursor = await db.execute(
                    "SELECT * FROM rfid_log WHERE device_id=? ORDER BY timestamp DESC LIMIT ?",
                    (device_id, limit),
                )
            else:
                cursor = await db.execute(
                    "SELECT * FROM rfid_log ORDER BY timestamp DESC LIMIT ?",
                    (limit,),
                )
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]
    except Exception as e:
        logger.error(f"RFID 记录查询失败: {e}")
        return []


# ── Presence Log ───────────────────────────────

async def save_presence_log(device_id: str, motion: bool):
    now = datetime.now().isoformat()
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO presence_log (device_id, motion, timestamp) VALUES (?, ?, ?)",
                (device_id, 1 if motion else 0, now),
            )
            await db.commit()
        logger.debug(f"红外: [{device_id}] {'有人' if motion else '无人'}")
    except Exception as e:
        logger.error(f"红外记录失败: {e}")


# ── AI Reports ─────────────────────────────────

async def save_ai_report(report_date: str, report_type: str, content: str, anomalies: str = "[]"):
    now = datetime.now().isoformat()
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                """INSERT OR REPLACE INTO ai_reports (report_date, report_type, content, anomalies, generated)
                   VALUES (?, ?, ?, ?, ?)""",
                (report_date, report_type, content, anomalies, now),
            )
            await db.commit()
        logger.info(f"AI 报告已保存: {report_date}")
    except Exception as e:
        logger.error(f"AI 报告保存失败: {e}")


async def get_ai_report(report_date: str) -> dict | None:
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM ai_reports WHERE report_date=? ORDER BY generated DESC LIMIT 1",
                (report_date,),
            )
            row = await cursor.fetchone()
            return dict(row) if row else None
    except Exception as e:
        logger.error(f"AI 报告查询失败 [{report_date}]: {e}")
        return None


async def get_ai_reports(limit: int = 30) -> list[dict]:
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT report_date, report_type, generated FROM ai_reports ORDER BY generated DESC LIMIT ?",
                (limit,),
            )
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]
    except Exception as e:
        logger.error(f"AI 报告列表查询失败: {e}")
        return []


async def get_device_messages(device_id: str, limit: int = 50) -> list[dict]:
    """Return messages sent to a device."""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """SELECT * FROM messages
                   WHERE to_device=? OR from_device=?
                   ORDER BY timestamp DESC LIMIT ?""",
                (device_id, device_id, limit),
            )
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]
    except Exception as e:
        logger.error(f"消息查询失败 [{device_id}]: {e}\n{traceback.format_exc()}")
        return []
