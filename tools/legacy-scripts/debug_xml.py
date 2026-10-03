c = open(r"F:\reasonix\xiangmu\jiaju\projects\esp32_smart_home\svg_output\04_sleep.svg", "rb").read()
lines = c.split(b'\n')
l10 = lines[9]
for i in range(715, 730):
    b = l10[i]
    ch = chr(b) if 32 <= b < 127 else "."
    print(f"  [{i}] 0x{b:02X} '{ch}'")
