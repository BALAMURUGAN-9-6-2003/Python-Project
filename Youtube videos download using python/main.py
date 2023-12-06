import tkinter as tk
from tkinter import messagebox
from pytube import YouTube
import os

class YouTubeDownloaderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("YouTube Downloader")

        self.url_label = tk.Label(master, text="Enter YouTube URL:")
        self.url_label.pack(pady=5)

        self.url_entry = tk.Entry(master, width=40)
        self.url_entry.pack(pady=10)

        self.get_info_button = tk.Button(master, text="Get Video Info", command=self.get_video_info)
        self.get_info_button.pack(pady=15)

        self.download_button = tk.Button(master, text="Download Video", command=self.download_video)
        self.download_button.pack(pady=15)

    def get_video_info(self):
        url = self.url_entry.get()
        if url:
            try:
                video = YouTube(url)
                info = f"Title: {video.title}\nThumbnail URL: {video.thumbnail_url}\nViews: {video.views}\n"
                messagebox.showinfo("Video Information", info)
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please enter a YouTube URL.")

    def download_video(self):
        url = self.url_entry.get()
        if url:
            try:
                video = YouTube(url)
                stream = video.streams.get_highest_resolution()

                # Set download path to the directory of the current script
                script_directory = os.path.dirname(os.path.abspath(__file__))
                video_title = video.title
                file_path = os.path.join(script_directory, f"{video_title}.mp4")

                stream.download(output_path=script_directory)
                
                notification_title = "Download Complete"
                notification_message = f"Video '{video_title}' has been downloaded successfully."
                messagebox.showinfo(
                    title=notification_title,
                    message=notification_message,
                    # ="YouTube Downloader"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please enter a YouTube URL.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("350x250")
    root.resizable(False,False)
    app = YouTubeDownloaderApp(root)
    root.mainloop()
