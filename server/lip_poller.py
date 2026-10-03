"""从唇语服务 24060 拉取最新纯文本，匹配后发家居 MQTT 指令。"""

import asyncio
import logging
import time

import aiohttp

logger = logging.getLogger("lip_poller")

VSR_LATEST_URL = "http://127.0.0.1:24060/recognition/latest"
POLL_INTERVAL_SEC = 1.0
# 8000 晚于识别启动时，第一条结果会被「对齐序号」丢掉。
# 结果够新就立刻下发，只有很久以前的旧结果才跳过。
FRESH_RESULT_SEC = 120.0


def _dispatch(text: str, seq: int) -> None:
    logger.info("从 24060 取到新识别: seq=%s text=%r", seq, text[:80])
    try:
        from mqtt_client import dispatch_lip_text, publish_lip_src_text

        dispatch_lip_text(text)
        publish_lip_src_text(text)
    except Exception as e:
        logger.error("处理唇语文本失败: %s", e)


async def poll_vsr_latest_loop():
    """轮询唇语 /recognition/latest。启动时丢掉过期结果，新鲜结果马上处理。"""
    last_seq = None
    timeout = aiohttp.ClientTimeout(total=3)
    logger.info("开始从唇语服务拉取识别文本: %s", VSR_LATEST_URL)

    while True:
        await asyncio.sleep(POLL_INTERVAL_SEC)
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(VSR_LATEST_URL) as resp:
                    if resp.status != 200:
                        logger.debug("唇语 latest HTTP %s", resp.status)
                        continue
                    data = await resp.json()
        except Exception as e:
            logger.debug("拉取唇语结果失败: %s", e)
            continue

        seq = int(data.get("seq") or 0)
        text = (data.get("plain_text") or data.get("src_recognition_results") or "").strip()
        if seq <= 0 or not text:
            continue
        if last_seq is None:
            last_seq = seq
            updated_at = float(data.get("updated_at") or 0)
            age = time.time() - updated_at if updated_at else 1e9
            if age > FRESH_RESULT_SEC:
                logger.info("已对齐唇语结果序号 seq=%s（旧结果 %.0fs 前），等待新的识别", seq, age)
                continue
            logger.info("启动后发现新鲜识别 seq=%s age=%.1fs，立即处理", seq, age)
            _dispatch(text, seq)
            continue
        if seq == last_seq:
            continue
        last_seq = seq
        _dispatch(text, seq)
