"""Generate all 10 SVG files - using &lt; &gt; for comparisons."""
import os, shutil

DIR = r"F:\reasonix\skill\ppt-master\projects\ppt169_lingmou_v7_ppt169_20260624\svg_output"
# Clean directory
for f in os.listdir(DIR):
    os.remove(os.path.join(DIR, f))

BG = "#0A0E17"
LT = "&lt;"
GT = "&gt;"

def w(name, svg):
    path = os.path.join(DIR, name)
    with open(path, "wb") as f:
        f.write(svg.encode("utf-8"))
    print(f"OK {name}")

# P01 Cover
w("01_cover.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">'
'<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".1"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient>'
'<radialGradient id="g"><stop offset="0%" stop-color="#F59E0B" stop-opacity=".06"/><stop offset="100%" stop-color="#F59E0B" stop-opacity="0"/></radialGradient></defs>'
'<rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/>'
'<rect x="0" y="0" width="1280" height="720" fill="url(#s)"/><rect x="0" y="0" width="1280" height="720" fill="url(#g)"/>'
'<text x="640" y="320" text-anchor="middle" font-family="\'SimHei\',\'Microsoft YaHei\',Arial,sans-serif" font-size="60" font-weight="bold" fill="#F1F5F9">\u7075\u7738\u667a\u8054</text>'
'<text x="640" y="380" text-anchor="middle" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="24" fill="#94A3B8">\u4f20\u611f\u91c7\u96c6 + AI \u5206\u6790\u7684\u5bb6\u5c45\u786c\u4ef6\u4e92\u8054\u7cfb\u7edf</text>'
'<text x="640" y="445" text-anchor="middle" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="18" fill="#64748B">ESP32 \u53cc\u677f\u67b6\u6784 \u00b7 MQTT \u4e92\u8054 \u00b7 \u5168\u6808\u81ea\u7814</text>'
'<text x="640" y="680" text-anchor="middle" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="14" fill="#64748B">ESP32 IoT \u9879\u76ee | 2026 \u5e74 6 \u6708</text>'
'<text x="1230" y="700" text-anchor="end" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="12" fill="#4B5563">01 / 10</text></svg>')

# P02 TOC
w("02_toc.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">'
'<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs>'
'<rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>'
'<text x="640" y="90" text-anchor="middle" font-family="\'SimHei\',\'Microsoft YaHei\',Arial,sans-serif" font-size="36" font-weight="bold" fill="#F1F5F9">\u4eca\u5929\u8bb2\u56db\u4ef6\u4e8b</text>'
'<rect x="120" y="145" width="480" height="100" rx="12" fill="#141B2D" stroke="#0EA5E9" stroke-width="1"/>'
'<text x="180" y="195" text-anchor="middle" font-family="\'SimHei\',\'Microsoft YaHei\',Arial,sans-serif" font-size="28" font-weight="bold" fill="#0EA5E9">01</text>'
'<text x="225" y="190" font-family="\'SimHei\',\'Microsoft YaHei\',Arial,sans-serif" font-size="22" font-weight="bold" fill="#F1F5F9">\u95ee\u9898</text>'
'<text x="225" y="220" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="16" fill="#94A3B8">\u667a\u80fd\u5bb6\u5c45\u7684\u788e\u7247\u5316\u56f0\u5c40</text>'
'<rect x="680" y="145" width="480" height="100" rx="12" fill="#141B2D" stroke="#F59E0B" stroke-width="1"/>'
'<text x="740" y="195" text-anchor="middle" font-family="\'SimHei\',\'Microsoft YaHei\',Arial,sans-serif" font-size="28" font-weight="bold" fill="#F59E0B">02</text>'
'<text x="785" y="190" font-family="\'SimHei\',\'Microsoft YaHei\',Arial,sans-serif" font-size="22" font-weight="bold" fill="#F1F5F9">\u65b9\u6848</text>'
'<text x="785" y="220" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="16" fill="#94A3B8">\u53cc\u677f\u4e00\u4e91\uff1a\u786c\u4ef6\u67b6\u6784+\u6570\u636e\u6d41\u7ba1\u9053</text>'
'<rect x="120" y="285" width="480" height="100" rx="12" fill="#141B2D" stroke="#22C55E" stroke-width="1"/>'
'<text x="180" y="335" text-anchor="middle" font-family="\'SimHei\',\'Microsoft YaHei\',Arial,sans-serif" font-size="28" font-weight="bold" fill="#22C55E">03</text>'
'<text x="225" y="330" font-family="\'SimHei\',\'Microsoft YaHei\',Arial,sans-serif" font-size="22" font-weight="bold" fill="#F1F5F9">\u9a8c\u8bc1</text>'
'<text x="225" y="360" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="16" fill="#94A3B8">\u573a\u666f\u6f14\u793a + \u529f\u80fd\u4e00\u89c8</text>'
'<rect x="680" y="285" width="480" height="100" rx="12" fill="#141B2D" stroke="#06B6D4" stroke-width="1"/>'
'<text x="740" y="335" text-anchor="middle" font-family="\'SimHei\',\'Microsoft YaHei\',Arial,sans-serif" font-size="28" font-weight="bold" fill="#06B6D4">04</text>'
'<text x="785" y="330" font-family="\'SimHei\',\'Microsoft YaHei\',Arial,sans-serif" font-size="22" font-weight="bold" fill="#F1F5F9">\u53cd\u601d</text>'
'<text x="785" y="360" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="16" fill="#94A3B8">\u603b\u7ed3 + \u4e0b\u4e00\u6b65\u6539\u8fdb</text>'
'<text x="640" y="680" text-anchor="middle" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="14" fill="#64748B">\u7075\u7738\u667a\u8054 \u2014 \u4f20\u611f\u91c7\u96c6+AI\u5206\u6790\u7684\u5bb6\u5c45\u786c\u4ef6\u4e92\u8054\u7cfb\u7edf</text>'
'<text x="1230" y="700" text-anchor="end" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="12" fill="#4B5563">02 / 10</text></svg>')

