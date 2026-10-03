"""Generate 15 SVGs for lingmou_v7 with 32px body font."""
import os
DIR = r"F:\reasonix\skill\ppt-master\projects\ppt169_lingmou_v7_ppt169_20260624\svg_output"
# Clean
for f in os.listdir(DIR):
    os.remove(os.path.join(DIR, f))

BG = "#0A0E17"
W = 'font-family="\'Microsoft YaHei\',Arial,sans-serif"'
T = 'font-family="\'SimHei\',\'Microsoft YaHei\',Arial,sans-serif"'
C = 'font-family="Consolas,\'Courier New\',monospace"'

def w(n, s):
    with open(os.path.join(DIR, n), "wb") as f:
        f.write(s.encode("utf-8"))
    print(f"  {n}")

# P01 Cover
w("01_cover.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".1"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient><radialGradient id="g"><stop offset="0%" stop-color="#F59E0B" stop-opacity=".06"/><stop offset="100%" stop-color="#F59E0B" stop-opacity="0"/></radialGradient></defs><rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/><rect x="0" y="0" width="1280" height="720" fill="url(#g)"/>'
'<text x="640" y="300" text-anchor="middle" '+T+' font-size="60" font-weight="bold" fill="#F1F5F9">\u7075\u7738\u667a\u8054</text>'
'<text x="640" y="355" text-anchor="middle" '+W+' font-size="28" fill="#94A3B8">\u4ee5\u4f20\u611f\u91c7\u96c6+AI\u5206\u6790\u4e3a\u6838\u5fc3\u7684\u5bb6\u5c45\u786c\u4ef6\u4e92\u8054\u7cfb\u7edf</text>'
'<text x="640" y="420" text-anchor="middle" '+W+' font-size="20" fill="#64748B">\u53cc ESP32 \u00b7 MQTT \u00b7 FastAPI \u00b7 AI \u5206\u6790</text>'
'<text x="640" y="480" text-anchor="middle" '+W+' font-size="18" fill="#64748B">\u5c0f\u7ec4\u6210\u5458\uff1a\u718a\u660a \u00b7 \u5f20\u9ece \u00b7 \u5415\u7965\u745e \u00b7 \u6881\u6d2a\u5f6c \u00b7 \u5434\u6d2a\u654f</text>'
'<text x="640" y="680" text-anchor="middle" '+W+' font-size="18" fill="#64748B">ESP32 IoT \u9879\u76ee | 2026\u5e746\u6708</text>'
'<text x="1230" y="700" text-anchor="end" '+W+' font-size="12" fill="#4B5563">01</text></svg>')

# P02 TOC
w("02_toc.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs><rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>'
'<text x="640" y="85" text-anchor="middle" '+T+' font-size="40" font-weight="bold" fill="#F1F5F9">\u76ee \u5f55</text>'
'<rect x="100" y="130" width="500" height="110" rx="12" fill="#141B2D" stroke="#0EA5E9" stroke-width="1"/>'
'<text x="140" y="190" '+T+' font-size="28" font-weight="bold" fill="#0EA5E9">01</text>'
'<text x="200" y="178" '+T+' font-size="24" font-weight="bold" fill="#F1F5F9">\u9879\u76ee\u80cc\u666f</text>'
'<text x="200" y="212" '+W+' font-size="18" fill="#94A3B8">\u667a\u80fd\u5bb6\u5c45\u7684\u788e\u7247\u5316\u56f0\u5c40</text>'
'<rect x="680" y="130" width="500" height="110" rx="12" fill="#141B2D" stroke="#F59E0B" stroke-width="1"/>'
'<text x="720" y="190" '+T+' font-size="28" font-weight="bold" fill="#F59E0B">02</text>'
'<text x="780" y="178" '+T+' font-size="24" font-weight="bold" fill="#F1F5F9">\u7cfb\u7edf\u67b6\u6784</text>'
'<text x="780" y="212" '+W+' font-size="18" fill="#94A3B8">\u56db\u5c42\u6a21\u578b + \u6570\u636e\u6d41\u8bbe\u8ba1</text>'
'<rect x="100" y="270" width="500" height="110" rx="12" fill="#141B2D" stroke="#22C55E" stroke-width="1"/>'
'<text x="140" y="330" '+T+' font-size="28" font-weight="bold" fill="#22C55E">03</text>'
'<text x="200" y="318" '+T+' font-size="24" font-weight="bold" fill="#F1F5F9">\u6838\u5fc3\u529f\u80fd</text>'
'<text x="200" y="352" '+W+' font-size="18" fill="#94A3B8">8\u5927\u529f\u80fd + \u7a21\u4ef6\u914d\u7f6e + \u573a\u666f\u8054\u52a8</text>'
'<rect x="680" y="270" width="500" height="110" rx="12" fill="#141B2D" stroke="#06B6D4" stroke-width="1"/>'
'<text x="720" y="330" '+T+' font-size="28" font-weight="bold" fill="#06B6D4">04</text>'
'<text x="780" y="318" '+T+' font-size="24" font-weight="bold" fill="#F1F5F9">\u4ee3\u7801\u5b9e\u73b0</text>'
'<text x="780" y="352" '+W+' font-size="18" fill="#94A3B8">MQTT + AI + \u6570\u636e\u5e93 + API</text>'
'<rect x="340" y="410" width="600" height="110" rx="12" fill="#141B2D" stroke="#EF4444" stroke-width="1"/>'
'<text x="380" y="470" '+T+' font-size="28" font-weight="bold" fill="#EF4444">05</text>'
'<text x="440" y="458" '+T+' font-size="24" font-weight="bold" fill="#F1F5F9">\u9879\u76ee\u6210\u679c</text>'
'<text x="440" y="492" '+W+' font-size="18" fill="#94A3B8">\u6d4b\u8bd5\u7ed3\u679c + \u9879\u76ee\u5c0f\u7ed3</text>'
'<text x="1230" y="700" text-anchor="end" '+W+' font-size="12" fill="#4B5563">02</text></svg>')

