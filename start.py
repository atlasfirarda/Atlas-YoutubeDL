import subprocess
import logging
import sys
import os
import ctypes
from importlib.metadata import distribution, PackageNotFoundError

os.system("cls" if os.name == "nt" else "clear")


def setTitle(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)


setTitle(r"atlasata-code // YT-DL //")

try:
    from src.colorTexts import red, green, yellow
except ImportError:
    print(r"""
 _____  _____  __     _____  _____       __ __  _____  ____   __
|  _  ||_   _||  |   |  _  ||   __| ___ |  |  ||_   _||    \ |  |
|     |  | |  |  |__ |     ||__   ||___||_   _|  | |  |  |  ||  |__
|__|__|  |_|  |_____||__|__||_____|       |_|    |_|  |____/ |_____|
""")
    toPrint = "\nERR: the 'colored' is not installed. downloading..\n"
    logging.info(toPrint)
    print(toPrint)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colored"])
        toPrint = "SUC: the 'colored' is installed.\n"
        logging.info(toPrint)
        print(toPrint)
        from src.colorTexts import red, green, yellow
    except subprocess.CalledProcessError as e:
        toPrint = f"ERR: the 'colored' can't be installable."
        logging.info(toPrint)
        print(toPrint)
        sys.exit(404)

requirements = [
    "ansicon",
    "blessed",
    "Brotli",
    "certifi",
    "charset-normalizer",
    "colored",
    "editor",
    "idna",
    "inquirer",
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
    "yt-dlp"
]

for req in requirements:
    try:
        # Paket yüklüyse dağıtım bilgilerini al
        distribution(req)
    except PackageNotFoundError:
        os.system("cls" if os.name == "nt" else "clear")
        banner = r"""
 _____  _____  __     _____  _____       __ __  _____  ____   __
|  _  ||_   _||  |   |  _  ||   __| ___ |  |  ||_   _||    \ |  |
|     |  | |  |  |__ |     ||__   ||___||_   _|  | |  |  |  ||  |__
|__|__|  |_|  |_____||__|__||_____|       |_|    |_|  |____/ |_____|

"""
        print(green(banner))

        toPrint = f"{red('ERR:')} the '{yellow(req)}' is not installed! {green('downloading...')}"
        logging.info(toPrint)
        print(toPrint)

        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
            toPrint = f"{green('SUC:')} the '{yellow(req)}' is installed."
            logging.info(toPrint)
            print(toPrint)
        except subprocess.CalledProcessError as e:
            toPrint = f"{red('ERR:')} the '{yellow(req)}' can't be installable. Details: {e}"
            logging.info(toPrint)
            print(toPrint)

# Ana programı çalıştırma kodu
mainPath = os.path.abspath(os.path.join("src", "main.py"))
try:
    cmd = subprocess.Popen([sys.executable, mainPath], cwd=os.getcwd())
except Exception as e:
    print(f"ERR: Failed to run the main program. Details: {e}")
    logging.error(f"Failed to run the main program: {e}")
    sys.exit(404)
