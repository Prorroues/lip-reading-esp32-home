"""Generate all SVGs with new font sizes (body=28px)."""
import os
DIR = r"F:\reasonix\skill\ppt-master\projects\ppt169_lingmou_v7_ppt169_20260624\svg_output"
BG = "#0A0E17"

# Clean
for f in os.listdir(DIR):
    os.remove(os.path.join(DIR, f))

def w(name, svg):
    path = os.path.join(DIR, name)
    with open(path, "wb") as f:
        f.write(svg.encode("utf-8"))
    print(f"  {name}")

W = 'font-family="\'Microsoft YaHei\',Arial,sans-serif"'
T = 'font-family="\'SimHei\',\'Microsoft YaHei\',Arial,sans-serif"'

# ─── P01 Cover ───
w("01_cover.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".1"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient>
<radialGradient id="g"><stop offset="0%" stop-color="#F59E0B" stop-opacity=".06"/><stop offset="100%" stop-color="#F59E0B" stop-opacity="0"/></radialGradient></defs>
<rect x="0" y="0" width="1280" height="720" fill=\"""" + BG + """\"/>
<rect x="0" y="0" width="1280" height="720" fill="url(#s)"/><rect x="0" y="0" width="1280" height="720" fill="url(#g)"/>
<text x="640" y="320" text-anchor="middle" """ + T + """ font-size="60" font-weight="bold" fill="#F1F5F9">\u7075\u7738\u667a\u8054</text>
<text x="640" y="380" text-anchor="middle" """ + W + """ font-size="28" fill="#94A3B8">\u4f20\u611f\u91c7\u96c6 + AI \u5206\u6790\u7684\u5bb6\u5c45\u786c\u4ef6\u4e92\u8054\u7cfb\u7edf</text>
<text x="640" y="445" text-anchor="middle" """ + W + """ font-size="22" fill="#64748B">ESP32 \u53cc\u677f\u67b6\u6784 \u00b7 MQTT \u4e92\u8054 \u00b7 \u5168\u6808\u81ea\u7814</text>
<text x="640" y="680" text-anchor="middle" """ + W + """ font-size="18" fill="#64748B">ESP32 IoT \u9879\u76ee | 2026 \u5e74 6 \u6708</text>
<text x="1230" y="700" text-anchor="end" """ + W + """ font-size="12" fill="#4B5563">01</text>
</svg>""")

# ─── P02 TOC ───
w("02_toc.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs>
<rect x="0" y="0" width="1280" height="720" fill=\"""" + BG + """\"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>
<text x="640" y="90" text-anchor="middle" """ + T + """ font-size="36" font-weight="bold" fill="#F1F5F9">\u4eca\u5929\u8bb2\u56db\u4ef6\u4e8b</text>
<rect x="120" y="145" width="480" height="110" rx="12" fill="#141B2D" stroke="#0EA5E9" stroke-width="1"/>
<text x="180" y="200" text-anchor="middle" """ + T + """ font-size="28" font-weight="bold" fill="#0EA5E9">01</text>
<text x="225" y="190" """ + T + """ font-size="24" font-weight="bold" fill="#F1F5F9">\u95ee\u9898</text>
<text x="225" y="225" """ + W + """ font-size="20" fill="#94A3B8">\u667a\u80fd\u5bb6\u5c45\u7684\u788e\u7247\u5316\u56f0\u5c40</text>
<rect x="680" y="145" width="480" height="110" rx="12" fill="#141B2D" stroke="#F59E0B" stroke-width="1"/>
<text x="740" y="200" text-anchor="middle" """ + T + """ font-size="28" font-weight="bold" fill="#F59E0B">02</text>
<text x="785" y="190" """ + T + """ font-size="24" font-weight="bold" fill="#F1F5F9">\u65b9\u6848</text>
<text x="785" y="225" """ + W + """ font-size="20" fill="#94A3B8">\u53cc\u677f\u4e00\u4e91</text>
<rect x="120" y="290" width="480" height="110" rx="12" fill="#141B2D" stroke="#22C55E" stroke-width="1"/>
<text x="180" y="345" text-anchor="middle" """ + T + """ font-size="28" font-weight="bold" fill="#22C55E">03</text>
<text x="225" y="335" """ + T + """ font-size="24" font-weight="bold" fill="#F1F5F9">\u9a8c\u8bc1</text>
<text x="225" y="370" """ + W + """ font-size="20" fill="#94A3B8">\u573a\u666f + \u529f\u80fd\u4e00\u89c8</text>
<rect x="680" y="290" width="480" height="110" rx="12" fill="#141B2D" stroke="#06B6D4" stroke-width="1"/>
<text x="740" y="345" text-anchor="middle" """ + T + """ font-size="28" font-weight="bold" fill="#06B6D4">04</text>
<text x="785" y="335" """ + T + """ font-size="24" font-weight="bold" fill="#F1F5F9">\u53cd\u601d</text>
<text x="785" y="370" """ + W + """ font-size="20" fill="#94A3B8">\u603b\u7ed3 + \u4e0b\u4e00\u6b65</text>
<text x="640" y="680" text-anchor="middle" """ + W + """ font-size="18" fill="#64748B">\u7075\u7738\u667a\u8054</text>
<text x="1230" y="700" text-anchor="end" """ + W + """ font-size="12" fill="#4B5563">02</text>
</svg>""")

