import subprocess
import sys
import os
from importlib.metadata import distribution, PackageNotFoundError


class downloadRequirements:
    def __init__(self, req: str = "none"):
        self.req = req

    def checkReq(self) -> bool:
        if not self.req == "none":
            try:
                distribution(self.req)
                return True
            except PackageNotFoundError:
                return False

    def downReq(self) -> bool:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", self.req])
            return True
        except subprocess.CalledProcessError:
            return False


requirements: list = [
    "ansicon",
    "blessed",
    "Brotli",
    "certifi",
    "charset-normalizer",
    "editor",
    "idna",
    "jinxed",
    "mutagen",
    "pycryptodomex",
    "readchar",
    "requests",
    "runs",
    "six",
    "urllib3",
    "wcwidth",
    "websockets",
    "xmod",
    "yt-dlp"]

total_req: int = requirements.__len__()
installed_req: int = 0
downloaded_req: int = 0
failed_req: int = 0

for requirement in requirements:

    down = downloadRequirements(requirement)

    if down.checkReq():
        installed_req += 1
        continue
    else:
        if down.downReq():
            downloaded_req += 1
            continue
        else:
            failed_req += 1
            continue
else:
    mainPath = os.path.abspath(os.path.join("src", "gui.py"))
    try:
        cmd = subprocess.Popen([sys.executable, mainPath], cwd=os.getcwd())
    except Exception:
        sys.exit(404)