# P03 Problem
w("03_problem.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs><rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>'
'<text x="640" y="80" text-anchor="middle" '+T+' font-size="40" font-weight="bold" fill="#F1F5F9">\u667a\u80fd\u5bb6\u5c45\u7684\u788e\u7247\u5316\u56f0\u5c40</text>'
'<rect x="60" y="125" width="540" height="130" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="90" y="170" '+T+' font-size="26" font-weight="bold" fill="#EF4444">\u54c1\u724c\u6797\u7acb</text>'
'<text x="90" y="210" '+W+' font-size="20" fill="#94A3B8">5-8\u4e2a\u4e0d\u540cApp\uff0c\u5404\u7ba1\u5404\u7684\u8bbe\u5907</text>'
'<text x="90" y="242" '+W+' font-size="20" fill="#94A3B8">\u4f53\u9a8c\u5272\u88c2\uff0c\u65e0\u7edf\u4e00\u6807\u51c6</text>'
'<rect x="60" y="280" width="540" height="130" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="90" y="325" '+T+' font-size="26" font-weight="bold" fill="#EF4444">\u5404\u81ea\u4e3a\u653f</text>'
'<text x="90" y="365" '+W+' font-size="20" fill="#94A3B8">\u8bbe\u5907\u95f4\u65e0\u6cd5\u771f\u6b63\u8054\u52a8</text>'
'<text x="90" y="397" '+W+' font-size="20" fill="#94A3B8">\u4e70\u518d\u591a\u4e5f\u662f\u5b64\u5c9b</text>'
'<rect x="60" y="435" width="540" height="130" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="90" y="480" '+T+' font-size="26" font-weight="bold" fill="#EF4444">\u6ca1\u6709\u771f\u667a\u80fd</text>'
'<text x="90" y="520" '+W+' font-size="20" fill="#94A3B8">\u53ea\u662f\u8fdc\u7a0b\u9065\u63a7</text>'
'<text x="90" y="552" '+W+' font-size="20" fill="#94A3B8">\u4e0d\u4f1a\u81ea\u52a8\u8c03\u8282\u548c\u9884\u8b66</text>'
'<rect x="660" y="125" width="560" height="440" rx="14" fill="#141B2D" stroke="#0EA5E9" stroke-width="1"/>'
'<text x="690" y="180" '+T+' font-size="28" font-weight="bold" fill="#0EA5E9">\u6211\u4eec\u7684\u65b9\u6848</text>'
'<text x="690" y="235" '+W+' font-size="22" fill="#F1F5F9">\u2022 15\u5143ESP32\u82af\u7247\u5c31\u591f\u4e86</text>'
'<text x="690" y="280" '+W+' font-size="22" fill="#F1F5F9">\u2022 \u4e0d\u7528\u88c5App\uff0c\u6d4f\u89c8\u5668\u63a7\u5236</text>'
'<text x="690" y="325" '+W+' font-size="22" fill="#F1F5F9">\u2022 \u4f20\u611f\u5668\u68c0\u6d4b\u5f02\u5e38\u81ea\u52a8\u5904\u7406</text>'
'<text x="690" y="370" '+W+' font-size="22" fill="#F1F5F9">\u2022 AI\u5206\u6790\u8d8b\u52bf\u548c\u5f02\u5e38</text>'
'<text x="690" y="415" '+W+' font-size="22" fill="#F1F5F9">\u2022 \u5168\u6808\u81ea\u7814\uff0c\u5f00\u6e90\u53ef\u590d\u7528</text>'
'<text x="690" y="460" '+W+' font-size="22" fill="#F1F5F9">\u2022 \u6781\u4f4e\u6210\u672c\uff0c\u5168\u5957\u767e\u5143\u5185</text>'
'<rect x="690" y="505" width="500" height="40" rx="8" fill="#0EA5E9" fill-opacity=".12"/>'
'<text x="940" y="532" text-anchor="middle" '+W+' font-size="20" fill="#0EA5E9">\u8fd9\u5c31\u662f\u7075\u7738\u667a\u8054</text>'
'<text x="1230" y="700" text-anchor="end" '+W+' font-size="12" fill="#4B5563">03</text></svg>')

print("P01-P03 done")

# P04 Architecture (四层模型)
w("04_architecture.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs><rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>'
'<text x="640" y="80" text-anchor="middle" '+T+' font-size="40" font-weight="bold" fill="#F1F5F9">\u7cfb\u7edf\u67b6\u6784 \u2014 \u56db\u5c42\u6a21\u578b</text>'
# Layer 4 (top)
'<rect x="160" y="130" width="960" height="55" rx="10" fill="#0EA5E9" fill-opacity=".1" stroke="#0EA5E9" stroke-width="1"/>'
'<text x="190" y="166" '+T+' font-size="20" font-weight="bold" fill="#0EA5E9">\u5e94\u7528\u5c42</text>'
'<text x="310" y="166" '+W+' font-size="18" fill="#F1F5F9">Web\u4eea\u8868\u76d8 \u00b7 \u8fdc\u7a0b\u63a7\u5236 \u00b7 \u81ea\u52a8\u5316\u5f15\u64ce</text>'
# Layer 3
'<rect x="160" y="205" width="960" height="55" rx="10" fill="#06B6D4" fill-opacity=".1" stroke="#06B6D4" stroke-width="1"/>'
'<text x="190" y="241" '+T+' font-size="20" font-weight="bold" fill="#06B6D4">\u670d\u52a1\u5c42</text>'
'<text x="310" y="241" '+W+' font-size="18" fill="#F1F5F9">FastAPI \u00b7 AI\u5206\u6790(DeepSeek) \u00b7 SQLite</text>'
# Layer 2
'<rect x="160" y="280" width="960" height="55" rx="10" fill="#141B2D" stroke="#F59E0B" stroke-width="1"/>'
'<text x="190" y="316" '+T+' font-size="20" font-weight="bold" fill="#F59E0B">\u63a7\u5236\u5c42</text>'
'<text x="310" y="316" '+W+' font-size="18" fill="#F1F5F9">ESP32#1 \u4e3b\u63a7\u677f \u00b7 ESP32#2 \u4f20\u611f\u5668\u677f \u00b7 MQTT Broker</text>'
# Layer 1 (bottom)
'<rect x="160" y="355" width="960" height="55" rx="10" fill="#22C55E" fill-opacity=".1" stroke="#22C55E" stroke-width="1"/>'
'<text x="190" y="391" '+T+' font-size="20" font-weight="bold" fill="#22C55E">\u611f\u77e5\u5c42</text>'
'<text x="310" y="391" '+W+' font-size="18" fill="#F1F5F9">DHT11 \u00b7 HC-SR04 \u00b7 \u5149\u654f \u00b7 PIR \u00b7 SCD41 \u00b7 RC522</text>'
# Details
'<rect x="160" y="440" width="960" height="200" rx="14" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="640" y="475" text-anchor="middle" '+T+' font-size="24" font-weight="bold" fill="#F1F5F9">\u786c\u4ef6\u914d\u7f6e\u6982\u89c8</text>'
'<text x="200" y="515" '+W+' font-size="18" fill="#94A3B8">ESP32 #1 \u4e3b\u63a7\uff1aDHT11 + 6\u8def\u706f\u5149 + RGB + \u98ce\u6247 + OLED</text>'
'<text x="200" y="548" '+W+' font-size="18" fill="#94A3B8">ESP32 #2 \u4f20\u611f\u5668\uff1a\u8d85\u58f0 + \u5149\u654f + PIR + CO2 + RFID + \u8235\u673a</text>'
'<text x="200" y="581" '+W+' font-size="18" fill="#94A3B8">\u901a\u4fe1\uff1aWiFi 2.4GHz + MQTT (mosquitto :1883)</text>'
'<text x="200" y="614" '+W+' font-size="18" fill="#94A3B8">\u8f6f\u4ef6\uff1aMicroPython + FastAPI + SQLite + WebSocket + AI</text>'
'<text x="1230" y="700" text-anchor="end" '+W+' font-size="12" fill="#4B5563">04</text></svg>')