# ─── P03 Problem ───
w("03_problem.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs>
<rect x="0" y="0" width="1280" height="720" fill=\"""" + BG + """\"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>
<text x="640" y="85" text-anchor="middle" """ + T + """ font-size="36" font-weight="bold" fill="#F1F5F9">\u667a\u80fd\u5bb6\u5c45\u7684\u788e\u7247\u5316\u56f0\u5c40</text>
<rect x="80" y="130" width="520" height="115" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="110" y="170" """ + W + """ font-size="24" font-weight="bold" fill="#EF4444">\u26a0 \u54c1\u724c\u6797\u7acb</text>
<text x="110" y="205" """ + W + """ font-size="18" fill="#94A3B8">5-8\u4e2a\u4e0d\u540cApp\uff0c\u5404\u7ba1\u5404\u7684\u8bbe\u5907</text>
<text x="110" y="233" """ + W + """ font-size="18" fill="#94A3B8">\u4f53\u9a8c\u5272\u88c2\uff0c\u65e0\u7edf\u4e00\u6807\u51c6</text>
<rect x="80" y="265" width="520" height="115" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="110" y="305" """ + W + """ font-size="24" font-weight="bold" fill="#EF4444">\u274c \u5404\u81ea\u4e3a\u653f</text>
<text x="110" y="340" """ + W + """ font-size="18" fill="#94A3B8">\u8bbe\u5907\u95f4\u65e0\u6cd5\u771f\u6b63\u8054\u52a8</text>
<text x="110" y="368" """ + W + """ font-size="18" fill="#94A3B8">\u4e70\u518d\u591a\u4e5f\u662f\u5b64\u5c9b</text>
<rect x="80" y="400" width="520" height="115" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="110" y="440" """ + W + """ font-size="24" font-weight="bold" fill="#EF4444">\u6ca1\u6709\u771f\u667a\u80fd</text>
<text x="110" y="475" """ + W + """ font-size="18" fill="#94A3B8">\u53ea\u662f\u8fdc\u7a0b\u9065\u63a7</text>
<text x="110" y="503" """ + W + """ font-size="18" fill="#94A3B8">\u4e0d\u4f1a\u81ea\u52a8\u8c03\u8282\u548c\u9884\u8b66</text>
<rect x="660" y="130" width="540" height="385" rx="14" fill="#141B2D" stroke="#0EA5E9" stroke-width="1"/>
<text x="690" y="180" """ + T + """ font-size="28" font-weight="bold" fill="#0EA5E9">\u2728 \u6211\u4eec\u7684\u65b9\u6848</text>
<text x="690" y="240" """ + W + """ font-size="22" fill="#F1F5F9">\u2022 15\u5143\u7684ESP32\u82af\u7247\u5c31\u591f\u4e86</text>
<text x="690" y="280" """ + W + """ font-size="22" fill="#F1F5F9">\u2022 \u4e0d\u7528\u88c5App\uff0c\u6d4f\u89c8\u5668\u63a7\u5236</text>
<text x="690" y="320" """ + W + """ font-size="22" fill="#F1F5F9">\u2022 \u4f20\u611f\u5668\u68c0\u6d4b\u5f02\u5e38\u81ea\u52a8\u5904\u7406</text>
<text x="690" y="360" """ + W + """ font-size="22" fill="#F1F5F9">\u2022 AI\u5206\u6790\u8d8b\u52bf\u548c\u5f02\u5e38</text>
<text x="690" y="400" """ + W + """ font-size="22" fill="#F1F5F9">\u2022 \u5168\u6808\u81ea\u7814 \u5f00\u6e90\u53ef\u590d\u7528</text>
<rect x="690" y="455" width="480" height="40" rx="8" fill="#0EA5E9" fill-opacity=".12"/>
<text x="930" y="481" text-anchor="middle" """ + W + """ font-size="20" fill="#0EA5E9">\u2728 \u8fd9\u5c31\u662f\u7075\u7738\u667a\u8054</text>
<text x="1230" y="700" text-anchor="end" """ + W + """ font-size="12" fill="#4B5563">03</text>
</svg>""")

# ─── P04 Architecture ───
w("04_architecture.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient>
<linearGradient id="a"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".15"/><stop offset="100%" stop-color="#06B6D4" stop-opacity=".08"/></linearGradient>
<linearGradient id="b"><stop offset="0%" stop-color="#F59E0B" stop-opacity=".15"/><stop offset="100%" stop-color="#F97316" stop-opacity=".08"/></linearGradient></defs>
<rect x="0" y="0" width="1280" height="720" fill=\"""" + BG + """\"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>
<text x="640" y="80" text-anchor="middle" """ + T + """ font-size="36" font-weight="bold" fill="#F1F5F9">\u53cc\u677f\u786c\u4ef6\u67b6\u6784</text>
<rect x="490" y="320" width="300" height="44" rx="22" fill="#0A0E17" stroke="#0EA5E9" stroke-width="1.5"/>
<text x="640" y="348" text-anchor="middle" """ + W + """ font-size="16" font-weight="bold" fill="#0EA5E9">Mosquitto MQTT Broker</text>
<line x1="490" y1="342" x2="380" y2="260" stroke="#0EA5E9" stroke-opacity=".3" stroke-width="1"/>
<line x1="790" y1="342" x2="900" y2="260" stroke="#F59E0B" stroke-opacity=".3" stroke-width="1"/>
<rect x="220" y="200" width="150" height="60" rx="10" fill="url(#a)" stroke="#0EA5E9" stroke-width="1.5"/>
<text x="295" y="228" text-anchor="middle" """ + W + """ font-size="16" font-weight="bold" fill="#0EA5E9">ESP32 #1</text>
<text x="295" y="250" text-anchor="middle" """ + W + """ font-size="14" fill="#94A3B8">\u4e3b\u63a7\u677f\uff08\u6267\u884c\u5668\uff09</text>
<rect x="910" y="200" width="150" height="60" rx="10" fill="url(#b)" stroke="#F59E0B" stroke-width="1.5"/>
<text x="985" y="228" text-anchor="middle" """ + W + """ font-size="16" font-weight="bold" fill="#F59E0B">ESP32 #2</text>
<text x="985" y="250" text-anchor="middle" """ + W + """ font-size="14" fill="#94A3B8">\u4f20\u611f\u5668\u677f\uff08\u91c7\u96c6\uff09</text>
<rect x="40" y="340" width="150" height="40" rx="8" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="115" y="366" text-anchor="middle" """ + W + """ font-size="15" fill="#F1F5F9">DHT11 \u6e29\u6e7f\u5ea6</text>
<rect x="40" y="395" width="150" height="40" rx="8" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="115" y="421" text-anchor="middle" """ + W + """ font-size="15" fill="#F1F5F9">6\u8def\u706f\u5149</text>
<rect x="40" y="450" width="150" height="40" rx="8" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="115" y="476" text-anchor="middle" """ + W + """ font-size="15" fill="#F1F5F9">RGB + \u98ce\u6247</text>
<rect x="40" y="505" width="150" height="40" rx="8" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="115" y="531" text-anchor="middle" """ + W + """ font-size="15" fill="#F1F5F9">OLED \u663e\u793a</text>
<line x1="250" y1="260" x2="100" y2="330" stroke="#0EA5E9" stroke-opacity=".2" stroke-width="1"/>
<rect x="1090" y="340" width="150" height="40" rx="8" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="1165" y="366" text-anchor="middle" """ + W + """ font-size="15" fill="#F1F5F9">HC-SR04 \u8d85\u58f0</text>
<rect x="1090" y="395" width="150" height="40" rx="8" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="1165" y="421" text-anchor="middle" """ + W + """ font-size="15" fill="#F1F5F9">LM393 \u5149\u654f</text>
<rect x="1090" y="450" width="150" height="40" rx="8" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="1165" y="476" text-anchor="middle" """ + W + """ font-size="15" fill="#F1F5F9">PIR \u4eba\u4f53</text>
<rect x="1090" y="505" width="150" height="40" rx="8" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="1165" y="531" text-anchor="middle" """ + W + """ font-size="15" fill="#F1F5F9">CO2/RFID/\u8235\u673a</text>
<line x1="1030" y1="260" x2="1180" y2="330" stroke="#F59E0B" stroke-opacity=".2" stroke-width="1"/>
<rect x="200" y="590" width="880" height="50" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="345" y="620" text-anchor="middle" """ + W + """ font-size="16" fill="#94A3B8">15 GPIO</text>
<line x1="470" y1="600" x2="470" y2="630" stroke="#1E293B" stroke-width="1"/>
<text x="580" y="620" text-anchor="middle" """ + W + """ font-size="16" fill="#94A3B8">6\u8def\u706f\u5149 + RGB</text>
<line x1="720" y1="600" x2="720" y2="630" stroke="#1E293B" stroke-width="1"/>
<text x="810" y="620" text-anchor="middle" """ + W + """ font-size="16" fill="#94A3B8">6\u7c7b\u4f20\u611f\u5668</text>
<line x1="910" y1="600" x2="910" y2="630" stroke="#1E293B" stroke-width="1"/>
<text x="1000" y="620" text-anchor="middle" """ + W + """ font-size="16" fill="#94A3B8">21\u6761MQTT</text>
<text x="1230" y="700" text-anchor="end" """ + W + """ font-size="12" fill="#4B5563">04</text>
</svg>""")

