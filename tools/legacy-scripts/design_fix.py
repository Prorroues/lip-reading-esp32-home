import os, re

out = r"F:\reasonix\xiangmu\jiaju\projects\esp32_smart_home\svg_output"

# Decorative defs to prepend after first <svg ...> tag
DECO_DEFS = '''  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#F1F5F9"/>
    </linearGradient>
    <linearGradient id="accentBar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2563EB" stop-opacity="0"/><stop offset="50%" stop-color="#2563EB" stop-opacity="0.3"/><stop offset="100%" stop-color="#2563EB" stop-opacity="0"/>
    </linearGradient>
  </defs>
'''

for fname in os.listdir(out):
    if not fname.endswith('.svg'): continue
    fpath = os.path.join(out, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Replace solid white bg with gradient
    content = content.replace('<rect width="1280" height="720" fill="#FFFFFF"/>',
                              '<rect width="1280" height="720" fill="url(#bgGrad)"/>')
    
    # 2. Add decorative elements BEFORE last </svg>
    deco = '''  <circle cx="80" cy="80" r="60" fill="#2563EB" fill-opacity="0.03"/>
  <circle cx="1200" cy="650" r="80" fill="#2563EB" fill-opacity="0.02"/>
  <circle cx="1150" cy="120" r="4" fill="#2563EB" fill-opacity="0.08"/>
  <circle cx="1100" cy="160" r="2" fill="#2563EB" fill-opacity="0.05"/>
  <rect x="0" y="712" width="1280" height="8" fill="url(#accentBar)"/>'''
    
    # Insert defs after <svg ...>
    content = re.sub(r'(<svg [^>]+>)', r'\1\n' + DECO_DEFS, content, count=1)
    
    # Insert deco before </svg>
    content = content.replace('</svg>', deco + '\n</svg>')
    
    # 3. Remove RFID references
    content = re.sub(r'<circle cx="[0-9]+" cy="[0-9]+" r="4" fill="[^"]+"/>\s*<text [^>]*font-size="[0-9]+"[^>]*>.*RC522.*RFID.*</text>', '', content)
    content = re.sub(r'<text [^>]*>.*RC522.*RFID.*</text>', '', content)
    content = re.sub(r'<text [^>]*>.*RFID.*刷卡.*</text>', '', content)
    content = re.sub(r'<text [^>]*>.*RFID.*门禁.*</text>', '', content)
    content = re.sub(r'<text [^>]*>.*RFID卡片.*</text>', '', content)
    # Remove entire RFID bullet item (circle+text combo)
    content = re.sub(r'<circle cx="\d+" cy="\d+" r="\d+" fill="#EA580C"/>\s*<text x="\d+" y="\d+"[^>]*>RC522 RFID.*?</text>', '', content)
    content = re.sub(r'<circle cx="\d+" cy="\d+" r="\d+" fill="#EA580C"/>\s*<text x="\d+" y="\d+"[^>]*>RC522.*SPI.*</text>', '', content)
    content = re.sub(r'<text x="[0-9.]+" y="[0-9.]+"[^>]*font-size="10"[^>]*fill="#1E293B">RC522 RFID</text>\s*<text x="[0-9.]+" y="[0-9.]+"[^>]*font-size="10"[^>]*fill="#475569">SPI.*</text>', '', content)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Done: {fname}')

print('ALL DONE')
