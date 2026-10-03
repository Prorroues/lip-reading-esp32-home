"""唇语识别文本 → 家居 MQTT 数字指令。

唇语服务本身不改；这里只消费已有的纯文本（MQTT lip_reading/src_text
或 POST /api/lip/command），命中词表后对家居 ESP32 下发数字指令。
"""

from __future__ import annotations

# 长词在前，避免「关风扇」被更短的词抢走。
# 每条: (关键词列表, 指令号或指令号列表, 说明)
_RULES: list[tuple[list[str], int | list[int], str]] = [
    (["关闭风扇", "关掉风扇", "关上风扇", "关风扇", "停止风扇", "停风扇"], 2, "关闭风扇"),
    (["打开风扇", "开启风扇", "开风扇", "启动风扇"], 1, "打开风扇"),
    (["关闭氛围灯", "关掉氛围灯", "关氛围灯", "关闭彩灯", "关彩灯", "关RGB"], 7, "关闭氛围灯"),
    (["打开氛围灯", "开启氛围灯", "开氛围灯", "暖色", "暖光"], 6, "氛围灯暖色"),
    (["自动氛围灯", "氛围灯自动"], 20, "氛围灯暖色"),
    (["关闭柜子灯", "关掉柜子灯", "关柜子灯"], 9, "关闭柜子灯"),
    (["打开柜子灯", "开启柜子灯", "开柜子灯"], 8, "打开柜子灯"),
    (["关闭床后灯", "关掉床后灯", "关床后灯"], 11, "关闭床后灯"),
    (["打开床后灯", "开启床后灯", "开床后灯"], 10, "打开床后灯"),
    (["关闭床下灯", "关掉床下灯", "关床下灯", "关闭床下前灯", "关床下前灯"], 13, "关闭床下灯"),
    (["打开床下灯", "开启床下灯", "开床下灯", "打开床下前灯", "开床下前灯"], 12, "打开床下灯"),
    (["关闭床头灯", "关掉床头灯", "关床头灯"], 15, "关闭床头灯"),
    (["打开床头灯", "开启床头灯", "开床头灯"], 14, "打开床头灯"),
    (["关闭上左灯", "关掉上左灯", "关上左灯"], 17, "关闭上左灯"),
    (["打开上左灯", "开启上左灯", "开上左灯"], 16, "打开上左灯"),
    (["关闭厕所灯", "关掉厕所灯", "关厕所灯"], 19, "关闭厕所灯"),
    (["打开厕所灯", "开启厕所灯", "开厕所灯"], 18, "打开厕所灯"),
    (
        ["关闭所有灯", "关掉所有灯", "关上所有灯", "关灯", "全部关灯"],
        [9, 11, 13, 15, 17, 19, 7],
        "关闭全部灯光",
    ),
    (
        ["打开所有灯", "开启所有灯", "开所有灯", "全部开灯", "开灯"],
        [8, 10, 12, 14, 16, 18],
        "打开全部灯光",
    ),
    (
        ["我回来了", "一键回家", "回家"],
        [14, 8, 6],
        "回家场景",
    ),
    (
        ["我出门了", "一键离家", "离家", "出门"],
        [9, 11, 13, 15, 17, 19, 2, 7],
        "离家场景",
    ),
]

HOME_DEVICE_ID = "esp32_lipreading_iot"


def _normalize(text: str) -> str:
    if not text:
        return ""
    cleaned = text.strip()
    for ch in (" ", "\t", "\n", "，", ",", "。", ".", "！", "!", "？", "?", "、"):
        cleaned = cleaned.replace(ch, "")
    return cleaned


def match_lip_text(text: str) -> dict:
    """匹配识别文本。未命中时 matched=False，不发指令。"""
    original = (text or "").strip()
    normalized = _normalize(original)
    if not normalized:
        return {
            "matched": False,
            "text": original,
            "commands": [],
            "descs": [],
            "reply": "没有识别到文字",
        }

    commands: list[int] = []
    descs: list[str] = []
    seen_cmds: set[int] = set()

    for keywords, cmds, desc in _RULES:
        if not any(key in normalized for key in keywords):
            continue
        cmd_list = cmds if isinstance(cmds, list) else [cmds]
        added = False
        for cmd in cmd_list:
            if cmd in seen_cmds:
                continue
            seen_cmds.add(cmd)
            commands.append(cmd)
            added = True
        if added:
            descs.append(desc)

    if not commands:
        if "风扇" in normalized or ("风" in normalized and "扇" in normalized):
            if any(k in normalized for k in ("关", "停")):
                commands, descs = [2], ["关闭风扇"]
            else:
                commands, descs = [1], ["打开风扇"]
        elif "开" in normalized and "风" in normalized:
            commands, descs = [1], ["打开风扇"]

    if not commands:
        news_like = any(w in normalized for w in ("习近平", "习近", "总书记", "新闻联播", "人民日报"))
        hint = (
            "识别被新闻语言模型带跑了，请重启唇语服务后再说一次「开风扇」"
            if news_like
            else f"未匹配到家居指令：{original}"
        )
        return {
            "matched": False,
            "text": original,
            "commands": [],
            "descs": [],
            "reply": hint,
        }

    reply = "已执行：" + "、".join(descs)
    return {
        "matched": True,
        "text": original,
        "commands": commands,
        "descs": descs,
        "reply": reply,
        "device_id": HOME_DEVICE_ID,
    }
