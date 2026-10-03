import glob

color_map = {
    '#0F172A': '#F8FAFC', '#1E293B': '#FFFFFF',
    '#0F2744': '#DBEAFE', '#2C1A0A': '#FEF3C7',
    '#1A2E0A': '#DCFCE7', '#0A1A0A': '#DCFCE7',
    '#1A3A1A': '#BBF7D0', '#3D2A0A': '#FEF3C7',
    '#38BDF8': '#2563EB', '#F59E0B': '#D97706',
    '#06B6D4': '#0284C7', '#E2E8F0': '#1E293B',
    '#94A3B8': '#475569', '#64748B': '#64748B',
    '#334155': '#CBD5E1', '#34D399': '#16A34A',
    '#EF4444': '#DC2626', '#111827': '#FFFFFF',
    '#1E3A5F': '#BFDBFE',
}

svg_dir = r'F:\reasonix\xiangmu\jiaju\projects\esp32_smart_home\svg_output'
for fpath in glob.glob(svg_dir + '\\*.svg'):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in color_map.items():
        content = content.replace(old, new)
    content = content.replace('stop-color="#BFDBFE"', 'stop-color="#DBEAFE"')
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Done: {fpath}')