# ─── P05 Software Stack ───
w("05_software.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs>
<rect x="0" y="0" width="1280" height="720" fill=\"""" + BG + """\"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>
<text x="640" y="80" text-anchor="middle" """ + T + """ font-size="36" font-weight="bold" fill="#F1F5F9">\u5168\u6808\u8f6f\u4ef6\u67b6\u6784</text>
<rect x="160" y="140" width="960" height="60" rx="10" fill="#0EA5E9" fill-opacity=".1" stroke="#0EA5E9" stroke-width="1"/>
<text x="190" y="178" """ + T + """ font-size="20" font-weight="bold" fill="#0EA5E9">\u4ea4\u4e92\u5c42</text>
<text x="300" y="178" """ + W + """ font-size="18" fill="#F1F5F9">Web Dashboard \u00b7 \u7eafHTML/CSS/JS</text>
<rect x="160" y="215" width="960" height="60" rx="10" fill="#06B6D4" fill-opacity=".1" stroke="#06B6D4" stroke-width="1"/>
<text x="190" y="253" """ + T + """ font-size="20" font-weight="bold" fill="#06B6D4">API\u5c42</text>
<text x="300" y="253" """ + W + """ font-size="18" fill="#F1F5F9">FastAPI REST \u00b7 /api/device /telemetry /command /ai_report</text>
<rect x="160" y="290" width="960" height="60" rx="10" fill="#141B2D" stroke="#F59E0B" stroke-width="1"/>
<text x="190" y="328" """ + T + """ font-size="20" font-weight="bold" fill="#F59E0B">\u901a\u4fe1\u5c42</text>
<text x="300" y="328" """ + W + """ font-size="18" fill="#F1F5F9">MQTT (mosquitto :1883) \u00b7 paho-mqtt \u00b7 QOS0</text>
<rect x="160" y="365" width="960" height="60" rx="10" fill="#22C55E" fill-opacity=".1" stroke="#22C55E" stroke-width="1"/>
<text x="190" y="403" """ + T + """ font-size="20" font-weight="bold" fill="#22C55E">\u6570\u636e\u5c42</text>
<text x="300" y="403" """ + W + """ font-size="18" fill="#F1F5F9">SQLite 6\u8868 \u00b7 aiosqlite \u00b7 CSV\u5bfc\u51fa</text>
<rect x="160" y="440" width="960" height="60" rx="10" fill="#EF4444" fill-opacity=".1" stroke="#EF4444" stroke-width="1"/>
<text x="190" y="478" """ + T + """ font-size="20" font-weight="bold" fill="#EF4444">AI\u5c42</text>
<text x="300" y="478" """ + W + """ font-size="18" fill="#F1F5F9">\u5f02\u5e38\u68c0\u6d4b \u00b7 \u8d8b\u52bf\u9884\u6d4b \u00b7 \u81ea\u52a8\u544a\u8b66 \u00b7 \u805a\u5408</text>
<rect x="160" y="530" width="960" height="60" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="640" y="558" text-anchor="middle" """ + W + """ font-size="16" font-weight="bold" fill="#94A3B8">\u6570\u636e\u6d41</text>
<text x="640" y="582" text-anchor="middle" """ + W + """ font-size="16" fill="#F1F5F9">ESP32 -> MQTT -> FastAPI -> SQLite + WebSocket -> Dashboard</text>
<rect x="200" y="610" width="170" height="30" rx="8" fill="#141B2D" stroke="#0EA5E9" stroke-width=".5"/>
<text x="285" y="630" text-anchor="middle" """ + W + """ font-size="14" fill="#0EA5E9">uvicorn</text>
<rect x="390" y="610" width="150" height="30" rx="8" fill="#141B2D" stroke="#F59E0B" stroke-width=".5"/>
<text x="465" y="630" text-anchor="middle" """ + W + """ font-size="14" fill="#F59E0B">paho-mqtt</text>
<rect x="560" y="610" width="120" height="30" rx="8" fill="#141B2D" stroke="#22C55E" stroke-width=".5"/>
<text x="620" y="630" text-anchor="middle" """ + W + """ font-size="14" fill="#22C55E">aiosqlite</text>
<rect x="700" y="610" width="150" height="30" rx="8" fill="#141B2D" stroke="#06B6D4" stroke-width=".5"/>
<text x="775" y="630" text-anchor="middle" """ + W + """ font-size="14" fill="#06B6D4">WebSocket</text>
<rect x="870" y="610" width="150" height="30" rx="8" fill="#141B2D" stroke="#EF4444" stroke-width=".5"/>
<text x="945" y="630" text-anchor="middle" """ + W + """ font-size="14" fill="#EF4444">AI\u68c0\u6d4b</text>
<text x="1230" y="700" text-anchor="end" """ + W + """ font-size="12" fill="#4B5563">05</text>
</svg>""")

# ─── P06 Data Pipeline ───
w("06_datapipeline.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient>
<linearGradient id="p" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0EA5E9"/><stop offset=".33" stop-color="#06B6D4"/><stop offset=".66" stop-color="#22C55E"/><stop offset="1" stop-color="#F59E0B"/></linearGradient></defs>
<rect x="0" y="0" width="1280" height="720" fill=\"""" + BG + """\"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>
<text x="640" y="80" text-anchor="middle" """ + T + """ font-size="36" font-weight="bold" fill="#F1F5F9">\u6570\u636e\u6d41\u7ba1\u9053\uff08\u4e0a\uff09</text>
<rect x="80" y="140" width="1120" height="4" rx="2" fill="url(#p)" opacity=".5"/>
<g """ + W + """>
<rect x="60" y="175" width="350" height="310" rx="14" fill="#141B2D" stroke="#0EA5E9" stroke-width="1"/>
<text x="235" y="220" text-anchor="middle" """ + T + """ font-size="28" font-weight="bold" fill="#0EA5E9">01 \u611f\u77e5</text>
<text x="80" y="265" font-size="20" fill="#94A3B8">\u2022 DHT11 \u6e29\u6e7f\u5ea6\uff08GPIO27\uff09</text>
<text x="80" y="300" font-size="20" fill="#94A3B8">\u2022 LM393 \u5149\u654f\uff08ADC 0-4095\uff09</text>
<text x="80" y="335" font-size="20" fill="#94A3B8">\u2022 PIR \u4eba\u4f53\u7ea2\u5916\uff08GPIO4\uff09</text>
<text x="80" y="370" font-size="20" fill="#94A3B8">\u2022 HC-SR04 \u8d85\u58f0\uff082cm-4m\uff09</text>
<text x="80" y="405" font-size="20" fill="#94A3B8">\u2022 SCD41 CO2\uff08I2C\uff09</text>
<text x="80" y="440" font-size="20" fill="#94A3B8">\u2022 RC522 RFID + SG90 \u8235\u673a</text>
<text x="235" y="475" text-anchor="middle" font-size="16" fill="#64748B">ESP32#2 \u91c7\u96c6</text>

<rect x="450" y="175" width="350" height="310" rx="14" fill="#141B2D" stroke="#06B6D4" stroke-width="1"/>
<text x="625" y="220" text-anchor="middle" """ + T + """ font-size="28" font-weight="bold" fill="#06B6D4">02 \u4f20\u8f93</text>
<text x="470" y="265" font-size="20" fill="#94A3B8">\u2022 WiFi 2.4GHz</text>
<text x="470" y="300" font-size="20" fill="#94A3B8">\u2022 MQTT \u534f\u8bae</text>
<text x="470" y="335" font-size="20" fill="#94A3B8">\u2022 mosquitto Broker</text>
<text x="470" y="370" font-size="20" fill="#94A3B8">\u2022 paho-mqtt \u5ba2\u6237\u7aef</text>
<text x="470" y="405" font-size="20" fill="#94A3B8">\u2022 8\u6761\u4e3b\u9898 \u53cc\u5411\u901a\u4fe1</text>
<text x="625" y="475" text-anchor="middle" font-size="16" fill="#64748B">MQTT Broker (:1883)</text>

<rect x="840" y="175" width="380" height="310" rx="14" fill="#141B2D" stroke="#22C55E" stroke-width="1"/>
<text x="1030" y="220" text-anchor="middle" """ + T + """ font-size="28" font-weight="bold" fill="#22C55E">03 \u5b58\u50a8</text>
<text x="860" y="265" font-size="20" fill="#94A3B8">\u2022 SQLite 6\u8868</text>
<text x="860" y="300" font-size="20" fill="#94A3B8">\u2022 FastAPI \u5199\u5165</text>
<text x="860" y="335" font-size="20" fill="#94A3B8">\u2022 aiosqlite \u5f02\u6b65</text>
<text x="860" y="370" font-size="20" fill="#94A3B8">\u2022 CSV \u5907\u4efd\u5bfc\u51fa</text>
<text x="860" y="405" font-size="20" fill="#94A3B8">\u2022 UPSERT \u53bb\u91cd</text>
<text x="1030" y="475" text-anchor="middle" font-size="16" fill="#64748B">\u6301\u4e45\u5316</text>
</g>
<rect x="80" y="520" width="1120" height="4" rx="2" fill="url(#p)" opacity=".5"/>
<text x="640" y="570" text-anchor="middle" """ + W + """ font-size="20" fill="#94A3B8">ESP32#2 -> MQTT -> FastAPI -> SQLite</text>
<text x="1230" y="700" text-anchor="end" """ + W + """ font-size="12" fill="#4B5563">06</text>
</svg>""")