# P05 Data Flow
w("05_dataflow.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs><rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>'
'<text x="640" y="80" text-anchor="middle" '+T+' font-size="40" font-weight="bold" fill="#F1F5F9">\u6570\u636e\u6d41\u8bbe\u8ba1</text>'
# Upstream
'<rect x="60" y="130" width="560" height="250" rx="14" fill="#141B2D" stroke="#0EA5E9" stroke-width="1"/>'
'<text x="90" y="175" '+T+' font-size="24" font-weight="bold" fill="#0EA5E9">\u4e0a\u884c\u6570\u636e\u6d41\uff08\u4f20\u611f\u5668 -> \u670d\u52a1\u5668\uff09</text>'
'<rect x="80" y="200" width="520" height="55" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="110" y="225" '+W+' font-size="18" fill="#F1F5F9">\u4f20\u611f\u5668\u91c7\u96c6</text>'
'<text x="330" y="225" '+W+' font-size="16" fill="#64748B">1s\u91c7\u6837\u5468\u671f</text>'
'<text x="110" y="250" '+C+' font-size="14" fill="#F59E0B">MQTT\u53d1\u5e03(esp32/+/telemetry)</text>'
'<rect x="80" y="275" width="520" height="55" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="110" y="300" '+W+' font-size="18" fill="#F1F5F9">\u670d\u52a1\u5668\u5904\u7406</text>'
'<text x="110" y="325" '+C+' font-size="14" fill="#22C55E">\u5b58\u50a8(SQLite) + \u5206\u6790(AI) + \u5e7f\u64ad(WebSocket)</text>'
'<rect x="80" y="350" width="520" height="55" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="110" y="375" '+W+' font-size="18" fill="#F1F5F9">WebSocket\u63a8\u9001 -> Dashboard\u663e\u793a</text>'
# Downstream
'<rect x="660" y="130" width="560" height="250" rx="14" fill="#141B2D" stroke="#F59E0B" stroke-width="1"/>'
'<text x="690" y="175" '+T+' font-size="24" font-weight="bold" fill="#F59E0B">\u4e0b\u884c\u6570\u636e\u6d41\uff08\u7528\u6237 -> \u8bbe\u5907\uff09</text>'
'<rect x="680" y="200" width="520" height="55" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="710" y="225" '+W+' font-size="18" fill="#F1F5F9">\u7528\u6237\u6307\u4ee4</text>'
'<text x="710" y="250" '+C+' font-size="14" fill="#06B6D4">POST /api/command</text>'
'<rect x="680" y="275" width="520" height="55" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="710" y="300" '+W+' font-size="18" fill="#F1F5F9">\u670d\u52a1\u5668\u8f6c\u53d1</text>'
'<text x="710" y="325" '+C+' font-size="14" fill="#F59E0B">MQTT\u4e0b\u53d1(esp32/+/command)</text>'
'<rect x="680" y="350" width="520" height="55" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="710" y="375" '+W+' font-size="18" fill="#F1F5F9">ESP32\u6267\u884c</text>'
'<text x="710" y="400" '+C+' font-size="14" fill="#22C55E">\u5f00/\u5173\u706f\u3001\u8c03RGB\u3001\u98ce\u6247\u63a7\u5236</text>'
# Summary
'<rect x="60" y="420" width="1160" height="100" rx="14" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="640" y="455" text-anchor="middle" '+T+' font-size="22" font-weight="bold" fill="#F1F5F9">\u4e3b\u9898\u7ed3\u6784</text>'
'<g '+W+' font-size="18" fill="#94A3B8">'
'<text x="100" y="490">\u2022 lip_reading/iot &mdash; ESP32#1\u63a7\u5236\u6307\u4ee4\uff0821\u6761\uff09</text>'
'<text x="690" y="490">\u2022 esp32/+/telemetry &mdash; \u4f20\u611f\u5668\u6570\u636e\u4e0a\u884c</text>'
'<text x="100" y="515">\u2022 esp32/+/presence &mdash; PIR\u4eba\u4f53\u68c0\u6d4b</text>'
'<text x="690" y="515">\u2022 esp32/+/command &mdash; \u63a7\u5236\u6307\u4ee4\u4e0b\u53d1</text>'
'</g>'
'<text x="1230" y="700" text-anchor="end" '+W+' font-size="12" fill="#4B5563">05</text></svg>')

