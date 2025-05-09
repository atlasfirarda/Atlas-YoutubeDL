import datetime
import os
import pkg_resources
from pkg_resources import DistributionNotFound


class LoggerModule:
    def __init__(self, text: str = None):

        self.text = None
        self.level = None
        self.fileName = None
        self.filePath = None

        self.started = False

        if text:
            self.text = text

        self.appData = os.path.join(os.path.expanduser("~"), "AppData", "Local")
        self.mainPath = os.path.join(self.appData, "TheAtlas")

        self.currentPath = self.getCurrentPath()
        self.logPath = self.getLogPath()
        self.dateTime = datetime.date.today()

        if not self.createLogPath():
            return

        if not self.dateTime:
            return

    def showBanner(self) -> bool:
        try:
            logo = rf""" _____ _             _   _   _           
|_   _| |__   ___   / \ | |_| | __ _ ___ 
  | | | '_ \ / _ \ / _ \| __| |/ _` / __|
  | | | | | |  __// ___ \ |_| | (_| \__ \
  |_| |_| |_|\___/_/   \_\__|_|\__,_|___/
"""
            try:
                pkg_resources.get_distribution("colored")
                from modules.ColorModule import ColorModule

                module = ColorModule(logo)
                print(module.red())
            except DistributionNotFound:
                print(logo)
            return True

        except:
            return False

    def createLogPath(self) -> bool:

        logPath = self.getLogPath()

        if not os.path.exists(logPath):
            os.mkdir(logPath)
            return True

        return False

    def getLogPath(self, path: str = None) -> str:

        if path != None:
            if os.path.exists(path):
                return path

        currentPath = self.currentPath

        if currentPath == None:
            return None

        logPath = os.path.join(currentPath, "logs")

        return logPath

    def getCurrentPath(self) -> str:

        currentPath = os.path.dirname(os.path.abspath(__name__))

        if currentPath == self.mainPath:
            currentPath = self.mainPath

        if currentPath:
            return currentPath

        return None

    def createLogFile(self) -> bool:

        if not self.dateTime:
            return False

        try:
            dayTime: int = self.dateTime.day.__int__()
            monthTime: int = self.dateTime.month.__int__()
            yearTime: int = int(self.dateTime.year.__str__()[1:])
        except:
            return False

        if not self.logPath:
            return False

        self.fileName: str = f"{dayTime}-0{monthTime}-{yearTime}.log"
        self.filePath: str = os.path.join(self.logPath, self.fileName)

        if not os.path.exists(self.filePath):
            open(self.filePath, "x", encoding="UTF-8")

        return True

    def startLog(self) -> bool:
        if not self.fileName or not self.filePath:
            return False

        startText: str = "** LOGGING HAS BEEN STARTED **"

        with open(self.filePath, "w", encoding="UTF-8") as fileWrite:
            fileWrite.write(startText)

        self.started = True

        return True

    def stopLog(self) -> bool:
        if not self.fileName or not self.filePath or not self.started:
            return False

        stopText: str = "** LOGGING HAS BEEN STOPPED **"

        with open(self.filePath, "r", encoding="UTF-8") as fileRead:
            fileLines = fileRead.readlines()

        fileLines.append(stopText)

        with open(self.filePath, "w", encoding="UTF-8") as fileWrite:
            for line in fileLines:
                fileWrite.writelines([line, "\n"])

        self.started = False

        return True

    def editLogFile(self, text, levelText) -> bool:

        if (
            not self.fileName
            or not self.filePath
            or not text
            or not levelText
            or not self.started
        ):
            return False

        completeText: str = f"{levelText} {text}"

        with open(self.filePath, "r", encoding="UTF-8") as fileRead:
            writeLines = fileRead.readlines()

        writeLines.append(completeText)

        with open(self.filePath, "w", encoding="UTF-8") as fileWrite:
            for line in writeLines:
                line = line.strip("\n")
                fileWrite.writelines([line, "\n"])

        return True

    def printLog(self, levelText, whiteMode) -> bool:

        if not levelText or not self.text or not self.started:
            return False

        text = self.text

        if not whiteMode:

            from modules.ColorModule import ColorModule

            color = ColorModule(levelText)

            match levelText:
                case "[INFO]":
                    text = f"{color.blue()} {text}"
                case "[DONE]":
                    text = f"{color.green()} {text}"
                case "[WARN]":
                    text = f"{color.yellow()} {text}"
                case "[ERROR]":
                    text = f"{color.red()} {text}"
                case _:
                    text = None
            if not text:
                return False

            print(text)

            return True

        match levelText:
            case "[INFO]":
                text = f"{levelText} {text}"
            case "[DONE]":
                text = f"{levelText} {text}"
            case "[WARN]":
                text = f"{levelText} {text}"
            case "[ERROR]":
                text = f"{levelText} {text}"
            case _:
                text = None
        if not text:
            return False

        print(text)

        return True


logger = LoggerModule()


def log(text, level, whiteMode: bool = False) -> bool:

    try:
        levelText: str = ""

        match level:
            case 0:
                levelText = "[INFO]"
            case 1:
                levelText = "[DONE]"
            case 2:
                levelText = "[WARN]"
            case 3:
                levelText = "[ERROR]"
            case _:
                levelText = None

        if not text:
            text = None

        logger.text = text

        logger.editLogFile(text, levelText)
        logger.printLog(levelText, whiteMode)

        return True
    except:
        return False


def startlog() -> bool:

    try:

        logger.createLogFile()
        logger.startLog()

        os.system("cls")

        logger.showBanner()

        return True
    except:
        return False


def stoplog() -> bool:

    try:
        logger.stopLog()

        return True
    except:
        return False


def banner() -> bool:

    try:

        os.system("cls")

        logger.showBanner()

        return True

    except:
        return False
