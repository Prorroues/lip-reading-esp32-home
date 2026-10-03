"""一键启动脚本 — 检查 Mosquitto → 安装依赖 → 启动后端 → 打开浏览器"""

import subprocess
import sys
import os
import time
import socket
import webbrowser
import traceback
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))

# ── Logging ────────────────────────────────────

def _ts():
    return datetime.now().strftime("%H:%M:%S")

def info(msg):
    print(f"[{_ts()}] {msg}")

def ok(msg):
    print(f"[{_ts()}] \033[92m[OK]\033[0m {msg}")

def warn(msg):
    print(f"[{_ts()}] \033[93m[!]\033[0m {msg}")

def fail(msg):
    print(f"[{_ts()}] \033[91m[FAIL]\033[0m {msg}")


# ── Checks ─────────────────────────────────────

def check_mosquitto():
    """检查 Mosquitto 是否在运行。"""
    info("检查 Mosquitto MQTT Broker...")

    # 方式0: 直接端口探测（最快最准）
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect(("127.0.0.1", 1883))
        s.close()
        ok("Mosquitto :1883 端口已监听")
        return True
    except Exception:
        s.close()

    # 方式1: Windows 服务
    try:
        result = subprocess.run(
            ["sc", "query", "mosquitto"],
            capture_output=True, text=True, timeout=5
        )
        if "RUNNING" in result.stdout:
            ok("Mosquitto 服务已在运行")
            return True
        elif "STOPPED" in result.stdout:
            warn("Mosquitto 服务已停止，尝试启动...")
            subprocess.run(["net", "start", "mosquitto"], capture_output=True, timeout=10)
            time.sleep(2)
            # 再次检查
            result2 = subprocess.run(
                ["sc", "query", "mosquitto"],
                capture_output=True, text=True, timeout=5
            )
            if "RUNNING" in result2.stdout:
                ok("Mosquitto 已启动")
                return True
    except FileNotFoundError:
        pass  # 非 Windows
    except Exception as e:
        warn(f"sc query 失败: {e}")

    # 方式2: 手动启动便携版
    mosq = os.path.join(ROOT, "tools", "mosquitto", "mosquitto.exe")
    mosq_conf = os.path.join(ROOT, "tools", "mosquitto", "mosquitto.conf")
    if os.path.exists(mosq) and os.path.exists(mosq_conf):
        warn(f"Mosquitto 未运行，启动便携版 ...")
        subprocess.Popen(
            [mosq, "-c", mosq_conf],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        time.sleep(2)
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.settimeout(2)
        try:
            s2.connect(("127.0.0.1", 1883))
            s2.close()
            ok("Mosquitto 后台已启动")
            return True
        except Exception:
            s2.close()

    fail("无法启动 Mosquitto")
    info("请手动安装并启动: https://mosquitto.org/download/")
    info("或命令行运行: mosquitto -v")
    return False


def install_deps():
    """安装 Python 依赖。"""
    req = os.path.join(ROOT, "server", "requirements.txt")
    if not os.path.exists(req):
        fail(f"文件不存在: {req}")
        return False

    info("安装 Python 依赖...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", req, "-q"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        ok("依赖安装完成")
        return True
    else:
        fail(f"依赖安装失败")
        if result.stderr:
            print(result.stderr.strip())
        return False


def check_python():
    """检查 Python 版本。"""
    info(f"Python: {sys.version}")
    if sys.version_info < (3, 10):
        warn(f"Python {sys.version_info.major}.{sys.version_info.minor} 较旧，建议 3.10+")

    # 检查关键模块是否可导入
    for mod in ["fastapi", "uvicorn", "paho.mqtt.client", "aiosqlite"]:
        try:
            __import__(mod)
        except ImportError:
            warn(f"缺少模块: {mod} (稍后自动安装)")


# ── Main ───────────────────────────────────────

def main():
    print("=" * 50)
    info("ESP32 IoT Server — 一键启动")
    print("=" * 50)

    check_python()

    # 检查文件结构
    required = [
        "server/main.py", "server/models.py", "server/mqtt_client.py",
        "server/routes.py", "server/ws.py", "server/exporter.py",
        "server/ai_analyzer.py", "server/ai_config.json", "server/requirements.txt",
        "web/dashboard.html",
    ]
    missing = [f for f in required if not os.path.exists(os.path.join(ROOT, f))]
    if missing:
        fail("缺少以下文件，请确认项目结构完整:")
        for m in missing:
            print(f"    - {m}")
        input("按任意键退出...")
        sys.exit(1)
    ok("项目文件完整")

    if not check_mosquitto():
        fail("Mosquitto 未就绪，退出")
        input("按任意键退出...")
        sys.exit(1)

    install_deps()

    info("启动 FastAPI 服务器...")
    print("-" * 50)
    info("仪表盘:   http://localhost:8000")
    info("API 文档: http://localhost:8000/docs")
    info("WebSocket: ws://localhost:8000/ws")
    print("-" * 50)

    # 等服务器就绪后再打开浏览器
    def _wait_and_open():
        import urllib.request
        info("等待服务器就绪...")
        for i in range(30):  # 最多等 30 秒
            try:
                urllib.request.urlopen("http://localhost:8000/api/health", timeout=1)
                ok("服务器就绪，打开浏览器")
                webbrowser.open("http://localhost:8000")
                return
            except Exception:
                time.sleep(1)
        warn("服务器启动超时，请手动打开 http://localhost:8000")
    import threading
    threading.Thread(target=_wait_and_open, daemon=True).start()

    # 杀掉占用 8000 端口的旧进程
    info("检查端口 8000 ...")
    try:
        result = subprocess.run(
            ["netstat", "-ano", "-p", "TCP"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.split("\n"):
            if ":8000" in line and "LISTENING" in line:
                parts = line.strip().split()
                pid = parts[-1]
                subprocess.run(["taskkill", "/f", "/pid", pid], capture_output=True)
                ok(f"已终止占用端口 8000 的进程 (PID {pid})")
                time.sleep(1)
                break
    except Exception:
        pass

    # 启动 uvicorn
    try:
        server_dir = os.path.join(ROOT, "server")
        os.chdir(server_dir)  # 确保 ../web 相对路径正确
        sys.path.insert(0, server_dir)  # 让 from models import 能找到
        import uvicorn
        uvicorn.run(
            "server.main:app",
            host="0.0.0.0", port=8000,
            log_level="info",
            app_dir=ROOT,
        )
    except KeyboardInterrupt:
        info("用户中断")
    except Exception as e:
        fail(f"服务器异常退出: {e}")
        traceback.print_exc()
        input("按任意键退出...")


if __name__ == "__main__":
    main()