# ─── P07 Data Pipeline (lower) ───
w("07_datapipeline2.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient>
<linearGradient id="p" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F59E0B"/><stop offset="1" stop-color="#EF4444"/></linearGradient></defs>
<rect x="0" y="0" width="1280" height="720" fill=\"""" + BG + """\"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>
<text x="640" y="80" text-anchor="middle" """ + T + """ font-size="36" font-weight="bold" fill="#F1F5F9">\u6570\u636e\u6d41\u7ba1\u9053\uff08\u4e0b\uff09</text>
<rect x="80" y="140" width="1120" height="4" rx="2" fill="url(#p)" opacity=".5"/>
<g """ + W + """>
<rect x="140" y="175" width="450" height="310" rx="14" fill="#141B2D" stroke="#F59E0B" stroke-width="1"/>
<text x="365" y="220" text-anchor="middle" """ + T + """ font-size="28" font-weight="bold" fill="#F59E0B">04 \u5206\u6790</text>
<text x="160" y="265" font-size="20" fill="#94A3B8">\u2022 AI \u5f02\u5e38\u68c0\u6d4b</text>
<text x="160" y="300" font-size="20" fill="#94A3B8">\u2022 \u8d8b\u52bf\u9884\u6d4b</text>
<text x="160" y="335" font-size="20" fill="#94A3B8">\u2022 \u5747\u503c/\u65b9\u5dee\u7edf\u8ba1</text>
<text x="160" y="370" font-size="20" fill="#94A3B8">\u2022 \u8d85\u9608\u503c\u544a\u8b66</text>
<text x="160" y="405" font-size="20" fill="#94A3B8">\u2022 \u6bcf\u5c0f\u65f6\u805a\u5408</text>
<text x="160" y="440" font-size="20" fill="#94A3B8">\u2022 GET /api/ai_report</text>
<text x="365" y="475" text-anchor="middle" font-size="16" fill="#64748B">\u672c\u5730AI\u5f15\u64ce</text>

<rect x="650" y="175" width="500" height="310" rx="14" fill="#141B2D" stroke="#EF4444" stroke-width="1"/>
<text x="900" y="220" text-anchor="middle" """ + T + """ font-size="28" font-weight="bold" fill="#EF4444">05 \u8054\u52a8</text>
<text x="670" y="265" font-size="20" fill="#94A3B8">\u2022 \u6e7f\u5ea6\u9ad8 -> \u98ce\u6247\u81ea\u52a8\u5f00\u542f</text>
<text x="670" y="300" font-size="20" fill="#94A3B8">\u2022 PIR\u611f\u5e94 -> \u706f\u5149\u81ea\u52a8\u4eae\u706d</text>
<text x="670" y="335" font-size="20" fill="#94A3B8">\u2022 \u5149\u654f\u6697 -> \u8865\u5149</text>
<text x="670" y="370" font-size="20" fill="#94A3B8">\u2022 CO2\u9ad8 -> \u6392\u98ce</text>
<text x="670" y="405" font-size="20" fill="#94A3B8">\u2022 \u8d85\u58f0\u8fd1 -> \u544a\u8b66</text>
<text x="670" y="440" font-size="20" fill="#94A3B8">\u2022 WebSocket -> Dashboard\u5f39\u7a97</text>
<text x="900" y="475" text-anchor="middle" font-size="16" fill="#64748B">\u5168\u81ea\u52a8\u54cd\u5e94</text>
</g>
<rect x="80" y="520" width="1120" height="4" rx="2" fill="url(#p)" opacity=".5"/>
<text x="640" y="570" text-anchor="middle" """ + W + """ font-size="20" fill="#94A3B8">AI\u5206\u6790 -> \u8054\u52a8 -> WebSocket -> Dashboard/\u6267\u884c</text>
<text x="1230" y="700" text-anchor="end" """ + W + """ font-size="12" fill="#4B5563">07</text>
</svg>""")

w("08_scene1.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs>
<rect x="0" y="0" width="1280" height="720" fill=\"""" + BG + """\"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>
<text x="640" y="80" text-anchor="middle" """ + T + """ font-size="36" font-weight="bold" fill="#F1F5F9">\u573a\u666f\u4e00\uff1a\u6e29\u6e7f\u5ea6\u9664\u6e7f + 6\u533a\u706f\u5149</text>
<rect x="60" y="130" width="560" height="520" rx="14" fill="#141B2D" stroke="#1E293B"/>
<rect x="60" y="130" width="560" height="50" rx="14" fill="#0EA5E9" fill-opacity=".08"/>
<text x="80" y="163" """ + T + """ font-size="22" font-weight="bold" fill="#0EA5E9">\u6e29\u6e7f\u5ea6 + \u98ce\u6247\u81ea\u52a8</text>
<rect x="80" y="200" width="520" height="130" rx="10" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="100" y="235" """ + W + """ font-size="22" font-weight="bold" fill="#F1F5F9">DHT11 \u6e29\u6e7f\u5ea6\u4f20\u611f\u5668</text>
<text x="100" y="270" """ + W + """ font-size="18" fill="#94A3B8">GPIO27 \u00b7 1s\u91c7\u96c6 \u00b7 \u72ec\u7acb\u7ebf\u7a0b</text>
<text x="100" y="300" """ + W + """ font-size="18" fill="#94A3B8">2.5s\u8d85\u65f6\u4fdd\u62a4 \u00b7 \u5931\u8d25\u6cbf\u7528\u4e0a\u6b21\u503c</text>
<rect x="80" y="350" width="520" height="150" rx="10" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="100" y="385" """ + W + """ font-size="22" font-weight="bold" fill="#F1F5F9">\u98ce\u6247\u81ea\u52a8\u63a7\u5236\u903b\u8f91</text>
<text x="100" y="420" """ + W + """ font-size="18" fill="#94A3B8">\u6e7f\u5ea6 85% \u4ee5\u4e0a -> \u98ce\u6247\u81ea\u52a8\u5f00\u542f\u9664\u6e7f</text>
<text x="100" y="450" """ + W + """ font-size="18" fill="#94A3B8">\u6e7f\u5ea6 82% \u4ee5\u4e0b -> \u98ce\u6247\u81ea\u52a8\u5173\u95ed</text>
<rect x="100" y="475" width="80" height="20" rx="6" fill="#0EA5E9" fill-opacity=".12"/>
<text x="140" y="490" text-anchor="middle" """ + W + """ font-size="13" fill="#0EA5E9">\u6ede\u56de3%\u9632\u6296</text>
<rect x="660" y="130" width="560" height="520" rx="14" fill="#141B2D" stroke="#1E293B"/>
<rect x="660" y="130" width="560" height="50" rx="14" fill="#F59E0B" fill-opacity=".08"/>
<text x="680" y="163" """ + T + """ font-size="22" font-weight="bold" fill="#F59E0B">6\u8def\u706f\u5149 + RGB</text>
<g """ + W + """ font-size="18">
<rect x="680" y="200" width="250" height="36" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="700" y="224" fill="#94A3B8">\u67dc\u5b50\u706f GPIO15</text>
<rect x="950" y="200" width="250" height="36" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="970" y="224" fill="#94A3B8">\u5e8a\u540e\u706f GPIO2</text>
<rect x="680" y="250" width="250" height="36" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="700" y="274" fill="#94A3B8">\u5e8a\u4e0b\u524d\u706f GPIO4</text>
<rect x="950" y="250" width="250" height="36" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="970" y="274" fill="#94A3B8">\u5e8a\u5934\u706f GPIO18</text>
<rect x="680" y="300" width="250" height="36" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="700" y="324" fill="#94A3B8">\u4e0a\u5de6\u706f GPIO19</text>
<rect x="950" y="300" width="250" height="36" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="970" y="324" fill="#94A3B8">\u53a5\u6240\u706f GPIO5</text>
</g>
<rect x="680" y="360" width="520" height="120" rx="10" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="700" y="395" """ + W + """ font-size="20" font-weight="bold" fill="#F1F5F9">RGB PWM \u8c03\u5149</text>
<text x="700" y="430" """ + W + """ font-size="18" fill="#94A3B8">R:GPIO26 G:GPIO25 B:GPIO33</text>
<text x="700" y="460" """ + W + """ font-size="18" fill="#94A3B8">0-1023\u8c03\u5149 \u00b7 \u6696\u8272/\u5173\u95ed/\u81ea\u52a8</text>
<rect x="680" y="500" width="520" height="80" rx="10" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="700" y="530" """ + W + """ font-size="18" font-weight="bold" fill="#94A3B8">MQTT 21\u6761\u6307\u4ee4</text>
<text x="700" y="560" """ + W + """ font-size="16" fill="#64748B">1-4:\u98ce\u6247 5:\u6e29\u6e7f\u5ea6 6-7:RGB 8-19:6\u8def\u706f 20-21:\u81ea\u52a8</text>
<text x="1230" y="700" text-anchor="end" """ + W + """ font-size="12" fill="#4B5563">08</text>
</svg>""")

