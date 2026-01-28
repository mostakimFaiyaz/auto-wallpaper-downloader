# Wallpaper Auto Downloader

A very lightweight Windows desktop application built with **Python** that automatically downloads a new wallpaper **every hour** and sets it as the system background.

The app is converted into an **EXE file** and added to **Windows Startup**, so it launches automatically when the PC boots.

---

## 🚀 Features

* ⏰ Automatically downloads **1 new wallpaper every hour**
* 🖼️ Sets the downloaded image as **desktop background**
* 🖥️ Simple **GUI interface**
* 🔁 Runs silently in the **background** after activation
* ⚡ Starts automatically with Windows using `shell:startup`

---

## 🛠️ How It Works

1. The application is written in **Python**
2. It is converted to an **EXE** using a Python packaging tool (e.g., PyInstaller)
3. The EXE file is placed in:

   ```
   shell:startup
   ```
4. When the PC starts:

   * The app GUI opens automatically
   * Click **Start** to enable the wallpaper changer
   * The app continues running in the background

---

## 📦 Installation

1. Download the EXE file from the repository or release section
2. Press **Win + R**, type:

   ```
   shell:startup
   ```
3. Copy the EXE file into the Startup folder
4. Restart your PC

---

## ▶️ Usage

1. Start your PC
2. The app GUI will open automatically
3. Click the **Start** button
4. The app will:

   * Download a new wallpaper every hour
   * Automatically set it as your desktop background

---

## 🧑‍💻 Author

**Mostakim Faiyaz**

---

## 📜 License

This project is open-source. Feel free to use, modify, and distribute it.

---

⭐ If you like this project, consider giving it a star on GitHub!
