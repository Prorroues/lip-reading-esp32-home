"""FastAPI entry point — ESP32 IoT multi-device server."""

import os
import sys
import asyncio as _asyncio
import logging
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from models import init_db
from mqtt_client import start_mqtt, stop_mqtt, set_broadcast, load_thresholds_from_config
from routes import router
from ws import handle as ws_handle, broadcast
from exporter import flush_hourly, generate_summary

# ── Logging setup ──────────────────────────────

LOG_FORMAT = "%(asctime)s [%(name)-4s] %(levelname)-7s %(message)s"
LOG_DATE = "%H:%M:%S"

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=LOG_DATE)

# Quiet down noisy third-party loggers
for noisy in ("uvicorn", "uvicorn.access", "paho"):
    logging.getLogger(noisy).setLevel(logging.WARNING)

logger = logging.getLogger("server")


# ── App lifecycle ──────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle with error handling."""
    # ── Startup ──
    logger.info("=" * 50)
    logger.info("ESP32 IoT Server 启动中...")
    logger.info("=" * 50)

    try:
        logger.info("初始化数据库...")
        await init_db()
    except Exception as e:
        logger.critical(f"数据库初始化失败，服务器无法启动: {e}")
        sys.exit(1)

    try:
        logger.info("注册 WebSocket 广播回调...")
        set_broadcast(broadcast)
    except Exception as e:
        logger.critical(f"WebSocket 回调注册失败: {e}")
        sys.exit(1)

    try:
        logger.info("启动 MQTT 客户端...")
        start_mqtt()
        logger.info("加载用户阈值配置...")
        await load_thresholds_from_config()
    except Exception as e:
        logger.critical(f"MQTT 客户端启动失败: {e}")
        logger.critical("请确认 Mosquitto 在 10.31.91.209:1883 运行")
        sys.exit(1)

    logger.info("-" * 50)
    logger.info("服务器就绪")
    logger.info("  仪表盘:   http://localhost:8000")
    logger.info("  API 文档: http://localhost:8000/docs")
    logger.info("  WebSocket: ws://localhost:8000/ws")
    # Start hourly aggregation background task
    async def _hourly_loop():
        while True:
            await _asyncio.sleep(3600)  # every hour
            try:
                flush_hourly()
                generate_summary()
            except Exception as e:
                logger.error(f"定时聚合失败: {e}")
    hourly_task = _asyncio.create_task(_hourly_loop())

    # 定时任务检查 (每60秒)
    from routes import check_scheduled_tasks
    async def _scheduler_loop():
        while True:
            await _asyncio.sleep(60)
            try:
                await check_scheduled_tasks()
            except Exception as e:
                logger.error(f"定时任务检查失败: {e}")
    scheduler_task = _asyncio.create_task(_scheduler_loop())

    from lip_poller import poll_vsr_latest_loop
    lip_poller_task = _asyncio.create_task(poll_vsr_latest_loop())
    logger.info("唇语结果轮询: http://127.0.0.1:24060/recognition/latest")

    logger.info("-" * 50)

    yield  # ── Server running ──

    # Cancel background tasks
    hourly_task.cancel()
    scheduler_task.cancel()
    lip_poller_task.cancel()
    try:
        await hourly_task
    except _asyncio.CancelledError:
        pass
    try:
        await scheduler_task
    except _asyncio.CancelledError:
        pass
    try:
        await lip_poller_task
    except _asyncio.CancelledError:
        pass

    # ── Shutdown ──
    logger.info("服务器关闭中...")
    try:
        stop_mqtt()
    except Exception as e:
        logger.error(f"MQTT 关闭异常: {e}")


# ── App ────────────────────────────────────────

app = FastAPI(title="ESP32 IoT Server", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Redirect root to dashboard.html
from fastapi.responses import FileResponse

@app.get("/")
async def root():
    dashboard = os.path.join(os.path.dirname(__file__), "..", "web", "dashboard.html")
    if os.path.exists(dashboard):
        return FileResponse(dashboard)
    return {"detail": "dashboard.html not found"}

# Serve static files from parent dir (for dashboard.html assets)
try:
    app.mount("/static", StaticFiles(directory="../web"), name="static")
    logger.info("静态文件服务: 已挂载上级目录")
except Exception as e:
    logger.warning(f"静态文件挂载失败: {e}")


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws_handle(ws)


# ── Entry point ────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    logger.info("以开发模式启动 (reload=True)")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="warning")