w("09_scene2.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
<defs><radialGradient id="s"><stop offset="0%" stop-color="#F59E0B" stop-opacity=".06"/><stop offset="100%" stop-color="#F59E0B" stop-opacity="0"/></radialGradient></defs>
<rect x="0" y="0" width="1280" height="720" fill=\"""" + BG + """\"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>
<text x="640" y="80" text-anchor="middle" """ + T + """ font-size="36" font-weight="bold" fill="#F1F5F9">\u573a\u666f\u4e8c\uff1a\u4f20\u611f\u5668 + RFID + AI</text>
<rect x="60" y="130" width="560" height="520" rx="14" fill="#141B2D" stroke="#1E293B"/>
<rect x="60" y="130" width="560" height="50" rx="14" fill="#F59E0B" fill-opacity=".08"/>
<text x="80" y="163" """ + T + """ font-size="22" font-weight="bold" fill="#F59E0B">\u591a\u4f20\u611f\u5668\u534f\u540c\u5de1\u68c0</text>
<g """ + W + """>
<rect x="80" y="200" width="245" height="70" rx="10" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="100" y="230" font-size="18" font-weight="bold" fill="#F1F5F9">HC-SR04 \u8d85\u58f0</text>
<text x="100" y="258" font-size="16" fill="#94A3B8">TRIG:17 ECHO:34</text>
<rect x="355" y="200" width="245" height="70" rx="10" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="375" y="230" font-size="18" font-weight="bold" fill="#F1F5F9">LM393 \u5149\u654f</text>
<text x="375" y="258" font-size="16" fill="#94A3B8">ADC 0-4095</text>
<rect x="80" y="290" width="245" height="70" rx="10" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="100" y="320" font-size="18" font-weight="bold" fill="#F1F5F9">PIR \u4eba\u4f53\u7ea2\u5916</text>
<text x="100" y="348" font-size="16" fill="#94A3B8">GPIO4</text>
<rect x="355" y="290" width="245" height="70" rx="10" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="375" y="320" font-size="18" font-weight="bold" fill="#F1F5F9">SCD41 CO2</text>
<text x="375" y="348" font-size="16" fill="#94A3B8">I2C 400-5000ppm</text>
<rect x="80" y="380" width="245" height="70" rx="10" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="100" y="410" font-size="18" font-weight="bold" fill="#F1F5F9">RC522 RFID</text>
<text x="100" y="438" font-size="16" fill="#94A3B8">SPI \u5237\u5361\u5f00\u95e8</text>
<rect x="355" y="380" width="245" height="70" rx="10" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="375" y="410" font-size="18" font-weight="bold" fill="#F1F5F9">SG90 \u8235\u673a</text>
<text x="375" y="438" font-size="16" fill="#94A3B8">PWM \u81ea\u52a8\u5173\u95e8</text>
<rect x="80" y="475" width="520" height="80" rx="10" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="100" y="505" font-size="18" font-weight="bold" fill="#94A3B8">\u8054\u52a8\u89c4\u5219</text>
<text x="100" y="535" font-size="16" fill="#64748B">CO2\u9ad8->\u6392\u98ce | \u5149\u654f\u6697->\u5f00\u706f | \u8d85\u58f0\u8fd1->\u544a\u8b66</text>
</g>
<rect x="660" y="130" width="560" height="520" rx="14" fill="#141B2D" stroke="#1E293B"/>
<rect x="660" y="130" width="560" height="50" rx="14" fill="#EF4444" fill-opacity=".08"/>
<text x="680" y="163" """ + T + """ font-size="22" font-weight="bold" fill="#EF4444">RFID + AI \u73af\u5883\u65e5\u62a5</text>
<g """ + W + """>
<rect x="680" y="200" width="520" height="110" rx="10" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="700" y="235" font-size="20" font-weight="bold" fill="#F1F5F9">RFID \u5237\u5361\u5f00\u95e8\u6d41\u7a0b</text>
<text x="700" y="270" font-size="18" fill="#94A3B8">\u8bfb\u53d6UID -> \u8235\u673a\u5f00\u95e8 -> 3s\u81ea\u52a8\u5173\u95e8</text>
<text x="700" y="300" font-size="16" fill="#64748B">SQLite rfid_log \u8bb0\u5f55\u6bcf\u6b21\u5237\u5361</text>
<rect x="680" y="335" width="520" height="110" rx="10" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="700" y="370" font-size="20" font-weight="bold" fill="#F1F5F9">AI \u73af\u5883\u5206\u6790</text>
<text x="700" y="405" font-size="18" fill="#94A3B8">\u6bcf\u5c0f\u65f6\u5206\u6790\u4f20\u611f\u5668\u6570\u636e</text>
<text x="700" y="435" font-size="16" fill="#64748B">\u5747\u503c/\u65b9\u5dee/\u5f02\u5e38\u6807\u6ce8 \u00b7 API\u5bfc\u51fa</text>
<rect x="680" y="470" width="520" height="110" rx="10" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>
<text x="700" y="505" font-size="20" font-weight="bold" fill="#F1F5F9">\u5b9e\u65f6\u544a\u8b66\u63a8\u9001</text>
<text x="700" y="540" font-size="18" fill="#94A3B8">\u5f02\u5e38 -> WebSocket -> Dashboard \u5f39\u7a97</text>
<text x="700" y="570" font-size="16" fill="#64748B">\u9608\u503c: \u6e29\u5ea6>35\u00b0C \u6e7f\u5ea6>95% CO2>2000ppm</text>
</g>
<text x="1230" y="700" text-anchor="end" """ + W + """ font-size="12" fill="#4B5563">09</text>
</svg>""")

w("10_features.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs>
<rect x="0" y="0" width="1280" height="720" fill=\"""" + BG + """\"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>
<text x="640" y="80" text-anchor="middle" """ + T + """ font-size="36" font-weight="bold" fill="#F1F5F9">10 \u9879\u6838\u5fc3\u80fd\u529b</text>
<g """ + W + """>
<rect x="60" y="135" width="360" height="115" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="80" y="172" font-size="18" font-weight="bold" fill="#0EA5E9">\u6e29\u6e7f\u5ea6\u76d1\u6d4b</text>
<text x="80" y="205" font-size="16" fill="#94A3B8">DHT11 \u00b7 1s\u91c7\u96c6</text>
<text x="80" y="235" font-size="15" fill="#64748B">GPIO27 \u00b7 \u00b12\u00b0C</text>
<rect x="460" y="135" width="360" height="115" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="480" y="172" font-size="18" font-weight="bold" fill="#F59E0B">6\u8def\u706f\u5149</text>
<text x="480" y="205" font-size="16" fill="#94A3B8">\u72ec\u7acbGPIO\u63a7\u5236</text>
<text x="480" y="235" font-size="15" fill="#64748B">\u6307\u4ee48-19</text>
<rect x="860" y="135" width="360" height="115" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="880" y="172" font-size="18" font-weight="bold" fill="#06B6D4">RGB\u8c03\u5149</text>
<text x="880" y="205" font-size="16" fill="#94A3B8">PWM 0-1023</text>
<text x="880" y="235" font-size="15" fill="#64748B">R26/G25/B33</text>
<rect x="60" y="275" width="360" height="115" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="80" y="312" font-size="18" font-weight="bold" fill="#0EA5E9">\u6e7f\u5ea6\u8054\u52a8\u98ce\u6247</text>
<text x="80" y="345" font-size="16" fill="#94A3B8">\u81ea\u52a8\u5f00\u5173</text>
<text x="80" y="375" font-size="15" fill="#64748B">\u6ede\u56de3%\u9632\u6296</text>
<rect x="460" y="275" width="360" height="115" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="480" y="312" font-size="18" font-weight="bold" fill="#F59E0B">\u591a\u4f20\u611f\u5668</text>
<text x="480" y="345" font-size="16" fill="#94A3B8">\u8d85\u58f0/\u5149\u654f/PIR/CO2</text>
<text x="480" y="375" font-size="15" fill="#64748B">1s\u91c7\u96c6\u5468\u671f</text>
<rect x="860" y="275" width="360" height="115" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="880" y="312" font-size="18" font-weight="bold" fill="#22C55E">RFID+\u8235\u673a</text>
<text x="880" y="345" font-size="16" fill="#94A3B8">\u5f00\u95e8 3s\u81ea\u52a8\u5173</text>
<text x="880" y="375" font-size="15" fill="#64748B">\u8bb0\u5f55\u53ef\u8ffd\u6eaf</text>
<rect x="60" y="415" width="360" height="115" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="80" y="452" font-size="18" font-weight="bold" fill="#EF4444">AI\u5206\u6790</text>
<text x="80" y="485" font-size="16" fill="#94A3B8">\u5f02\u5e38\u68c0\u6d4b+\u9884\u6d4b</text>
<text x="80" y="505" font-size="15" fill="#64748B">\u6bcf\u5c0f\u65f6\u805a\u5408</text>
<rect x="460" y="415" width="360" height="115" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="480" y="452" font-size="18" font-weight="bold" fill="#0EA5E9">\u6570\u636e\u6301\u4e45\u5316</text>
<text x="480" y="485" font-size="16" fill="#94A3B8">SQLite 6\u8868 CSV</text>
<text x="480" y="505" font-size="15" fill="#64748B">\u6beb\u79d2\u7ea7\u5199\u5165</text>
<rect x="860" y="415" width="360" height="115" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="880" y="452" font-size="18" font-weight="bold" fill="#22C55E">\u5b9e\u65f6\u63a8\u9001</text>
<text x="880" y="485" font-size="16" fill="#94A3B8">WebSocket\u53cc\u5411</text>
<text x="880" y="505" font-size="15" fill="#64748B">\u65e0\u5237\u65b0</text>
</g>
<text x="1230" y="700" text-anchor="end" """ + W + """ font-size="12" fill="#4B5563">10</text>
</svg>""")