# P06 Features
w("06_features.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs><rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>'
'<text x="640" y="80" text-anchor="middle" '+T+' font-size="40" font-weight="bold" fill="#F1F5F9">8\u5927\u529f\u80fd\u603b\u89c8</text>'
'<g '+W+'>'
# Card 1
'<rect x="60" y="130" width="270" height="120" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="80" y="170" font-size="20" font-weight="bold" fill="#0EA5E9">\u73af\u5883\u76d1\u6d4b</text>'
'<text x="80" y="202" font-size="16" fill="#94A3B8">DHT11\u6e29\u6e7f\u5ea6</text>'
'<text x="80" y="228" font-size="16" fill="#94A3B8">+OLED\u663e\u793a</text>'
# Card 2
'<rect x="365" y="130" width="270" height="120" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="385" y="170" font-size="20" font-weight="bold" fill="#F59E0B">\u667a\u80fd\u901a\u98ce</text>'
'<text x="385" y="202" font-size="16" fill="#94A3B8">\u6e7f\u5ea6>=85%\u6216</text>'
'<text x="385" y="228" font-size="16" fill="#94A3B8">\u6e29\u5ea6>=30\u00b0C\u81ea\u52a8\u98ce\u6247</text>'
# Card 3
'<rect x="670" y="130" width="270" height="120" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="690" y="170" font-size="20" font-weight="bold" fill="#06B6D4">\u5149\u7167\u81ea\u9002\u5e94</text>'
'<text x="690" y="202" font-size="16" fill="#94A3B8">\u5149\u654f\u68c0\u6d4b</text>'
'<text x="690" y="228" font-size="16" fill="#94A3B8">+\u81ea\u52a8\u5f00\u706f</text>'
# Card 4
'<rect x="975" y="130" width="245" height="120" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="995" y="170" font-size="20" font-weight="bold" fill="#22C55E">\u4eba\u4f53\u611f\u5e94</text>'
'<text x="995" y="202" font-size="16" fill="#94A3B8">PIR\u7ea2\u5916</text>'
'<text x="995" y="228" font-size="16" fill="#94A3B8">+\u53a5\u6240\u706f</text>'
# Row 2
'<rect x="60" y="275" width="270" height="120" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="80" y="315" font-size="20" font-weight="bold" fill="#EF4444">RFID\u95e8\u7981</text>'
'<text x="80" y="347" font-size="16" fill="#94A3B8">RC522\u5237\u5361</text>'
'<text x="80" y="373" font-size="16" fill="#94A3B8">+\u6b22\u8fce\u6a21\u5f0f</text>'
# Card 6
'<rect x="365" y="275" width="270" height="120" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="385" y="315" font-size="20" font-weight="bold" fill="#0EA5E9">\u667a\u80fd\u95e8\u9501</text>'
'<text x="385" y="347" font-size="16" fill="#94A3B8">SG90\u8235\u673a</text>'
'<text x="385" y="373" font-size="16" fill="#94A3B8">+\u8d85\u58f0\u6ce2\u81ea\u52a8\u5f00\u95e8</text>'
# Card 7
'<rect x="670" y="275" width="270" height="120" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="690" y="315" font-size="20" font-weight="bold" fill="#F59E0B">RGB\u73af\u5883\u706f</text>'
'<text x="690" y="347" font-size="16" fill="#94A3B8">\u6e29\u6e7f\u5ea6</text>'
'<text x="690" y="373" font-size="16" fill="#94A3B8">\u611f\u77e5\u53d8\u8272</text>'
# Card 8
'<rect x="975" y="275" width="245" height="120" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="995" y="315" font-size="20" font-weight="bold" fill="#06B6D4">CO2\u76d1\u6d4b</text>'
'<text x="995" y="347" font-size="16" fill="#94A3B8">SCD41</text>'
'<text x="995" y="373" font-size="16" fill="#94A3B8">+\u8d85\u6807\u901a\u98ce</text>'
'</g>'
# Summary
'<rect x="60" y="430" width="1160" height="70" rx="12" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="100" y="465" '+W+' font-size="18" fill="#94A3B8">\u2022 6\u4f20\u611f\u5668 + 7\u6267\u884c\u5668</text>'
'<text x="460" y="465" '+W+' font-size="18" fill="#94A3B8">\u2022 8\u5927\u529f\u80fd\u573a\u666f</text>'
'<text x="780" y="465" '+W+' font-size="18" fill="#94A3B8">\u2022 7\u6761\u81ea\u52a8\u5316\u89c4\u5219</text>'
'<text x="100" y="492" '+W+' font-size="18" fill="#94A3B8">\u2022 20+ REST API\u63a5\u53e3</text>'
'<text x="460" y="492" '+W+' font-size="18" fill="#94A3B8">\u2022 \u8fde\u7eed2h\u7a33\u5b9a\u8fd0\u884c\u6d4b\u8bd5\u901a\u8fc7</text>'
'<text x="1230" y="700" text-anchor="end" '+W+' font-size="12" fill="#4B5563">06</text></svg>')

print("P01-P06 done")

