import re, glob, os

out = r"F:\reasonix\xiangmu\jiaju\projects\esp32_smart_home\svg_output"

# ── 1. Font size swap table ──
swaps = [
    # scene titles
    ('font-size="48" font-weight="bold" fill="#1E293B" text-anchor="middle"',
     'font-size="52" font-weight="bold" fill="#1E293B" text-anchor="middle"'),
    # chapter titles
    ('font-size="44" font-weight="bold" fill="#1E293B" text-anchor="middle">',
     'font-size="48" font-weight="bold" fill="#1E293B" text-anchor="middle">'),
    # page titles
    ('font-size="28" font-weight="bold"', 'font-size="32" font-weight="bold"'),
    # card subtitles (15-16 -> 18)
    ('font-size="15" font-weight="bold"', 'font-size="18" font-weight="bold"'),
    ('font-size="16" font-weight="bold"', 'font-size="18" font-weight="bold"'),
    # body text 13/14 -> 16
    ('font-size="13" fill', 'font-size="16" fill'),
    ('font-size="14" fill', 'font-size="16" fill'),
    # monospace 10/11 -> 13
    ('font-size="10" fill', 'font-size="13" fill', 'Consolas'),
    ('font-size="11" fill', 'font-size="13" fill', 'Consolas'),
    # annotation 11/12 -> 14
    ('font-size="11" fill="#94A3B8"', 'font-size="14" fill="#94A3B8"'),
    ('font-size="12" fill="#94A3B8"', 'font-size="14" fill="#94A3B8"'),
    ('font-size="11" fill="#94A3B8" text-anchor', 'font-size="14" fill="#94A3B8" text-anchor'),
    ('font-size="12" fill="#94A3B8" text-anchor', 'font-size="14" fill="#94A3B8" text-anchor'),
    # subtitle 24 -> 28
    ('font-size="24" fill="#475569" text-anchor="middle"', 'font-size="28" fill="#475569" text-anchor="middle"'),
]

for fname in sorted(os.listdir(out)):
    if not fname.endswith('.svg'): continue
    fpath = os.path.join(out, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    for swap in swaps:
        if len(swap) == 2:
            old, new = swap
            if old in content:
                content = content.replace(old, new)
                changed = True
        elif len(swap) == 3:
            old, new, keyword = swap
            if old in content and keyword in content:
                content = content.replace(old, new)
                changed = True

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    if changed:
        print(f'Font+: {fname}')
print('Font swap done')
