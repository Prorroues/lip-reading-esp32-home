import os

OUT = r"F:\reasonix\xiangmu\jiaju\projects\esp32_smart_home\svg_output"

SVGS = {
"05_night": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <rect width="1280" height="720" fill="#FFFFFF"/>
  <text x="80" y="55" font-family="Microsoft YaHei, Arial, sans-serif" font-size="14" fill="#94A3B8">应用场景</text>
  <text x="640" y="180" font-family="Microsoft YaHei, Arial, sans-serif" font-size="48" font-weight="bold" fill="#1E293B" text-anchor="middle">起夜</text>
  <text x="640" y="240" font-family="Microsoft YaHei, Arial, sans-serif" font-size="24" fill="#475569" text-anchor="middle">红外感应到人，自动为你点亮厕所灯</text>
  <rect x="480" y="260" width="320" height="3" rx="1.5" fill="#EA580C"/>
  <rect x="140" y="330" width="280" height="110" rx="12" fill="#FFF7ED"/><text x="280" y="370" font-family="Microsoft YaHei, Arial, sans-serif" font-size="20" font-weight="bold" fill="#EA580C" text-anchor="middle">PIR 人体红外感应</text><text x="280" y="400" font-family="Microsoft YaHei, Arial, sans-serif" font-size="14" fill="#475569" text-anchor="middle">检测到移动 → 触发事件</text><text x="280" y="422" font-family="Arial, sans-serif" font-size="12" fill="#94A3B8" text-anchor="middle">MQTT 发布: esp32/+/presence</text>
  <rect x="500" y="330" width="280" height="110" rx="12" fill="#EFF6FF"/><text x="640" y="370" font-family="Microsoft YaHei, Arial, sans-serif" font-size="20" font-weight="bold" fill="#2563EB" text-anchor="middle">服务端自动处理</text><text x="640" y="400" font-family="Microsoft YaHei, Arial, sans-serif" font-size="14" fill="#475569" text-anchor="middle">收到 presence 消息</text><text x="640" y="422" font-family="Arial, sans-serif" font-size="12" fill="#94A3B8" text-anchor="middle">→ 下发 MQTT 指令 18</text>
  <rect x="860" y="330" width="280" height="110" rx="12" fill="#F0FDF4"/><text x="1000" y="370" font-family="Microsoft YaHei, Arial, sans-serif" font-size="20" font-weight="bold" fill="#16A34A" text-anchor="middle">厕所灯点亮</text><text x="1000" y="400" font-family="Microsoft YaHei, Arial, sans-serif" font-size="14" fill="#475569" text-anchor="middle">ESP32 收到指令 18</text><text x="1000" y="422" font-family="Arial, sans-serif" font-size="12" fill="#94A3B8" text-anchor="middle">GPIO5 高电平 → 灯亮</text>
  <rect x="240" y="490" width="800" height="130" rx="12" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/><text x="640" y="535" font-family="Microsoft YaHei, Arial, sans-serif" font-size="18" fill="#1E293B" text-anchor="middle">PIR 人体红外 → MQTT Broker → FastAPI → WebSocket → Dashboard</text><text x="640" y="565" font-family="Microsoft YaHei, Arial, sans-serif" font-size="15" fill="#475569" text-anchor="middle">红外检测到无人时 → 自动关闭厕所灯，不打扰睡眠</text><text x="640" y="590" font-family="Microsoft YaHei, Arial, sans-serif" font-size="15" fill="#475569" text-anchor="middle">全程无需触摸开关，黑暗中自然完成</text>
  <text x="1220" y="700" font-family="Arial, sans-serif" font-size="11" fill="#94A3B8" text-anchor="end">05 / 18</text>
</svg>""",
}

for name, svg in SVGS.items():
    with open(os.path.join(OUT, f"{name}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"OK: {name}")
