# ============================================================================================

import Downloader as Downloader
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory
import subprocess
import threading
import os
import sys
import eyed3
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube.cli import on_progress
from pytube import YouTube, Playlist
import concurrent.futures

from time import sleep

HEIGHT = 500
WIDTH = 700

# ============================================================================================


class Application:
    def __init__(self, root, videos_dir=None):
        self.videos_dir = videos_dir

        self.songs = 0
        self.max_songs = 0

        root.minsize(500, 700)
        root.title('YTDownloader')

        self.frame = tk.Frame(root)
        self.frame.grid(row=0)

        # url stuff------------------------------------------------
        self.label_url = tk.Label(self.frame, font=40, text="URL:")
        self.label_url.grid(row=3, sticky=W, pady=30, padx=30)

        self.url_entry = tk.Entry(self.frame, font=40, width="50")
        self.url_entry.grid(row=3, column=1, columnspan=20, pady=30)

        self.btnDownload = tk.Button(self.frame, text="Download", font=40, height=1, width=8,
                                     command=lambda: self.btnDownload_callback(self.url_entry.get()))
        self.btnDownload.grid(row=3, column=21, sticky=E, padx=30, pady=30)

        # # save stuff-----------------------------------------------
        self.label_dir = tk.Label(self.frame, font=40, text="Path:")
        self.label_dir.grid(row=4, sticky=W, pady=1, padx=30)

        self.path_entry = tk.Entry(self.frame, font=40, width="50")
        self.path_entry.grid(row=4, column=1, columnspan=20, pady=1)

        self.btnChooseDir = tk.Button(self.frame, text="Folder", font=40, height=1, width=8,
                                      command=lambda: self.btnChooseDir_callback())
        self.btnChooseDir.grid(row=4, column=21, sticky=E, padx=30, pady=1)

        self.text = tk.Text(self.frame, height=30, width=70)
        self.text.config(state='normal')

        self.text.grid(row=7, column=0, columnspan=100,
                       pady=20, padx=30, sticky=W)

        self.progress = ttk.Progressbar(
            self.frame, orient="horizontal", length=520, mode="determinate")

        self.progress.grid(row=8, column=0, columnspan=100,
                           pady=20, padx=30, sticky=W)

        self.btnCancel = tk.Button(self.frame, text="Exit", font=40, height=1, width=8,
                                   command=lambda: sys.exit(1))
        self.btnCancel.grid(row=10, column=21, sticky=E, pady=10, padx=30)

        root.mainloop()
    # --------------------------------------------------------------------------------------------
    # Buttons callbacks functions

    def btnDownload_callback(self, url_entry):
        print(url_entry)

        if(self.videos_dir != None):
            self.text.insert(tk.INSERT, "Please wait....\n")
            my_thread = threading.Thread(
                target=self.download_playlist, args=(url_entry,))
            my_thread.start()
        else:
            dialog_title = 'Error'
            dialog_text = 'Please select folder!'
            tk.messagebox.showwarning(dialog_title, dialog_text)

    def btnChooseDir_callback(self):
        Tk().withdraw()
        path_to_save = askdirectory()
        print(path_to_save)
        self.path_entry.insert(tk.INSERT, path_to_save)
        self.videos_dir = path_to_save

    # --------------------------------------------------------------------------------------------

    # YOUTUBE STUFF
    def download_song(self, url):
        sleep(10)
        try:
            yt = YouTube(url, proxies={"http": "http://144.91.116.171:443"})
        except Exception as e:
            self.text.insert(tk.INSERT, f'[-]Connection Error! {str(e)}\n')

        print(f'[*]Downloading : {yt.title}')
        self.text.insert(tk.INSERT, f'[*]Downloading : {yt.title}\n')

        stream = yt.streams.filter(only_audio=True).first()

        # download and save to the selected path.
        try:
            stream.download(self.videos_dir)
        except:
            self.text.insert(
                tk.INSERT, f'[-]Downloading : {yt.title} failed\n')

        video_name = self.videos_dir+"\\"+stream.title+".mp4"
        song_name = self.videos_dir+"\\"+stream.title+".mp3"

        self.text.insert(tk.INSERT, f'[+]Converting : {yt.title} to mp3\n')

        video = VideoFileClip(video_name)
        video.audio.write_audiofile(song_name)

        self.songs += 1
        self.progress["value"] = self.songs
        video.close()
    # --------------------------------------------------------------------------------------------

    def download_playlist(self, playlist_url=None):

        pl = Playlist(playlist_url)

        self.progress["value"] = 0
        self.max_songs = len(pl)
        self.progress["maximum"] = len(pl)

        print(f'[+]Saving playlist at: {self.videos_dir}')
        print(f'[+]Downloading playlist, total: {len(pl)} songs')

        self.text.insert(
            tk.INSERT, f'[+]Saving playlist at: {self.videos_dir}\n')
        self.text.insert(
            tk.INSERT, f'[+]Downloading playlist, total: {len(pl)} songs\n')

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.download_song, pl, chunksize=5)

        print('[+]Download completed!')
        self.text.insert(tk.INSERT, '[+]Download completed!\n')

        tk.messagebox.showinfo("YTDownloader", "Download completed!")

        self.clean_up()
    # --------------------------------------------------------------------------------------------

    def clean_up(self):
        folder = os.listdir(self.videos_dir)

        for item in folder:
            if item.endswith(".mp4"):
                print(
                    f'[*]Removing file: {os.path.join(self.videos_dir, item)}')
                self.text.insert(
                    tk.INSERT, f'[*]Removing file: {os.path.join(self.videos_dir, item)}\n')
                os.remove(os.path.join(self.videos_dir, item))
            elif item.endswith(".mp3"):
                info = item.split("-")
                audiofile = eyed3.load(os.path.join(self.videos_dir, item))
                audiofile.tag.artist = info[0].split('.')[0]
                audiofile.tag.title = info[1]

                audiofile.tag.save()


# ============================================================================================
if __name__ == "__main__":
    root = tk.Tk()
    Application(root)
# ============================================================================================
