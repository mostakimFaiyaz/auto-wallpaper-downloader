import os
import requests
import ctypes
from PIL import Image
from io import BytesIO
from random import choice


API_KEYWORDS = ["ghibli", "movie", "abstract", "fantasy art", "TV series", "anime"]
SAVE_DIR = os.path.join(os.getcwd(), "wallpapers")
MAX_IMAGES = 30
DOWNLOAD_COUNT = 3


if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


def get_api_url(keyword):
    return f"https://wallhaven.cc/api/v1/search?q={keyword}&categories=111&purity=100&sorting=random&atleast=1920x1080"


def get_next_filename():
    nums = []
    for f in os.listdir(SAVE_DIR):
        if f.startswith("wallpaper_") and f.endswith(".jpg"):
            try:
                num = int(f.split("_")[1].split(".")[0])
                nums.append(num)
            except:
                continue
    next_num = max(nums) + 1 if nums else 1
    return f"wallpaper_{str(next_num).zfill(3)}.jpg"


def cleanup_folder():
    files = sorted([os.path.join(SAVE_DIR, f) for f in os.listdir(SAVE_DIR) if f.endswith(".jpg")], key=os.path.getctime)
    while len(files) > MAX_IMAGES:
        oldest = files.pop(0)
        os.remove(oldest)
        print(f"🗑 Deleted oldest file: {oldest}")


def download_wallpapers():
    for _ in range(DOWNLOAD_COUNT):
        keyword = choice(API_KEYWORDS)
        api_url = get_api_url(keyword)
        print(f"\n📥 Fetching with keyword: {keyword}")
        
        try:
            res = requests.get(api_url)
            data = res.json()

            if 'data' not in data or not data['data']:
                print("❌ No wallpapers found.")
                continue

            image_data = choice(data['data'])
            image_url = image_data['path']
            print(f"🔗 Downloading: {image_url}")

            img_res = requests.get(image_url)
            img = Image.open(BytesIO(img_res.content))
            filename = get_next_filename()
            img.save(os.path.join(SAVE_DIR, filename), "JPEG")
            print(f"✅ Saved as {filename}")

        except Exception as e:
            print(f"❌ Error: {e}")

    cleanup_folder()


download_wallpapers()