# P07 Hardware
w("07_hardware.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs><rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>'
'<text x="640" y="80" text-anchor="middle" '+T+' font-size="40" font-weight="bold" fill="#F1F5F9">\u786c\u4ef6\u914d\u7f6e\u8be6\u60c5</text>'
# Left: ESP32 #1
'<rect x="60" y="130" width="560" height="510" rx="14" fill="#141B2D" stroke="#0EA5E9" stroke-width="1"/>'
'<rect x="60" y="130" width="560" height="50" rx="14" fill="#0EA5E9" fill-opacity=".08"/>'
'<text x="80" y="163" '+T+' font-size="22" font-weight="bold" fill="#0EA5E9">ESP32 #1 \u2014 \u4e3b\u63a7\u677f</text>'
'<g '+W+' font-size="18">'
'<text x="90" y="205" fill="#94A3B8">GPIO27 &rarr; DHT11 (\u6e29\u6e7f\u5ea6)</text>'
'<text x="90" y="240" fill="#94A3B8">GPIO26/25/33 &rarr; RGB LED</text>'
'<text x="90" y="275" fill="#94A3B8">GPIO15/2/4/18/19/5 &rarr; 6\u8def\u706f\u5149</text>'
'<text x="90" y="310" fill="#94A3B8">GPIO21 &rarr; \u98ce\u6247\u7ee7\u7535\u5668</text>'
'<text x="90" y="345" fill="#94A3B8">I2C (SDA/SCL) &rarr; OLED\u663e\u793a</text>'
'<text x="90" y="380" fill="#94A3B8">DHT11: \u5355\u603b\u7ebf\u6570\u5b57\u4fe1\u53f7</text>'
'<text x="90" y="415" fill="#94A3B8">40\u4f4d\u6570\u636e(\u6e7f\u5ea68+\u6e29\u5ea68+\u6821\u9a8c8)</text>'
'<text x="90" y="450" fill="#94A3B8">WiFi 2.4GHz + MQTT\u5ba2\u6237\u7aef</text>'
'<text x="90" y="485" fill="#94A3B8">21\u6761MQTT\u6307\u4ee4\u5168\u8986\u76d6</text>'
'<text x="90" y="520" fill="#94A3B8">Client: esp32_lipreading_iot</text>'
'<text x="90" y="555" fill="#94A3B8">\u8ba2\u9605: lip_reading/iot</text>'
'</g>'
# Right: ESP32 #2
'<rect x="660" y="130" width="560" height="510" rx="14" fill="#141B2D" stroke="#F59E0B" stroke-width="1"/>'
'<rect x="660" y="130" width="560" height="50" rx="14" fill="#F59E0B" fill-opacity=".08"/>'
'<text x="680" y="163" '+T+' font-size="22" font-weight="bold" fill="#F59E0B">ESP32 #2 \u2014 \u4f20\u611f\u5668\u677f</text>'
'<g '+W+' font-size="18">'
'<text x="690" y="205" fill="#94A3B8">GPIO17/34 &rarr; HC-SR04 (\u8d85\u58f0\u6ce2)</text>'
'<text x="690" y="240" fill="#94A3B8">GPIO33/5 &rarr; LM393 (\u5149\u654f\u7535\u963b)</text>'
'<text x="690" y="275" fill="#94A3B8">GPIO4 &rarr; PIR (\u4eba\u4f53\u7ea2\u5916)</text>'
'<text x="690" y="310" fill="#94A3B8">GPIO32/22 &rarr; SCD41 (CO2, I2C)</text>'
'<text x="690" y="345" fill="#94A3B8">GPIO18/23/19/21 &rarr; RC522 (RFID, SPI)</text>'
'<text x="690" y="380" fill="#94A3B8">GPIO16 &rarr; SG90 (\u8235\u673a)</text>'
'<text x="690" y="415" fill="#94A3B8">HC-SR04: Trig+Echo\u6d4b\u8ddd\u79bb</text>'
'<text x="690" y="450" fill="#94A3B8">LM393: DO\u6570\u5b57+AO\u6a21\u62df(0-4095)</text>'
'<text x="690" y="485" fill="#94A3B8">PIR: \u70ed\u91ca\u7535\u7ea2\u5916(8-14um)</text>'
'<text x="690" y="520" fill="#94A3B8">SCD41: NDIR\u7ea2\u5916\u5438\u6536(400-5000ppm)</text>'
'<text x="690" y="555" fill="#94A3B8">RC522: 13.56MHz SPI, Mifare 1K</text>'
'</g>'
'<text x="1230" y="700" text-anchor="end" '+W+' font-size="12" fill="#4B5563">07</text></svg>')

# P08 Scenes
w("08_scenes.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs><rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>'
'<text x="640" y="80" text-anchor="middle" '+T+' font-size="40" font-weight="bold" fill="#F1F5F9">\u573a\u666f\u8054\u52a8 \u2014 \u81ea\u52a8\u5316\u89c4\u5219</text>'
'<g '+W+'>'
# Rule 1
'<rect x="60" y="130" width="360" height="70" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="90" y="158" font-size="18" font-weight="bold" fill="#0EA5E9">1. \u7ea2\u5916\u6709\u4eba</text>'
'<text x="90" y="185" font-size="16" fill="#94A3B8">\u2192 \u5f00\u53a5\u6240\u706f</text>'
# Rule 2
'<rect x="460" y="130" width="360" height="70" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="490" y="158" font-size="18" font-weight="bold" fill="#06B6D4">2. CO2 > 1000ppm</text>'
'<text x="490" y="185" font-size="16" fill="#94A3B8">\u2192 \u5f00\u98ce\u6247\u901a\u98ce</text>'
# Rule 3
'<rect x="860" y="130" width="360" height="70" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="890" y="158" font-size="18" font-weight="bold" fill="#22C55E">3. \u5149\u7ebf\u6697+\u5f00\u95e8</text>'
'<text x="890" y="185" font-size="16" fill="#94A3B8">\u2192 \u81ea\u52a8\u5f00\u706f</text>'
# Rule 4
'<rect x="60" y="220" width="360" height="70" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="90" y="248" font-size="18" font-weight="bold" fill="#F59E0B">4. \u5149\u7ebf\u6697+\u4eba\u4f53\u79fb\u52a8</text>'
'<text x="90" y="275" font-size="16" fill="#94A3B8">\u2192 \u81ea\u52a8\u5f00\u706f</text>'
# Rule 5
'<rect x="460" y="220" width="360" height="70" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="490" y="248" font-size="18" font-weight="bold" fill="#EF4444">5. RFID\u5237\u5361</text>'
'<text x="490" y="275" font-size="16" fill="#94A3B8">\u2192 \u5f00\u95e8+\u706f+RGB\u6696\u8272</text>'
# Rule 6
'<rect x="860" y="220" width="360" height="70" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="890" y="248" font-size="18" font-weight="bold" fill="#0EA5E9">6. \u8d85\u58f0\u6ce2\u8fd1\u8ddd\u79bb</text>'
'<text x="890" y="275" font-size="16" fill="#94A3B8">\u2192 \u81ea\u52a8\u5f00\u95e8</text>'
# Rule 7
'<rect x="60" y="310" width="360" height="70" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="90" y="338" font-size="18" font-weight="bold" fill="#22C55E">7. \u591c\u95f4\u5f00\u95e8</text>'
'<text x="90" y="365" font-size="16" fill="#94A3B8">\u2192 \u8702\u9e23\u5668\u62a5\u8b66</text>'
'</g>'
# One-click scenes
'<rect x="60" y="420" width="560" height="210" rx="14" fill="#141B2D" stroke="#22C55E" stroke-width="1"/>'
'<text x="90" y="460" '+T+' font-size="22" font-weight="bold" fill="#22C55E">\u56de\u5bb6\u6a21\u5f0f</text>'
'<text x="90" y="495" '+W+' font-size="18" fill="#94A3B8">POST /api/scene/home</text>'
'<text x="90" y="528" '+W+' font-size="18" fill="#F1F5F9">\u2713 \u5168\u5c4b\u5f00\u706f + RGB\u6696\u8272</text>'
'<text x="90" y="560" '+W+' font-size="18" fill="#F1F5F9">\u2713 \u98ce\u6247\u5c31\u7eea + \u95e8\u9501\u5f00\u542f</text>'
'<text x="90" y="592" '+W+' font-size="16" fill="#64748B">\u5ef6\u65f630s\u540e\u81ea\u52a8\u5173\u95e8</text>'
'<rect x="660" y="420" width="560" height="210" rx="14" fill="#141B2D" stroke="#EF4444" stroke-width="1"/>'
'<text x="690" y="460" '+T+' font-size="22" font-weight="bold" fill="#EF4444">\u79bb\u5bb6\u6a21\u5f0f</text>'
'<text x="690" y="495" '+W+' font-size="18" fill="#94A3B8">POST /api/scene/away</text>'
'<text x="690" y="528" '+W+' font-size="18" fill="#F1F5F9">\u2717 \u5168\u5c4b\u5173\u706f + RGB\u7184\u706d</text>'
'<text x="690" y="560" '+W+' font-size="18" fill="#F1F5F9">\u2717 \u98ce\u6247\u5173\u95ed + \u95e8\u9501\u4e0a\u9501</text>'
'<text x="690" y="592" '+W+' font-size="16" fill="#64748B">\u4e00\u952e\u6267\u884c\uff0c\u5c4f\u853d\u5176\u4ed6\u89e6\u53d1</text>'
'<text x="1230" y="700" text-anchor="end" '+W+' font-size="12" fill="#4B5563">08</text></svg>')

