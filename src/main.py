import os

from getYoutube import Download

folderPath = os.path.abspath(os.path.join("downloads"))
ffmpegPath = os.path.abspath(os.path.join("src", "ffmpeg", "ffmpeg.exe"))

download = Download(folderPath, ffmpegPath)
