"""
Gemini Vision 识图脚本
用法：
  python gemini_vision.py <图片路径或URL> [prompt]

示例：
  python gemini_vision.py C:\Users\xinggui\Pictures\photo.jpg "描述这张图片"
  python gemini_vision.py https://example.com/photo.jpg "提取图中的文字"
"""
import sys
import os
from pathlib import Path

# ── 读取 .env ──
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY or API_KEY in ("your-gemini-api-key", ""):
    print("❌ 请先在 .env 中填入 GEMINI_API_KEY")
    print("   编辑 F:\\reasonix\\skill\\ppt-master\\.env，取消注释并填入你的 Key：")
    print("   GEMINI_API_KEY=你的Key")
    sys.exit(1)

# ── 导入 google-genai ──
try:
    from google import genai
except ImportError:
    print("❌ 缺少 google-genai 库，正在安装...")
    os.system(f"{sys.executable} -m pip install google-genai")
    from google import genai

client = genai.Client(api_key=API_KEY)

def load_image(path_or_url):
    """支持本地文件路径和 URL"""
    if path_or_url.startswith(("http://", "https://")):
        import requests
        from io import BytesIO
        resp = requests.get(path_or_url, timeout=30)
        resp.raise_for_status()
        from PIL import Image
        return Image.open(BytesIO(resp.content))
    else:
        from PIL import Image
        return Image.open(path_or_url)

def main():
    if len(sys.argv) < 2:
        print("用法: python gemini_vision.py <图片路径/URL> [prompt]")
        sys.exit(1)

    image_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else "请详细描述这张图片的内容"

    print(f"📷 加载图片: {image_path}")
    image = load_image(image_path)
    print(f"   ✓ {image.size}")

    print(f"💬 提问: {prompt}")
    print("⏳ 调用 Gemini...")
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[prompt, image]
    )
    print(f"\n✅ 回答:\n{response.text}")

if __name__ == "__main__":
    main()
