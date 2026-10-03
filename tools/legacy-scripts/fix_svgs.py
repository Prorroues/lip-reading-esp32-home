import glob, os

pages = {
    "02_pain": r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <rect width="1280" height="720" fill="#FFFFFF"/>
  <text x="640" y="80" font-family="Microsoft YaHei, Arial, sans-serif" font-size="36" font-weight="bold" fill="#1E293B" text-anchor="middle">你是否遇到过？</text>
  <rect x="580" y="95" width="120" height="3" rx="1.5" fill="#EA580C"/>
  <rect x="60" y="150" width="360" height="400" rx="16" fill="#FFF7ED" stroke="#FED7AA" stroke-width="1"/><circle cx="240" cy="210" r="40" fill="#EA580C" fill-opacity="0.1"/><text x="240" y="220" font-family="Arial, sans-serif" font-size="36" fill="#EA580C" text-anchor="middle">35°</text><text x="240" y="280" font-family="Microsoft YaHei, Arial, sans-serif" font-size="22" font-weight="bold" fill="#1E293B" text-anchor="middle">夏天回家闷热</text><text x="240" y="330" font-family="Microsoft YaHei, Arial, sans-serif" font-size="16" fill="#475569" text-anchor="middle">进门第一件事</text><text x="240" y="355" font-family="Microsoft YaHei, Arial, sans-serif" font-size="16" fill="#475569" text-anchor="middle">到处找遥控器</text><text x="240" y="380" font-family="Microsoft YaHei, Arial, sans-serif" font-size="16" fill="#475569" text-anchor="middle">等半天才凉下来</text>
  <rect x="460" y="150" width="360" height="400" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/><circle cx="640" cy="210" r="40" fill="#475569" fill-opacity="0.08"/><text x="640" y="220" font-family="Arial, sans-serif" font-size="36" fill="#475569" text-anchor="middle">🔌</text><text x="640" y="280" font-family="Microsoft YaHei, Arial, sans-serif" font-size="22" font-weight="bold" fill="#1E293B" text-anchor="middle">出门忘记关灯</text><text x="640" y="330" font-family="Microsoft YaHei, Arial, sans-serif" font-size="16" fill="#475569" text-anchor="middle">人在外面</text><text x="640" y="355" font-family="Microsoft YaHei, Arial, sans-serif" font-size="16" fill="#475569" text-anchor="middle">灯开了整整一天</text><text x="640" y="380" font-family="Microsoft YaHei, Arial, sans-serif" font-size="16" fill="#475569" text-anchor="middle">心疼电费</text>
  <rect x="860" y="150" width="360" height="400" rx="16" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1"/><circle cx="1040" cy="210" r="40" fill="#2563EB" fill-opacity="0.08"/><text x="1040" y="220" font-family="Arial, sans-serif" font-size="36" fill="#2563EB" text-anchor="middle">❓</text><text x="1040" y="280" font-family="Microsoft YaHei, Arial, sans-serif" font-size="22" font-weight="bold" fill="#1E293B" text-anchor="middle">不知房间状态</text><text x="1040" y="330" font-family="Microsoft YaHei, Arial, sans-serif" font-size="16" fill="#475569" text-anchor="middle">现在温度多少？</text><text x="1040" y="355" font-family="Microsoft YaHei, Arial, sans-serif" font-size="16" fill="#475569" text-anchor="middle">湿度高不高？</text><text x="1040" y="380" font-family="Microsoft YaHei, Arial, sans-serif" font-size="16" fill="#475569" text-anchor="middle">完全不知道</text>
  <text x="640" y="640" font-family="Microsoft YaHei, Arial, sans-serif" font-size="20" fill="#2563EB" text-anchor="middle">这些，都可以改变</text>
  <text x="1220" y="700" font-family="Arial, sans-serif" font-size="11" fill="#94A3B8" text-anchor="end">02 / 18</text>
</svg>''',
    "03_vision": r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <rect width="1280" height="720" fill="#FFFFFF"/>
  <text x="640" y="200" font-family="Microsoft YaHei, Arial, sans-serif" font-size="52" font-weight="bold" fill="#1E293B" text-anchor="middle">一座会感知的房子</text>
  <rect x="520" y="225" width="240" height="3" rx="1.5" fill="#2563EB"/>
  <text x="640" y="290" font-family="Microsoft YaHei, Arial, sans-serif" font-size="22" fill="#475569" text-anchor="middle">15 元 ESP32 芯片，6 类传感器，6 路灯光</text>
  <text x="640" y="325" font-family="Microsoft YaHei, Arial, sans-serif" font-size="22" fill="#475569" text-anchor="middle">感知温湿度 · 自动除湿 · 远程控灯 · 安全告警</text>
  <rect x="140" y="410" width="200" height="100" rx="12" fill="#EFF6FF"/><text x="240" y="450" font-family="Arial, sans-serif" font-size="36" font-weight="bold" fill="#2563EB" text-anchor="middle">15</text><text x="240" y="480" font-family="Microsoft YaHei, Arial, sans-serif" font-size="15" fill="#475569" text-anchor="middle">GPIO 引脚</text>
  <rect x="380" y="410" width="200" height="100" rx="12" fill="#FFF7ED"/><text x="480" y="450" font-family="Arial, sans-serif" font-size="36" font-weight="bold" fill="#EA580C" text-anchor="middle">6</text><text x="480" y="480" font-family="Microsoft YaHei, Arial, sans-serif" font-size="15" fill="#475569" text-anchor="middle">路独立灯光</text>
  <rect x="620" y="410" width="200" height="100" rx="12" fill="#F0FDF4"/><text x="720" y="450" font-family="Arial, sans-serif" font-size="36" font-weight="bold" fill="#16A34A" text-anchor="middle">6</text><text x="720" y="480" font-family="Microsoft YaHei, Arial, sans-serif" font-size="15" fill="#475569" text-anchor="middle">类传感器</text>
  <rect x="860" y="410" width="200" height="100" rx="12" fill="#F8FAFC"/><text x="960" y="450" font-family="Arial, sans-serif" font-size="36" font-weight="bold" fill="#475569" text-anchor="middle">21</text><text x="960" y="480" font-family="Microsoft YaHei, Arial, sans-serif" font-size="15" fill="#475569" text-anchor="middle">条 MQTT 指令</text>
  <text x="640" y="600" font-family="Microsoft YaHei, Arial, sans-serif" font-size="20" fill="#2563EB" text-anchor="middle">纯开源 · 零依赖 · 全栈可控</text>
  <text x="1220" y="700" font-family="Arial, sans-serif" font-size="11" fill="#94A3B8" text-anchor="end">03 / 18</text>
</svg>''',
}

out_dir = r"F:\reasonix\xiangmu\jiaju\projects\esp32_smart_home\svg_output"
for name, content in pages.items():
    path = os.path.join(out_dir, f"{name}.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Written: {name}.svg")
print("Done")
