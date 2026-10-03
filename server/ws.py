"""WebSocket manager — pushes real-time events to connected dashboard clients."""

import json
import logging
import traceback
from fastapi import WebSocket

logger = logging.getLogger("ws")

# All connected WebSocket clients
_connections: list[WebSocket] = []


async def register(ws: WebSocket):
    try:
        await ws.accept()
        _connections.append(ws)
        client = ws.client.host if ws.client else "?"
        logger.info(f"WebSocket 连接: {client} (共 {len(_connections)} 个客户端)")
    except Exception as e:
        logger.error(f"WebSocket accept 失败: {e}\n{traceback.format_exc()}")
        raise


async def unregister(ws: WebSocket):
    try:
        if ws in _connections:
            _connections.remove(ws)
        client = ws.client.host if ws.client else "?"
        logger.info(f"WebSocket 断开: {client} (剩余 {len(_connections)} 个)")
    except Exception as e:
        logger.error(f"WebSocket unregister 异常: {e}")


async def broadcast(event: str, data: dict):
    """Push an event to all connected WebSocket clients."""
    payload = json.dumps({"event": event, "data": data}, ensure_ascii=False)
    dead: list[WebSocket] = []
    for ws in _connections:
        try:
            await ws.send_text(payload)
        except RuntimeError as e:
            # Connection already closed
            logger.debug(f"WebSocket 发送跳过 (已关闭): {e}")
            dead.append(ws)
        except Exception as e:
            logger.warning(f"WebSocket 发送失败: {e}")
            dead.append(ws)
    for ws in dead:
        await unregister(ws)
    if dead:
        logger.info(f"清理了 {len(dead)} 个断开的 WebSocket 连接")


async def handle(ws: WebSocket):
    """Main WebSocket loop for a single client."""
    client_ip = ws.client.host if ws.client else "?"
    await register(ws)
    try:
        while True:
            data = await ws.receive_text()
            if data == "ping":
                await ws.send_text('{"event":"pong","data":{}}')
            else:
                logger.debug(f"WebSocket 收到 [{client_ip}]: {data[:100]}")
    except RuntimeError as e:
        # Normal disconnect
        logger.debug(f"WebSocket [{client_ip}] 正常断开: {e}")
    except Exception as e:
        logger.warning(f"WebSocket [{client_ip}] 异常: {e}\n{traceback.format_exc()}")
    finally:
        await unregister(ws)
