# 默启未来 —— ESP 智能家居系统

智能家居演示系统三合一：**ESP32 固件**（MicroPython）+ **家居中控**（FastAPI）+ **Web Dashboard**。接收唇语识别结果，翻译成灯/风扇等设备的控制指令。

> 隶属"默启未来"项目 | 唇语后端：[lip-reading-backend](https://github.com/Prorroues/lip-reading-backend) | 眼镜 APP：[lip-reading-glasses-app](https://github.com/Prorroues/lip-reading-glasses-app)

## 系统架构

```
唇语后端(:24060) --/recognition/latest--> 家居中控(:8000) --MQTT--> ESP32 执行器
                                              |
                                              +--> Web Dashboard (浏览器)
                                              +--> SQLite 数据存储
```

- `esp32/`：MicroPython 固件，订阅 MQTT 指令，控制风扇、RGB 灯、6 路房间灯
- `server/`：FastAPI 中控，轮询唇语识别结果、词表匹配（`lip_matcher.py`）、MQTT 桥接、REST API、WebSocket、语音助手（可选 DeepSeek + MiniMax）
- `web/`：纯 HTML Dashboard（零依赖）

## 快速开始

### 1. 安装 Mosquitto（MQTT Broker）

从 [mosquitto.org/download](https://mosquitto.org/download/) 下载安装并启动服务（监听 1883）。

### 2. 启动家居中控

```bash
# Windows 一键启动（自动检查 Mosquitto、装依赖、起服务、开浏览器）
start.bat
# 或手动
python start.py
```

启动后访问：
- Dashboard: http://localhost:8000
- API 文档: http://localhost:8000/docs

### 3. 刷入 ESP32 固件

```bash
cd esp32
cp config.example.py config.py   # 填入你的 WiFi 和 MQTT 地址
# 用 Thonny / mpremote 把 main.py、boot.py、config.py、umqttsimple.py、hzk16s 上传到 ESP32
```

### 4. 可选配置

- `server/ai_config.json`：复制 `server/ai_config.example.json` 改名并填入 DeepSeek / MiniMax key，启用语音助手与 AI 分析（不配置也能用基础控制）
- 唇语联动：先启动 [lip-reading-backend](https://github.com/Prorroues/lip-reading-backend)（:24060），中控会自动每秒拉取识别结果

## 指令对照表（MQTT → ESP32）

| 指令 | 功能 | 指令 | 功能 |
|---|---|---|---|
| 1 / 3 | 开风扇 | 12 / 13 | 床下前灯 开/关 |
| 2 / 4 | 关风扇 | 14 / 15 | 床头灯 开/关 |
| 6 | RGB 暖色 | 16 / 17 | 上左灯 开/关 |
| 7 | 关闭 RGB | 18 / 19 | 厕所灯 开/关 |
| 8 / 9 | 柜子灯 开/关 | 20 | RGB 自动/暖色 |
| 10 / 11 | 床后灯 开/关 | 21 (JSON) | 自定义 RGB 颜色 |

唇语控制示例：说"打开风扇"→ 唇语后端识别 → 中控匹配 → 自动下发指令 1。

## 文档

- [docs/pins.md](docs/pins.md)：ESP32 引脚对照表（硬件接线）
- [docs/roadmap.md](docs/roadmap.md)：项目进化路线
- `esp32/legacy/`：带 DHT11 温湿度传感器的旧版固件（留档）
- `tools/legacy-scripts/`：Dashboard/SVG 生成脚本（留档）

## 许可证

Apache License 2.0 — 详见 [LICENSE](LICENSE)。