print("P01-P08 done")

# P09 Software Stack
w("09_software.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs><rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>'
'<text x="640" y="80" text-anchor="middle" '+T+' font-size="40" font-weight="bold" fill="#F1F5F9">\u8f6f\u4ef6\u5168\u6808\u67b6\u6784</text>'
'<rect x="60" y="130" width="560" height="510" rx="14" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="90" y="170" '+T+' font-size="22" font-weight="bold" fill="#0EA5E9">\u670d\u52a1\u5668\u7aef (Python/FastAPI)</text>'
'<g '+W+' font-size="17">'
'<text x="90" y="210" fill="#94A3B8">main.py &mdash; \u5165\u53e3</text>'
'<text x="90" y="245" fill="#94A3B8">mqtt_client.py &mdash; MQTT(15KB)</text>'
'<text x="90" y="280" fill="#94A3B8">ai_analyzer.py &mdash; AI\u5206\u6790(11KB)</text>'
'<text x="90" y="315" fill="#94A3B8">routes.py &mdash; \u8def\u7531(19KB)</text>'
'<text x="90" y="350" fill="#94A3B8">models.py &mdash; \u6570\u636e\u6a21\u578b(16KB)</text>'
'<text x="90" y="385" fill="#94A3B8">ws.py &mdash; WebSocket</text>'
'<text x="90" y="420" fill="#94A3B8">exporter.py &mdash; \u6570\u636e\u5bfc\u51fa</text>'
'<text x="90" y="455" fill="#94A3B8">FastAPI + uvicorn\u670d\u52a1\u5668</text>'
'<text x="90" y="490" fill="#94A3B8">paho-mqtt\u5ba2\u6237\u7aef\u8fde\u63a5</text>'
'<text x="90" y="525" fill="#94A3B8">aiosqlite\u5f02\u6b65\u6570\u636e\u5e93</text>'
'<text x="90" y="560" fill="#94A3B8">CSV\u6570\u636e\u5bfc\u51fa\u529f\u80fd</text>'
'</g>'
'<rect x="660" y="130" width="560" height="510" rx="14" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="690" y="170" '+T+' font-size="22" font-weight="bold" fill="#F59E0B">ESP32\u7aef (MicroPython)</text>'
'<g '+W+' font-size="17">'
'<text x="690" y="210" fill="#94A3B8">main.py &mdash; \u4e3b\u63a7\u677f(20KB)</text>'
'<text x="690" y="245" fill="#94A3B8">sensor_node.py &mdash; \u4f20\u611f\u5668\u677f(17KB)</text>'
'<text x="690" y="280" fill="#94A3B8">oled_display.py &mdash; OLED\u663e\u793a</text>'
'<text x="690" y="315" fill="#94A3B8">oled_font.py &mdash; \u4e2d\u6587\u5b57\u4f53</text>'
'<text x="690" y="350" fill="#94A3B8">ssd1306.py &mdash; OLED\u9a71\u52a8</text>'
'<text x="690" y="385" fill="#94A3B8">umqttsimple.py &mdash; MQTT\u5ba2\u6237\u7aef</text>'
'<text x="690" y="420" fill="#94A3B8">DHT11 + RGB + \u7ee7\u7535\u5668\u63a7\u5236</text>'
'<text x="690" y="455" fill="#94A3B8">6\u8def\u706f\u5149IO\u53e3\u63a7\u5236</text>'
'<text x="690" y="490" fill="#94A3B8">I2C\u901a\u4fe1(OLED/CO2)</text>'
'<text x="690" y="525" fill="#94A3B8">SPI\u901a\u4fe1(RFID)</text>'
'<text x="690" y="560" fill="#94A3B8">PWM\u8c03\u5149(RGB) + PWM\u8235\u673a</text>'
'</g>'
'<text x="1230" y="700" text-anchor="end" '+W+' font-size="12" fill="#4B5563">09</text></svg>')

