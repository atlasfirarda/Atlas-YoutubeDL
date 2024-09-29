import os
import logging
import subprocess

from inquirer import List, Text, prompt
from yt_dlp import YoutubeDL
from colorTexts import red, green, yellow


class Download:
    def __init__(
        self,
        output,
        ffmpegPath: str = None,
    ):
        self.output = output
        self.ffmpegPath = ffmpegPath

        os.system("cls" if os.name == "nt" else "clear")
        print(self.banner())

        if self.ffmpegPath is None:
            toPrint = f"{red("ERR:")} No FFmpeg path provided, exiting.."
            logging.info(toPrint)
            print(toPrint)
            exit(404)

        questionVid = [
            Text("videoUrl", message="Enter the video link you want download to"),
        ]

        answerVid = prompt(questionVid)
        self.videoLink = answerVid["videoUrl"]
        if not self.videoLink == "" and (
            str(self.videoLink).startswith("https://www.youtube.com/watch?v=") or str(self.videoLink).startswith(
            "youtube.com/watch?v=") or str(self.videoLink).startswith("https://youtube.com/watch?v=") or str(
            self.videoLink).startswith("https://youtu.be/")):
            toPrint = f"\n{green("SUC:")} Entered link: {yellow(self.videoLink)}"
            logging.info(toPrint)
            print(toPrint)
        else:
            toPrint = f"\n{red('ERR:')} The entered video link is invalid, exiting...\n"
            logging.info(toPrint)
            print(toPrint)
            exit(1)

        resolutions = self.listResolutions()

        questionRes = [
            List(
                "resolution",
                message="Select the resolution you want to download (width x height)",
                choices=[f"{w}x{h}" for w, h in resolutions],
            ),
        ]

        os.system("cls" if os.name == "nt" else "clear")
        print(self.banner())
        answerRes = prompt(questionRes)

        if not answerVid["videoUrl"]:
            os.system("cls" if os.name == "nt" else "clear")
            print(self.banner())
            toPrint = f"{red('ERR:')} No video link provided, exiting...\n"
            logging.info(toPrint)
            print(toPrint)
            exit(1)
        if not answerRes["resolution"]:
            os.system("cls" if os.name == "nt" else "clear")
            print(self.banner())
            toPrint = f"{red('ERR:')} No resolution is selected, exiting...\n"
            logging.info(toPrint)
            print(toPrint)
            exit(1)

        self.resolution = answerRes["resolution"]
        self.width, self.height = map(int, self.resolution.split("x"))

        toPrint = f"{green("SUC:")} Selected Resolution: {yellow(self.resolution)}"
        logging.info(toPrint)
        print(toPrint)

        self.downloadVideo()

    def banner(self):
        banner = r"""
 _____  _____  __     _____  _____       __ __  _____  ____   __
|  _  ||_   _||  |   |  _  ||   __| ___ |  |  ||_   _||    \ |  |
|     |  | |  |  |__ |     ||__   ||___||_   _|  | |  |  |  ||  |__
|__|__|  |_|  |_____||__|__||_____|       |_|    |_|  |____/ |_____|

"""

        return green(banner)

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

        if not os.path.exists(os.path.abspath(os.path.join("downloads"))):
            os.mkdir(os.path.abspath(os.path.join("downloads")))

        if not os.path.exists(self.output):
            with YoutubeDL(options) as ytdl:
                os.system("cls" if os.name == "nt" else "clear")
                print(self.banner())
                ytdl.download([self.videoLink])
                toPrint = f"{green("SUC: ")}the '{yellow(self.getName())}' is downloaded to '{yellow(self.outputDir)}'\n"
                logging.info(toPrint)
                print(toPrint)
                subprocess.Popen(['explorer', self.outputDir])
                print(f"{yellow("**")} press a key to exit..")
                input()
                exit(1)
        else:
            os.system("cls" if os.name == "nt" else "clear")
            print(self.banner())
            toPrint = f"{red('ERR:')} the '{green(self.getName())}' is already exists at '{green(self.outputDir)}' skipping..\n"
            logging.info(toPrint)
            print(toPrint)
            subprocess.Popen(['explorer', self.outputDir])
            input()
            print(f"{yellow("**")} press a key to exit..")
            exit(1)

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
