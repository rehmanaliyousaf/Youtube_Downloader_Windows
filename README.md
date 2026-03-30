# 🎬 YouTube Downloader

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)


A modern, fast, and user-friendly YouTube video downloader built with Python, using CustomTkinter (CTk) for GUI and yt-dlp for powerful downloading capabilities.
---
# 🚀 Features
- 🎥 Download YouTube videos in multiple resolutions
- 🎵 Extract and download audio (MP3)
- ⚡ Fast and reliable downloads using yt-dlp
- 🖥️ Modern GUI built with CustomTkinter
- 📂 Choose custom download location
- 📊 Progress bar and status updates
- 🔄 Resume option if internet connection failed.
- ✅ EXE build for Windows
## 🛠️ Tech Stack
- Python 3.x
- CustomTkinter (CTk) – Modern GUI framework
- yt-dlp – YouTube downloading backend

## 📸 Preview

<img width="463" height="379" alt="gui_main" src="https://github.com/user-attachments/assets/3e8b26f1-cf8c-4c48-92e6-98293f9465e4" />

# 📋 Prerequisites
To download videos in high resolution (1080p and above) or as MP3s, you must have FFmpeg installed on your system.
## For Windows Users (Recommended)
1. Download: Visit the [official FFmpeg builds page](https://www.ffmpeg.org/download.html) and download the ffmpeg-release-essentials.zip.
2. Extract: Extract the ZIP file to a permanent folder, for example: C:\ffmpeg.
- **Add to PATH:**
  - Search for "Edit the system environment variables" in your Start menu.
  - Click Environment Variables, find the Path variable under "System variables," and click Edit.
  - Click New and paste the path to your ffmpeg bin folder (e.g., C:\ffmpeg\bin).
  - Click OK on all windows and restart any open Command Prompts. 

## For macOS Users
Install easily via Homebrew: 
```bash
brew install ffmpeg
```

## For Linux Users (Ubuntu/Debian)
Use the apt package manager:
```bash
sudo apt update && sudo apt install ffmpeg
```
# 📦 Installation
1. Clone the Repository

```bash
- git clone https://github.com/rehmanaliyousaf/Youtube_Downloader_Windows.git
```
Go to the project folder

```bash
- cd Youtube_Downloader_Windows
```
2. Install dependencies

```bash
pip install -r requirements.txt
```
If you don't have a requirements file, install manually:

pip install customtkinter yt-dlp

# ▶️ Usage

### Run the application:

python app.py
Steps:
1. Paste the YouTube video URL
2. Select download format (Video/Audio)
3. Choose output folder
4. Click Download

Enjoy your file 🎉
# 📁 Project Structure
```text
youtube-downloader/
│
├── app.py
├── requirements.txt
└── README.md
└──ffmpeg.exe
└──ffplay.exe
└──ffprobe.exe
```
You can modify download settings inside your code:

- Default download path
- Video quality (e.g., 720p, 1080p)
- Audio format (mp3, wav)
# 🧠 Future Improvements
✅ Playlist download support

✅ Video preview thumbnail

✅ Download history

✅ Dark/Light theme toggle

✅ Multi-threaded downloads

# 🐞 Known Issues
- Some videos may fail due to YouTube restrictions
- Requires stable internet connection
- yt-dlp updates frequently (keep it updated)

## 🔄 Update yt-dlp

To ensure smooth downloads:

pip install -U yt-dlp

## 📜 License

This project is licensed under the MIT License.
---
## 🙌 Acknowledgements
Thanks to yt-dlp for powerful downloading support
Inspired by modern GUI applications
## 💡 Author

Rehman Ali Yousaf

GitHub: https://github.com/rehmanaliyousaf