# P10 MQTT Code
w("10_mqtt_code.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs><rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>'
'<text x="640" y="80" text-anchor="middle" '+T+' font-size="40" font-weight="bold" fill="#F1F5F9">\u6838\u5fc3\u4ee3\u7801\uff1aMQTT\u81ea\u52a8\u5316</text>'
'<rect x="60" y="125" width="560" height="280" rx="14" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="90" y="165" '+T+' font-size="22" font-weight="bold" fill="#0EA5E9">MQTT\u4e8b\u4ef6\u5904\u7406</text>'
'<rect x="80" y="185" width="520" height="200" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<g '+C+' font-size="14" fill="#94A3B8">'
'<text x="100" y="212">async def on_telemetry(msg):</text>'
'<text x="100" y="237">    data = json.loads(msg.payload)</text>'
'<text x="100" y="262">    await db.save_telemetry(data)</text>'
'<text x="100" y="287">    comfort = calc_comfort(data)</text>'
'<text x="100" y="312">    if comfort.score &lt; 60:</text>'
'<text x="120" y="337">        await publish("esp32/+/command", auto_cmd())</text>'
'<text x="100" y="362">    await ws.broadcast(data)</text>'
'</g>'
'<rect x="660" y="125" width="560" height="280" rx="14" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="690" y="165" '+T+' font-size="22" font-weight="bold" fill="#F59E0B">MQTT\u4e3b\u9898\u7ed3\u6784</text>'
'<rect x="680" y="185" width="520" height="40" rx="6" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="700" y="205" '+W+' font-size="16" fill="#0EA5E9">\u4e3b\u9898 &nbsp;&nbsp;&nbsp; \u65b9\u5411 &nbsp;&nbsp;&nbsp; \u7528\u9014</text>'
'<g '+W+' font-size="15" fill="#94A3B8">'
'<rect x="680" y="235" width="520" height="30" rx="4" fill="#0A0E17"/>
'<text x="700" y="256" fill="#94A3B8">esp32/+/telemetry &nbsp;&nbsp; \u2191 &nbsp;&nbsp; \u4f20\u611f\u5668\u6570\u636e</text>'
'<rect x="680" y="270" width="520" height="30" rx="4" fill="#0A0E17"/>
'<text x="700" y="291" fill="#94A3B8">esp32/+/presence &nbsp;&nbsp;\u2191 &nbsp;&nbsp; \u4eba\u4f53\u68c0\u6d4b</text>'
'<rect x="680" y="305" width="520" height="30" rx="4" fill="#0A0E17"/>
'<text x="700" y="326" fill="#94A3B8">esp32/+/rfid &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \u2191 &nbsp;&nbsp; RFID\u4e8b\u4ef6</text>'
'<rect x="680" y="340" width="520" height="30" rx="4" fill="#0A0E17"/>
'<text x="700" y="361" fill="#94A3B8">esp32/+/command &nbsp;&nbsp; \u2193 &nbsp;&nbsp; \u63a7\u5236\u6307\u4ee4</text>'
'<rect x="680" y="375" width="520" height="30" rx="4" fill="#0A0E17"/>
'<text x="700" y="396" fill="#94A3B8">esp32/+/config &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \u2193 &nbsp;&nbsp; \u914d\u7f6e\u4e0b\u53d1</text>'
'</g>'
'<rect x="60" y="440" width="1160" height="100" rx="14" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="90" y="478" '+T+' font-size="20" font-weight="bold" fill="#22C55E">\u5b8c\u6574\u6570\u636e\u94fe\u8def</text>'
'<text x="90" y="518" '+W+' font-size="18" fill="#94A3B8">ESP32\u91c7\u96c6 \u2192 MQTT\u53d1\u5e03 \u2192 mosquitto Broker \u2192 paho-mqtt on_message() \u2192 SQLite + WebSocket</text>'
'<text x="1230" y="700" text-anchor="end" '+W+' font-size="12" fill="#4B5563">10</text></svg>')

# P11 AI Code
w("11_ai_code.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs><rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>'
'<text x="640" y="80" text-anchor="middle" '+T+' font-size="40" font-weight="bold" fill="#F1F5F9">\u6838\u5fc3\u4ee3\u7801\uff1aAI\u8212\u9002\u5ea6\u8bc4\u5206</text>'
'<rect x="60" y="125" width="560" height="280" rx="14" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="90" y="165" '+T+' font-size="22" font-weight="bold" fill="#0EA5E9">\u8212\u9002\u5ea6\u8bc4\u5206\u7b97\u6cd5</text>'
'<rect x="80" y="185" width="520" height="200" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<g '+C+' font-size="14" fill="#94A3B8">'
'<text x="100" y="212">def calc_comfort(temp, humi, co2):</text>'
'<text x="100" y="237">    score = 100</text>'
'<text x="100" y="262">    score -= abs(temp - 24) * 2  # \u6700\u4f73\u6e29\u5ea624\u00b0C</text>'
'<text x="100" y="287">    score -= abs(humi - 55) * 0.5  # \u6700\u4f73\u6e7f\u5ea655%</text>'
'<text x="100" y="312">    if co2 &gt; 1000:</text>'
'<text x="120" y="337">        score -= 20  # CO2\u8fc7\u9ad8\u6263\u5206</text>'
'<text x="100" y="362">    return max(0, min(100, score))</text>'
'</g>'
'<rect x="660" y="125" width="560" height="280" rx="14" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="690" y="165" '+T+' font-size="22" font-weight="bold" fill="#F59E0B">\u76f8\u5173API\u63a5\u53e3</text>'
'<g '+W+' font-size="18">'
'<rect x="680" y="195" width="520" height="50" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="710" y="225" fill="#0EA5E9">GET /api/ai/summary</text>'
'<text x="710" y="242" fill="#64748B">AI\u6458\u8981\u62a5\u544a</text>'
'<rect x="680" y="255" width="520" height="50" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="710" y="285" fill="#F59E0B">POST /api/ai/analyze</text>'
'<text x="710" y="302" fill="#64748B">\u6df1\u5ea6\u5206\u6790 (DeepSeek)</text>'
'<rect x="680" y="315" width="520" height="50" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="710" y="345" fill="#22C55E">GET /api/comfort</text>'
'<text x="710" y="362" fill="#64748B">\u5b9e\u65f6\u8212\u9002\u5ea6\u8bc4\u5206</text>'
'<rect x="680" y="375" width="520" height="50" rx="8" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="710" y="405" fill="#06B6D4">GET /api/ai/compare</text>'
'<text x="710" y="422" fill="#64748B">\u5386\u53f2\u5bf9\u6bd4\u5206\u6790</text>'
'</g>'
'<rect x="60" y="440" width="1160" height="80" rx="14" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="90" y="478" '+T+' font-size="20" font-weight="bold" fill="#22C55E">\u8212\u9002\u5ea6\u5206\u7ea7\u6807\u51c6</text>'
'<text x="90" y="510" '+W+' font-size="16" fill="#94A3B8">80-100: \u8212\u9002 | 60-79: \u4e00\u822c | 40-59: \u4e0d\u8212\u9002 | &lt;40: \u7cdf\u7cd5</text>'
'<text x="1230" y="700" text-anchor="end" '+W+' font-size="12" fill="#4B5563">11</text></svg>')