# P03 Problem
w("03_problem.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">'
'<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs>'
'<rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>'
'<text x="640" y="90" text-anchor="middle" font-family="\'SimHei\',\'Microsoft YaHei\',Arial,sans-serif" font-size="32" font-weight="bold" fill="#F1F5F9">\u667a\u80fd\u5bb6\u5c45\u7684\u788e\u7247\u5316\u56f0\u5c40</text>'
'<rect x="80" y="145" width="520" height="100" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="110" y="185" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="18" font-weight="bold" fill="#EF4444">\u26a0 \u54c1\u724c\u6797\u7acb</text>'
'<text x="110" y="215" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="15" fill="#94A3B8">5-8 \u4e2a\u4e0d\u540c App\uff0c\u5404\u7ba1\u5404\u7684\u8bbe\u5907</text>'
'<rect x="80" y="270" width="520" height="100" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="110" y="310" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="18" font-weight="bold" fill="#EF4444">\u274c \u5404\u81ea\u4e3a\u653f</text>'
'<text x="110" y="340" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="15" fill="#94A3B8">\u8bbe\u5907\u95f4\u65e0\u6cd5\u771f\u6b63\u8054\u52a8\uff0c\u4e70\u518d\u591a\u4e5f\u662f\u5b64\u5c9b</text>'
'<rect x="80" y="395" width="520" height="100" rx="10" fill="#141B2D" stroke="#1E293B" stroke-width="1"/>'
'<text x="110" y="435" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="18" font-weight="bold" fill="#EF4444">\u6ca1\u6709\u771f\u667a\u80fd</text>'
'<text x="110" y="465" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="15" fill="#94A3B8">\u53ea\u662f\u8fdc\u7a0b\u9065\u63a7\uff0c\u4e0d\u4f1a\u81ea\u52a8\u8c03\u8282\u3001\u4e0d\u4f1a\u5f02\u5e38\u9884\u8b66</text>'
'<rect x="660" y="145" width="540" height="350" rx="14" fill="#141B2D" stroke="#0EA5E9" stroke-width="1"/>'
'<text x="690" y="190" font-family="\'SimHei\',\'Microsoft YaHei\',Arial,sans-serif" font-size="22" font-weight="bold" fill="#0EA5E9">\u2728 \u6211\u4eec\u7684\u65b9\u6848</text>'
'<text x="690" y="250" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="17" fill="#F1F5F9">15 \u5143\u7684 ESP32 \u82af\u7247\u5c31\u591f\u4e86</text>'
'<text x="690" y="285" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="17" fill="#F1F5F9">\u4e0d\u7528\u88c5 App\uff0c\u6d4f\u89c8\u5668\u6253\u5f00\u5c31\u80fd\u63a7\u5236</text>'
'<text x="690" y="320" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="17" fill="#F1F5F9">\u4f20\u611f\u5668\u68c0\u6d4b\u5230\u5f02\u5e38\uff0c\u7cfb\u7edf\u81ea\u5df1\u5904\u7406</text>'
'<text x="690" y="355" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="17" fill="#F1F5F9">AI \u5206\u6790\u8d8b\u52bf\u548c\u5f02\u5e38\uff0c\u4e0d\u53ea\u662f\u91c7\u96c6\u6570\u636e</text>'
'<rect x="690" y="390" width="480" height="36" rx="8" fill="#0EA5E9" fill-opacity=".12"/>'
'<text x="930" y="414" text-anchor="middle" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="16" fill="#0EA5E9">\u2728 \u8fd9\u5c31\u662f\u7075\u7738\u667a\u8054</text>'
'<text x="1230" y="700" text-anchor="end" font-family="\'Microsoft YaHei\',Arial,sans-serif" font-size="12" fill="#4B5563">03 / 10</text></svg>')

print("P01-P03 done")
