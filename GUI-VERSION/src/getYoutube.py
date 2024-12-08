import os
import subprocess

from yt_dlp import YoutubeDL


class Download:
    def __init__(
            self,
            output,
            videoLink: str = None,
            ffmpegPath: str = None,
    ):
        self.outputDir = None
        self.output = output
        self.ffmpegPath = ffmpegPath
        self.videoLink = videoLink
        self.width, self.height = self.listResolutions()[0]

        if self.ffmpegPath is None:
            toPrint = f"ERR: No FFmpeg path provided, exiting.."
            print(toPrint)
            exit(404)

        self.downloadVideo()

    def listResolutions(self):
        options = {
            "listformats": False,
            "quiet": True,
            "no_warnings": True,
        }

        with YoutubeDL(options) as ytdl:
            infoDict = ytdl.extract_info(self.videoLink, download=False)
            formats = infoDict.get("formats", [])
            resolutions = [
                (f.get("width"), f.get("height"))
                for f in formats
                if f.get("width") and f.get("height") and f.get("height") >= 240
            ]

            return sorted(set(resolutions), key=lambda x: x[1], reverse=True)

    def getName(self) -> str:
        options = {
            "listformats": False,
            "quiet": True,
            "no_warnings": True,
        }

        with YoutubeDL(options) as ytdl:
            infoDict = ytdl.extract_info(self.videoLink, download=False)
            title: str = infoDict.get("title")

            if r"\|^*-'&/" in title:
                title = title.replace(r'/\:*|?<>"', "")

            title = f"{title} ({self.width}x{self.height})"

            return title

    def downloadVideo(self):
        self.outputDir = self.output
        self.output = os.path.join(self.output, f"{self.getName()}.mp4")
        options = self.getOptions()

        if not os.path.exists(os.path.join(self.outputDir)):
            os.mkdir(os.path.join(self.outputDir))

        if not os.path.exists(self.output):
            with YoutubeDL(options) as ytdl:
                ytdl.download([self.videoLink])
                subprocess.Popen(['explorer', self.outputDir])
        else:
            subprocess.Popen(['explorer', self.outputDir])

    def getOptions(self):
        return {
            "format": f"bestvideo[height<={self.height}][width<={self.width}]+bestaudio[ext=m4a]/best[ext=mp4]",
            "outtmpl": self.output,
            "ffmpeg_location": os.path.dirname(self.ffmpegPath),
            "merge_output_format": "mp4",
            "quiet": True,
            "noplaylist": True,
            "no_warnings": True,
            "nocookies": True,
        }