# P11 Summary upper
w("11_summary1.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs>
<rect x="0" y="0" width="1280" height="720" fill=\"""" + BG + """\"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>
<text x="640" y="80" text-anchor="middle" """ + T + """ font-size="36" font-weight="bold" fill="#F1F5F9">\u603b\u7ed3\uff08\u4e0a\uff09</text>
<rect x="60" y="130" width="560" height="260" rx="14" fill="#141B2D" stroke="#0EA5E9" stroke-width="1"/>
<text x="90" y="175" """ + T + """ font-size="24" font-weight="bold" fill="#0EA5E9">\u505a\u4e86\u4ec0\u4e48</text>
<text x="90" y="215" """ + W + """ font-size="20" fill="#F1F5F9">\u2022 \u53ccESP32\u786c\u4ef6\u67b6\u6784 + MQTT\u4e92\u8054</text>
<text x="90" y="250" """ + W + """ font-size="20" fill="#F1F5F9">\u2022 FastAPI\u5168\u6808 + SQLite\u6301\u4e45\u5316</text>
<text x="90" y="285" """ + W + """ font-size="20" fill="#F1F5F9">\u2022 Web Dashboard + AI\u5f02\u5e38\u68c0\u6d4b</text>
<text x="90" y="320" """ + W + """ font-size="20" fill="#F1F5F9">\u2022 7\u5927\u81ea\u52a8\u8054\u52a8\u573a\u666f</text>
<text x="90" y="355" """ + W + """ font-size="20" fill="#F1F5F9">\u2022 \u53cc\u677f\u540f\u5354 + \u5168\u6808\u81ea\u7814</text>
<rect x="660" y="130" width="560" height="260" rx="14" fill="#141B2D" stroke="#F59E0B" stroke-width="1"/>
<text x="690" y="175" """ + T + """ font-size="24" font-weight="bold" fill="#F59E0B">\u5b66\u5230\u4e86\u4ec0\u4e48</text>
<text x="690" y="215" """ + W + """ font-size="20" fill="#F1F5F9">\u2022 MicroPython\u5d4c\u5165\u5f0f + GPIO\u63a7\u5236</text>
<text x="690" y="250" """ + W + """ font-size="20" fill="#F1F5F9">\u2022 MQTT\u7269\u8054\u7f51\u901a\u4fe1\u534f\u8bae</text>
<text x="690" y="285" """ + W + """ font-size="20" fill="#F1F5F9">\u2022 FastAPI + WebSocket\u5168\u6808</text>
<text x="690" y="320" """ + W + """ font-size="20" fill="#F1F5F9">\u2022 SQLite + AI\u6570\u636e\u5206\u6790</text>
<text x="690" y="355" """ + W + """ font-size="20" fill="#F1F5F9">\u2022 \u786c\u4ef6\u8c03\u8bd5 + \u6392\u9519\u80fd\u529b</text>
<text x="1230" y="700" text-anchor="end" """ + W + """ font-size="12" fill="#4B5563">11</text>
</svg>""")

# P12 Summary lower
w("12_summary2.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs>
<rect x="0" y="0" width="1280" height="720" fill=\"""" + BG + """\"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>
<text x="640" y="80" text-anchor="middle" """ + T + """ font-size="36" font-weight="bold" fill="#F1F5F9">\u603b\u7ed3\uff08\u4e0b\uff09</text>
<rect x="60" y="130" width="560" height="240" rx="14" fill="#141B2D" stroke="#22C55E" stroke-width="1"/>
<text x="90" y="175" """ + T + """ font-size="24" font-weight="bold" fill="#22C55E">\u4e0b\u4e00\u6b65\u6539\u8fdb</text>
<text x="90" y="215" """ + W + """ font-size="20" fill="#94A3B8">\u2022 App\u8fdc\u7a0b\u63a7\u5236</text>
<text x="90" y="250" """ + W + """ font-size="20" fill="#94A3B8">\u2022 \u8bed\u97f3\u63a7\u5236\uff08\u5c0f\u7231/\u5929\u732b\uff09</text>
<text x="90" y="285" """ + W + """ font-size="20" fill="#94A3B8">\u2022 \u4f20\u611f\u5668\u677f\u786c\u4ef6\u5b8c\u6574\u6fc0\u6d3b</text>
<text x="90" y="320" """ + W + """ font-size="20" fill="#94A3B8">\u2022 \u516c\u7f51IoT\u5e73\u53f0\u63a5\u5165</text>
<text x="90" y="355" """ + W + """ font-size="20" fill="#94A3B8">\u2022 \u5b9a\u65f6\u573a\u666f + \u5730\u7406\u4f4d\u7f6e\u89e6\u53d1</text>
<rect x="660" y="130" width="560" height="240" rx="14" fill="#141B2D" stroke="#06B6D4" stroke-width="1"/>
<text x="690" y="175" """ + T + """ font-size="24" font-weight="bold" fill="#06B6D4">\u9879\u76ee\u7279\u8272</text>
<text x="690" y="215" """ + W + """ font-size="20" fill="#F1F5F9">\u2022 \u5168\u6808\u81ea\u7814 \u00b7 MIT License</text>
<text x="690" y="250" """ + W + """ font-size="20" fill="#F1F5F9">\u2022 \u6781\u4f4e\u6210\u672c\uff08\u5168\u5957\u767e\u5143\u5185\uff09</text>
<text x="690" y="285" """ + W + """ font-size="20" fill="#F1F5F9">\u2022 \u96f6\u4f9d\u8d56\u524d\u7aef \u7eafHTML/CSS/JS</text>
<text x="690" y="320" """ + W + """ font-size="20" fill="#F1F5F9">\u2022 \u4ece\u786c\u4ef6\u5230AI\u5168\u94fe\u8def\u81ea\u63a7</text>
<text x="690" y="355" """ + W + """ font-size="20" fill="#F1F5F9">\u2022 \u53ef\u6f14\u793a\u3001\u53ef\u62d3\u5c55\u3001\u53ef\u590d\u7528</text>
<rect x="180" y="410" width="920" height="60" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>
<text x="640" y="440" text-anchor="middle" """ + T + """ font-size="20" font-weight="bold" fill="#94A3B8">\u5f53\u524d\u7248\u672c\uff1av1.0 -> v1.5 \u8fc7\u6e21\u4e2d</text>
<text x="640" y="462" text-anchor="middle" """ + W + """ font-size="16" fill="#64748B">v0.1\u5355\u677f -> v0.5\u53cc\u677f -> v1.0\u5168\u5c4b -> v1.5\u8054\u52a8</text>
<text x="1230" y="700" text-anchor="end" """ + W + """ font-size="12" fill="#4B5563">12</text>
</svg>""")

