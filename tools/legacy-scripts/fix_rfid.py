import re

# Fix P12
p12 = r"F:\reasonix\xiangmu\jiaju\projects\esp32_smart_home\svg_output\12_sensor.svg"
c = open(p12, "r", encoding="utf-8").read()
# Remove RC522 row and rfid_log
c = re.sub(r"<text x=\"100\" y=\"260\"[^>]*>[^<]*RC522[^<]*</text>", "", c)
c = re.sub(r"<text x=\"210\" y=\"260\"[^>]*>[^<]*SPI[^<]*</text>", "", c)
c = re.sub(r"<text x=\"320\" y=\"260\"[^>]*>[^<]*13\\.56[^<]*</text>", "", c)
c = re.sub(r"<text x=\"460\" y=\"260\"[^>]*>[^<]*rfid[^<]*</text>", "", c)
c = c.replace("RFID→开灯+暖色·", "")
c = c.replace("·rfid_log", "")
open(p12, "w", encoding="utf-8").write(c)
print("P12 OK")

# Fix P18
p18 = r"F:\reasonix\xiangmu\jiaju\projects\esp32_smart_home\svg_output\18_outlook.svg"
c = open(p18, "r", encoding="utf-8").read()
# Remove RFID card (first card, x=60 y=110, 270 wide)
c = re.sub(r"<rect x=\"60\" y=\"110\" width=\"270\" height=\"120\"[^>]*>.*?</text>", "", c, flags=re.DOTALL)
c = c.replace("RFID", "")
# Reposition 3 cards evenly (gaps cleaned)
c = c.replace('x="360" y="110"', 'x="140" y="110"')
c = c.replace('x="660" y="110"', 'x="500" y="110"')
c = c.replace('x="960" y="110"', 'x="860" y="110"')
for old_x in ["495","795","1090"]:
    new_x = {"495":"275","795":"635","1090":"995"}[old_x]
    for y_val in ["150","180","200","222"]:
        c = c.replace(f'x="{old_x}" y="{y_val}"', f'x="{new_x}" y="{y_val}"')
open(p18, "w", encoding="utf-8").write(c)
print("P18 OK")