# P12 Database + API
w("12_db_api.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs><rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>'
'<text x="640" y="80" text-anchor="middle" '+T+' font-size="40" font-weight="bold" fill="#F1F5F9">\u6570\u636e\u5e93\u8bbe\u8ba1 + API\u4e00\u89c8</text>'
# Database
'<rect x="60" y="130" width="560" height="510" rx="14" fill="#141B2D" stroke="#0EA5E9" stroke-width="1"/>'
'<text x="90" y="170" '+T+' font-size="22" font-weight="bold" fill="#0EA5E9">\u6570\u636e\u5e93 9\u5f20\u6838\u5fc3\u8868</text>'
'<g '+W+' font-size="18">'
'<rect x="80" y="195" width="240" height="36" rx="6" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="100" y="219" fill="#0EA5E9">devices</text>'
'<text x="260" y="219" fill="#94A3B8">\u8bbe\u5907\u4fe1\u606f\u8868</text>'
'<rect x="80" y="240" width="240" height="36" rx="6" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="100" y="264" fill="#0EA5E9">telemetry_log</text>'
'<text x="260" y="264" fill="#94A3B8">\u4f20\u611f\u5668\u6570\u636e\u65e5\u5fd7</text>'
'<rect x="80" y="285" width="240" height="36" rx="6" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="100" y="309" fill="#F59E0B">commands</text>'
'<text x="260" y="309" fill="#94A3B8">\u63a7\u5236\u6307\u4ee4\u8bb0\u5f55</text>'
'<rect x="80" y="330" width="240" height="36" rx="6" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="100" y="354" fill="#22C55E">rfid_log</text>'
'<text x="260" y="354" fill="#94A3B8">RFID\u5237\u5361\u65e5\u5fd7</text>'
'<rect x="80" y="375" width="240" height="36" rx="6" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="100" y="399" fill="#06B6D4">presence_log</text>'
'<text x="260" y="399" fill="#94A3B8">\u4eba\u4f53\u68c0\u6d4b\u65e5\u5fd7</text>'
'<rect x="80" y="420" width="240" height="36" rx="6" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="100" y="444" fill="#EF4444">config</text>'
'<text x="260" y="444" fill="#94A3B8">\u7cfb\u7edf\u914d\u7f6e\u8868</text>'
'<rect x="80" y="465" width="240" height="36" rx="6" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="100" y="489" fill="#0EA5E9">ai_reports</text>'
'<text x="260" y="489" fill="#94A3B8">AI\u5206\u6790\u62a5\u544a</text>'
'<rect x="80" y="510" width="240" height="36" rx="6" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="100" y="534" fill="#F59E0B">access_log</text>'
'<text x="260" y="534" fill="#94A3B8">\u95e8\u7981\u8bbf\u95ee\u8bb0\u5f55</text>'
'<rect x="80" y="555" width="240" height="36" rx="6" fill="#0A0E17" stroke="#1E293B" stroke-width=".5"/>'
'<text x="100" y="579" fill="#22C55E">messages</text>'
'<text x="260" y="579" fill="#94A3B8">\u7cfb\u7edf\u6d88\u606f\u8868</text>'
'</g>'
# API
'<rect x="660" y="130" width="560" height="510" rx="14" fill="#141B2D" stroke="#F59E0B" stroke-width="1"/>'
'<text x="690" y="170" '+T+' font-size="22" font-weight="bold" fill="#F59E0B">REST API\u4e00\u89c8</text>'
'<g '+C+' font-size="16">'
'<text x="700" y="210" fill="#0EA5E9">GET &nbsp;&nbsp;&nbsp;&nbsp; /api/devices</text>'
'<text x="700" y="240" fill="#94A3B8">\u83b7\u53d6\u8bbe\u5907\u5217\u8868</text>'
'<text x="700" y="275" fill="#F59E0B">POST &nbsp;&nbsp; /api/devices/{id}/command</text>'
'<text x="700" y="305" fill="#94A3B8">\u53d1\u9001\u63a7\u5236\u6307\u4ee4</text>'
'<text x="700" y="340" fill="#22C55E">POST &nbsp;&nbsp; /api/devices/{id}/rgb</text>'
'<text x="700" y="370" fill="#94A3B8">\u8bbe\u7f6eRGB\u989c\u8272</text>'
'<text x="700" y="405" fill="#06B6D4">POST &nbsp;&nbsp; /api/scene/home</text>'
'<text x="700" y="435" fill="#94A3B8">\u56de\u5bb6\u6a21\u5f0f</text>'
'<text x="700" y="470" fill="#EF4444">POST &nbsp;&nbsp; /api/scene/away</text>'
'<text x="700" y="500" fill="#94A3B8">\u79bb\u5bb6\u6a21\u5f0f</text>'
'<text x="700" y="535" fill="#0EA5E9">GET &nbsp;&nbsp;&nbsp;&nbsp; /api/ai/summary</text>'
'<text x="700" y="565" fill="#94A3B8">AI\u6458\u8981\u62a5\u544a</text>'
'<text x="700" y="600" fill="#F59E0B">GET &nbsp;&nbsp;&nbsp;&nbsp; /api/comfort</text>'
'<text x="700" y="630" fill="#94A3B8">\u8212\u9002\u5ea6\u8bc4\u5206</text>'
'</g>'
'<text x="1230" y="700" text-anchor="end" '+W+' font-size="12" fill="#4B5563">12</text></svg>')

print("P01-P12 done")



