# =========================
# Wallpaper Manager (Windows)
# =========================

import os, json, time, threading, ctypes, requests, traceback
from io import BytesIO
from random import choice
from datetime import datetime
from PIL import Image
import tkinter as tk
from tkinter import ttk, messagebox
import pystray
from pystray import MenuItem as item

# -------------------------
# PATHS
# -------------------------
BASE_DIR = os.path.join(os.path.expanduser("~"), "WallpaperApp")
SAVE_DIR = os.path.join(BASE_DIR, "wallpapers")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
LOG_FILE = os.path.join(BASE_DIR, "log.txt")

os.makedirs(SAVE_DIR, exist_ok=True)

# -------------------------
# DEFAULT CONFIG
# -------------------------
DEFAULT_CONFIG = {
    "keywords": ["anime", "ghibli", "abstract"],
    "interval_minutes": 60,
    "download_count": 3,
    "max_images": 30,
    "set_wallpaper": True
}

# -------------------------
# CONFIG
# -------------------------
def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    with open(CONFIG_FILE, "r", encoding="utf8") as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf8") as f:
        json.dump(cfg, f, indent=2)

cfg = load_config()

# -------------------------
# LOGGING
# -------------------------
def log(msg):
    ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
    with open(LOG_FILE, "a", encoding="utf8") as f:
        f.write(ts + msg + "\n")
    print(msg)

# -------------------------
# WALLPAPER SET
# -------------------------
def set_wallpaper(path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

# -------------------------
# WALLPAPER DOWNLOAD
# -------------------------
def get_api_url(keyword):
    return f"https://wallhaven.cc/api/v1/search?q={keyword}&purity=100&sorting=random&atleast=1920x1080"

def next_filename():
    files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".jpg")]
    nums = [int(f.split("_")[1].split(".")[0]) for f in files if "_" in f]
    n = max(nums) + 1 if nums else 1
    return f"wallpaper_{str(n).zfill(3)}.jpg"

def cleanup():
    files = sorted(
        [os.path.join(SAVE_DIR, f) for f in os.listdir(SAVE_DIR) if f.endswith(".jpg")],
        key=os.path.getctime
    )
    while len(files) > cfg["max_images"]:
        os.remove(files.pop(0))

def download_once():
    kw = choice(cfg["keywords"])
    log(f"Keyword: {kw}")

    r = requests.get(get_api_url(kw), timeout=20).json()
    if not r.get("data"):
        return

    img_url = choice(r["data"])["path"]
    img = Image.open(BytesIO(requests.get(img_url).content))

    if img.mode == "RGBA":
        img = img.convert("RGB")

    w, h = img.size
    if w <= h:
        return

    path = os.path.join(SAVE_DIR, next_filename())
    img.save(path, "JPEG")
    log(f"Saved {path}")

    if cfg["set_wallpaper"]:
        set_wallpaper(path)

    cleanup()

# -------------------------
# BACKGROUND ENGINE
# -------------------------
class Engine(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.stop_event = threading.Event()

    def run(self):
        log("Engine started")
        while not self.stop_event.is_set():
            try:
                for _ in range(cfg["download_count"]):
                    download_once()
            except Exception as e:
                log(str(e))
            self.stop_event.wait(cfg["interval_minutes"] * 60)
        log("Engine stopped")

    def stop(self):
        self.stop_event.set()

engine = None

# -------------------------
# GUI
# -------------------------
root = tk.Tk()
root.title("Wallpaper Manager")
root.geometry("420x360")

def start_engine():
    global engine
    if engine and engine.is_alive():
        return
    engine = Engine()
    engine.start()
    status.set("Running")

def stop_engine():
    global engine
    if engine:
        engine.stop()
        engine = None
    status.set("Stopped")

def save_settings():
    try:
        cfg["interval_minutes"] = int(interval.get())
        cfg["download_count"] = int(count.get())
        save_config(cfg)
        messagebox.showinfo("Saved", "Settings saved")
    except:
        messagebox.showerror("Error", "Invalid settings")

ttk.Label(root, text="Interval (minutes)").pack()
interval = ttk.Entry(root)
interval.insert(0, cfg["interval_minutes"])
interval.pack()

ttk.Label(root, text="Images per run").pack()
count = ttk.Entry(root)
count.insert(0, cfg["download_count"])
count.pack()

status = tk.StringVar(value="Stopped")
ttk.Label(root, textvariable=status).pack(pady=10)

ttk.Button(root, text="Start", command=start_engine).pack(fill="x")
ttk.Button(root, text="Stop", command=stop_engine).pack(fill="x")
ttk.Button(root, text="Save Settings", command=save_settings).pack(fill="x")

# -------------------------
# SYSTEM TRAY
# -------------------------
def show_app(icon, item):
    root.after(0, root.deiconify)

def quit_app(icon, item):
    stop_engine()
    icon.stop()
    root.destroy()

icon = pystray.Icon(
    "WallpaperManager",
    Image.new("RGB", (64, 64), "black"),
    menu=pystray.Menu(
        item("Show", show_app),
        item("Start", lambda i, x: start_engine()),
        item("Stop", lambda i, x: stop_engine()),
        item("Exit", quit_app),
    )
)

def hide_to_tray():
    root.withdraw()
    threading.Thread(target=icon.run, daemon=True).start()

root.protocol("WM_DELETE_WINDOW", hide_to_tray)

root.mainloop()
