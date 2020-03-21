# ============================================================================================
import os
import re
import eyed3
from moviepy.editor import *
from pytube.cli import on_progress
from pytube import YouTube, Playlist
import concurrent.futures
import pyfiglet
# ============================================================================================


class Downloader:

    def __init__(self, videos_dir=None):
        self.videos_dir = videos_dir

    def download_song(self, url):

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
        print(f'[+]Downloading playlist, total: {len(pl)} songs')

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(
                self.download_song, pl, chunksize=5)

    def clean_up(self):
        folder = os.listdir(self.videos_dir)

        for item in folder:
            if item.endswith(".mp4"):
                print(
                    f'[*]Removing file: {os.path.join(self.videos_dir, item)}')
                os.remove(os.path.join(self.videos_dir, item))
            elif item.endswith(".mp3"):
                info = item.split("-")
                audiofile = eyed3.load(os.path.join(self.videos_dir, item))
                audiofile.tag.artist = info[0].split('.')[0]
                audiofile.tag.title = info[1]

                audiofile.tag.save()


# ============================================================================================


def menu():
    print('1.Download a song')
    print('2.Download a playlist')
    print('3.Exit')
    print('------------------------------------------------------------')

    option = 0

    while(option != 1 and option != 2 and option != 3):
        option = int(input('Select an option:'))

    return option
# ============================================================================================


def main():
    ascii_banner = pyfiglet.figlet_format('YTDownload')
    print(ascii_banner)
    print('Developed by: Konstantinos Bourantas')
    print('------------------------------------------------------------')

    option = menu()

    print('------------------------------------------------------------')

    if option == 3:
        sys.exit(1)

    url = input("Enter url:")

    if option == 1:
        downloader = Downloader()
        downloader.download_song(url)
    elif option == 2:
        videos_dir = input("Enter folder name:")
        downloader = Downloader(videos_dir)

        try:
            os.mkdir(videos_dir)
        except OSError:
            print("[-]Creation of the directory \"%s\" failed" % videos_dir)
        else:
            print("[+]Successfully created the directory \"%s\" " % videos_dir)

        downloader.download_playlist(url)

        downloader.clean_up()


# ============================================================================================


if __name__ == "__main__":
    main()
