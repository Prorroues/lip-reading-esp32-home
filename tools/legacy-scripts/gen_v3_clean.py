"""Generate 15 SVG files for lingmou_v7 with 32px body."""
import os, sys

DIR = r"F:\reasonix\skill\ppt-master\projects\ppt169_lingmou_v7_ppt169_20260624\svg_output"
for f in os.listdir(DIR):
    os.remove(os.path.join(DIR, f))

BG = "#0A0E17"
W = 'font-family="\'Microsoft YaHei\',Arial,sans-serif"'
T = 'font-family="\'SimHei\',\'Microsoft YaHei\',Arial,sans-serif"'
C = 'font-family="Consolas,\'Courier New\',monospace"'

def w(n, svg):
    p = os.path.join(DIR, n)
    with open(p, "wb") as f:
        f.write(svg.encode("utf-8"))
    print(f"  {n}")

# P01 Cover
s = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">'
s += '<defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".1"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient>'
s += '<radialGradient id="g"><stop offset="0%" stop-color="#F59E0B" stop-opacity=".06"/><stop offset="100%" stop-color="#F59E0B" stop-opacity="0"/></radialGradient></defs>'
s += '<rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/>'
s += '<rect x="0" y="0" width="1280" height="720" fill="url(#s)"/><rect x="0" y="0" width="1280" height="720" fill="url(#g)"/>'
s += '<text x="640" y="300" text-anchor="middle" '+T+' font-size="60" font-weight="bold" fill="#F1F5F9">灵眸智联</text>'
s += '<text x="640" y="355" text-anchor="middle" '+W+' font-size="28" fill="#94A3B8">以传感采集+AI分析为核心的家居硬件互联系统</text>'
s += '<text x="640" y="420" text-anchor="middle" '+W+' font-size="20" fill="#64748B">双ESP32 \u00b7 MQTT \u00b7 FastAPI \u00b7 AI分析</text>'
s += '<text x="640" y="480" text-anchor="middle" '+W+' font-size="18" fill="#64748B">小组成员：熊昊 \u00b7 张黎 \u00b7 吕祥瑞 \u00b7 梁洪彬 \u00b7 吴洪敏</text>'
s += '<text x="640" y="680" text-anchor="middle" '+W+' font-size="18" fill="#64748B">ESP32 IoT项目 | 2026年6月</text>'
s += '<text x="1230" y="700" text-anchor="end" '+W+' font-size="12" fill="#4B5563">01</text></svg>'
w("01_cover.svg", s)

# P02 TOC
s = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><defs><radialGradient id="s"><stop offset="0%" stop-color="#0EA5E9" stop-opacity=".06"/><stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/></radialGradient></defs>'
s += '<rect x="0" y="0" width="1280" height="720" fill="'+BG+'"/><rect x="0" y="0" width="1280" height="720" fill="url(#s)"/>'
s += '<text x="640" y="85" text-anchor="middle" '+T+' font-size="40" font-weight="bold" fill="#F1F5F9">目 录</text>'
s += '<rect x="100" y="130" width="500" height="110" rx="12" fill="#141B2D" stroke="#0EA5E9" stroke-width="1"/>'
s += '<text x="140" y="190" '+T+' font-size="28" font-weight="bold" fill="#0EA5E9">01</text>'
s += '<text x="200" y="178" '+T+' font-size="24" font-weight="bold" fill="#F1F5F9">项目背景</text>'
s += '<text x="200" y="212" '+W+' font-size="18" fill="#94A3B8">智能家居的碎片化困局</text>'
s += '<rect x="680" y="130" width="500" height="110" rx="12" fill="#141B2D" stroke="#F59E0B" stroke-width="1"/>'
s += '<text x="720" y="190" '+T+' font-size="28" font-weight="bold" fill="#F59E0B">02</text>'
s += '<text x="780" y="178" '+T+' font-size="24" font-weight="bold" fill="#F1F5F9">系统架构</text>'
s += '<text x="780" y="212" '+W+' font-size="18" fill="#94A3B8">四层模型 + 数据流设计</text>'
s += '<rect x="100" y="270" width="500" height="110" rx="12" fill="#141B2D" stroke="#22C55E" stroke-width="1"/>'
s += '<text x="140" y="330" '+T+' font-size="28" font-weight="bold" fill="#22C55E">03</text>'
s += '<text x="200" y="318" '+T+' font-size="24" font-weight="bold" fill="#F1F5F9">核心功能</text>'
s += '<text x="200" y="352" '+W+' font-size="18" fill="#94A3B8">8大功能 + 硬件配置 + 场景联动</text>'
s += '<rect x="680" y="270" width="500" height="110" rx="12" fill="#141B2D" stroke="#06B6D4" stroke-width="1"/>'
s += '<text x="720" y="330" '+T+' font-size="28" font-weight="bold" fill="#06B6D4">04</text>'
s += '<text x="780" y="318" '+T+' font-size="24" font-weight="bold" fill="#F1F5F9">代码实现</text>'
s += '<text x="780" y="352" '+W+' font-size="18" fill="#94A3B8">MQTT + AI + 数据库 + API</text>'
s += '<rect x="340" y="410" width="600" height="110" rx="12" fill="#141B2D" stroke="#EF4444" stroke-width="1"/>'
s += '<text x="380" y="470" '+T+' font-size="28" font-weight="bold" fill="#EF4444">05</text>'
s += '<text x="440" y="458" '+T+' font-size="24" font-weight="bold" fill="#F1F5F9">项目成果</text>'
s += '<text x="440" y="492" '+W+' font-size="18" fill="#94A3B8">测试结果 + 项目小结</text>'
s += '<text x="1230" y="700" text-anchor="end" '+W+' font-size="12" fill="#4B5563">02</text></svg>'
w("02_toc.svg", s)

print("P01-P02 done")
