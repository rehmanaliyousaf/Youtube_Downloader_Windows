import customtkinter as ctk
from tkinter import messagebox, filedialog
import yt_dlp
import threading
import os
import sys
import socket
import time


class ModernYoutubeDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ultimate YouTube Downloader by RAYTECH")
        self.geometry("620x680")

        self.is_cancelled = False
        self.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(self, text="YouTube Downloader", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0,
                                                                                                     pady=20)

        # URL Input
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Paste YouTube URL here...", width=500)
        self.url_entry.grid(row=1, column=0, pady=10)

        # Save Path Selection
        self.path_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.path_frame.grid(row=2, column=0, padx=20, pady=10)

        # Default to user's Downloads folder
        default_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.save_path_var = ctk.StringVar(value=default_path)

        self.path_entry = ctk.CTkEntry(self.path_frame, textvariable=self.save_path_var, width=380)
        self.path_entry.pack(side="left", padx=(0, 10))

        self.browse_btn = ctk.CTkButton(self.path_frame, text="Browse", width=100, command=self.browse_folder)
        self.browse_btn.pack(side="left")

        # Resolution Selection
        ctk.CTkLabel(self, text="Select Quality:").grid(row=3, column=0, pady=(10, 0))
        self.res_var = ctk.StringVar(value="Best Available")
        self.res_combo = ctk.CTkComboBox(self, values=["Best Available", "1080p", "720p", "480p", "360p"],
                                         variable=self.res_var)
        self.res_combo.grid(row=4, column=0, pady=10)

        # Audio Toggle
        self.audio_var = ctk.BooleanVar(value=False)
        self.audio_check = ctk.CTkCheckBox(self, text="Audio Only (MP3)", variable=self.audio_var)
        self.audio_check.grid(row=5, column=0, pady=10)

        # Status & Progress
        self.status_label = ctk.CTkLabel(self, text="Ready to download", font=ctk.CTkFont(size=13))
        self.status_label.grid(row=6, column=0, pady=(20, 0))

        self.progress_bar = ctk.CTkProgressBar(self, width=500)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=7, column=0, pady=10)

        # Control Buttons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=8, column=0, pady=20)

        self.download_btn = ctk.CTkButton(self.btn_frame, text="Download / Resume", command=self.start_download_thread)
        self.download_btn.pack(side="left", padx=10)

        self.cancel_btn = ctk.CTkButton(self.btn_frame, text="Cancel", fg_color="#c42b1c", hover_color="#a82318",
                                        state="disabled", command=self.cancel_download)
        self.cancel_btn.pack(side="left", padx=10)

    def browse_folder(self):
        selected_path = filedialog.askdirectory()
        if selected_path:
            self.save_path_var.set(selected_path)

    def is_internet_available(self):
        """Check internet connectivity by pinging Google DNS."""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def get_ffmpeg_path(self):
        """Find bundled ffmpeg.exe for PyInstaller or local use."""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, "ffmpeg.exe")
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg.exe")

    def progress_hook(self, d):
        if self.is_cancelled:
            raise Exception("CANCELLED_BY_USER")

        if d['status'] == 'downloading':
            p_str = d.get('_percent_str', '0%').replace('%', '').strip()
            try:
                progress = float(p_str) / 100
                speed = d.get('_speed_str', 'N/A')
                self.after(0, lambda: self.progress_bar.set(progress))
                self.after(0, lambda: self.status_label.configure(text=f"Downloading: {p_str}% | Speed: {speed}"))
            except:
                pass

    def cancel_download(self):
        self.is_cancelled = True
        self.status_label.configure(text="Cancelling... please wait.")

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            return messagebox.showwarning("Error", "Please enter a valid URL.")

        self.is_cancelled = False
        self.download_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.progress_bar.set(0)

        thread = threading.Thread(target=self.run_download_loop, args=(url,), daemon=True)
        thread.start()

    def run_download_loop(self, url):
        res_choice = self.res_var.get().replace("p", "")
        save_dir = self.save_path_var.get()
        ffmpeg_bin = self.get_ffmpeg_path()
        ffmpeg_dir = os.path.dirname(ffmpeg_bin) if os.path.exists(ffmpeg_bin) else None

        opts = {
            'progress_hooks': [self.progress_hook],
            'continuedl': True,  # Force resume support
            'ffmpeg_location': ffmpeg_dir,  # Portable FFmpeg path
            'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),
            'fragment_retries': 20,  # Built-in retries for small hiccups
            'retries': 10,
        }

        if self.audio_var.get():
            opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
            })
        else:
            fmt = 'bestvideo+bestaudio/best' if res_choice == "Best Available" else f'bestvideo[height<={res_choice}]+bestaudio/best'
            opts.update({'format': fmt, 'merge_output_format': 'mp4'})

        while not self.is_cancelled:
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])

                # Success
                self.after(0, lambda: messagebox.showinfo("Done", "Download completed successfully!"))
                self.after(0, lambda: self.status_label.configure(text="Finished"))
                break

            except Exception as e:
                if "CANCELLED_BY_USER" in str(e) or self.is_cancelled:
                    self.after(0, lambda: self.status_label.configure(text="Download Cancelled."))
                    break

                # Handle Internet Loss
                self.after(0, lambda: self.status_label.configure(text="Connection lost. Waiting for internet..."))

                # Check for internet every 5 seconds
                while not self.is_internet_available() and not self.is_cancelled:
                    time.sleep(5)

                if self.is_cancelled: break
                self.after(0, lambda: self.status_label.configure(text="Internet restored. Resuming download..."))
                time.sleep(2)  # Brief pause before restarting yt-dlp

        self.after(0, lambda: self.download_btn.configure(state="normal"))
        self.after(0, lambda: self.cancel_btn.configure(state="disabled"))


if __name__ == "__main__":
    app = ModernYoutubeDownloader()
    app.mainloop()
