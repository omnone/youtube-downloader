# ============================================================================================
import os
import re
from moviepy.editor import *
from pytube.cli import on_progress
from pytube import YouTube, Playlist
import concurrent.futures

# ============================================================================================


class Downloader:

    def __init__(self, videos_dir=None):
        self.videos_dir = videos_dir

    def song_download(self, url):

        yt = YouTube(url, on_progress_callback=on_progress)

        stream = yt.streams.first()

        # download and save to the computer path.
        stream.download(os.getcwd()+'\\'+self.videos_dir)

        video_name = os.getcwd()+'\\'+self.videos_dir+"\\"+stream.title+".mp4"
        song_name = os.getcwd()+'\\'+self.videos_dir+"\\"+stream.title+".mp3"

        video = VideoFileClip(video_name)
        video.audio.write_audiofile(song_name)

    def download_playlist(self, playlist=None):

        pl = Playlist(playlist)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(
                self.song_download, pl, chunksize=5)

# ============================================================================================


def main():
    url = input("Enter url:")

    videos_dir = input("Enter folder name:")
    downloader = Downloader(videos_dir)

    try:
        os.mkdir(videos_dir)
    except OSError:
        print("[-]Creation of the directory \"%s\" failed" % videos_dir)
    else:
        print("[+]Successfully created the directory \"%s\" " % videos_dir)

    downloader.download_playlist(url)

# ============================================================================================


if __name__ == "__main__":
    main()
