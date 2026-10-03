# ESP32 网络与 MQTT 配置
# 使用方法：复制本文件为 config.py（与 main.py 同目录），填入真实值后刷入设备
# config.py 已在 .gitignore 中，不会被提交

WIFI_SSID = "你的WiFi名称"
WIFI_PASSWORD = "你的WiFi密码"

# MQTT Broker 地址（通常是运行家居中控 server 的电脑 IP，须与眼镜、ESP32 同一局域网）
MQTT_BROKER = "192.168.137.1"
MQTT_PORT = 1883