# P13 Thanks
w("13_thanks.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".1"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient>
<radialGradient id="g"><stop offset="0%" stop-color="#F59E0B" stop-opacity=".05"/><stop offset="100%" stop-color="#F59E0B" stop-opacity="0"/></radialGradient></defs>
<rect x="0" y="0" width="1280" height="720" fill=\"""" + BG + """\"/>
<rect x="0" y="0" width="1280" height="720" fill="url(#s)"/><rect x="0" y="0" width="1280" height="720" fill="url(#g)"/>
<text x="640" y="340" text-anchor="middle" """ + T + """ font-size="60" font-weight="bold" fill="#F1F5F9">\u8c22\u8c22</text>
<text x="640" y="400" text-anchor="middle" """ + W + """ font-size="28" fill="#94A3B8">\u7075\u7738\u667a\u8054 \u2014 \u8ba9\u5bb6\u771f\u7684\u61c2\u4f60</text>
<text x="640" y="465" text-anchor="middle" """ + W + """ font-size="22" fill="#64748B">\u53cc\u677f\u67b6\u6784 \u00b7 MQTT \u4e92\u8054 \u00b7 AI \u5206\u6790 \u00b7 \u7eaf\u5f00\u6e90</text>
<text x="640" y="500" text-anchor="middle" """ + W + """ font-size="20" fill="#64748B">MicroPython + Python FastAPI \u00b7 MIT License</text>
<text x="640" y="680" text-anchor="middle" """ + W + """ font-size="18" fill="#64748B">ESP32 IoT \u9879\u76ee | 2026 \u5e74 6 \u6708</text>
<text x="1230" y="700" text-anchor="end" """ + W + """ font-size="12" fill="#4B5563">13</text>
</svg>""")

print("ALL DONE: 13 pages!")

