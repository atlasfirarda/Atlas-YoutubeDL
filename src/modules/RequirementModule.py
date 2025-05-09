from modules.LoggerModule import log, banner

import pkg_resources
from pkg_resources import DistributionNotFound

import subprocess
import sys
import requests


class RequirementModule:
    def __init__(self, requirements: list[str]):

        self.requirements = None

        if requirements:
            self.requirements = requirements

    def installRequirements(self) -> bool:

        if not self.requirements:
            return False

        isColored: bool = False

        for requirement in self.requirements:
            version = self.getLatestVersion(requirement)

            if requirement == "colored":
                isColored = True
            else:
                isColored = False

            try:
                if pkg_resources.get_distribution(requirement).version == version:
                    continue
                else:
                    log(
                        f"{requirement} has an update '{pkg_resources.get_distribution(requirement).version}' > '{version}'",
                        2,
                        isColored,
                    )
            except DistributionNotFound:
                log(f"{requirement} has not installed!", 2, isColored)
                pass

            try:
                log(f"Installing {requirement} ({version})", 0, isColored)
                subprocess.check_call(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "--quiet",
                        "install",
                        f"{requirement}=={version}",
                    ]
                )
                log(f"Installed {requirement} ({version})", 1, isColored)

                if requirement == "colored":
                    banner()

            except subprocess.CalledProcessError as ex:
                log(f"Installation Failed {requirement} ({version})", 2)
                log(f"{ex}", 3, True)

                continue

        return True

    @staticmethod
    def installRequirement(requirement) -> bool:

        if not requirement:
            return False

        isColored: bool = False

        version = getLatestVersion(requirement)

        if requirement == "colored":
            isColored = True
        else:
            isColored = False

        try:
            if pkg_resources.get_distribution(requirement).version == version:
                return True
            else:
                log(
                    f"{requirement} has an update '{pkg_resources.get_distribution(requirement).version}' > '{version}'",
                    2,
                    isColored,
                )
        except DistributionNotFound:
            log(f"{requirement} has not installed!", 2, isColored)
            pass

        try:

            log(f"Installing {requirement} ({version})", 0, isColored)
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "--quiet",
                    "install",
                    f"{requirement}=={version}",
                ]
            )
            log(f"Installed {requirement} ({version})", 1, isColored)

            return True

        except subprocess.CalledProcessError as ex:
            log(f"Installation Failed {requirement} ({version})", 2, isColored)
            log(f"{ex}", 3, isColored)

            return False

    def getLatestVersions(self) -> list[str]:

        if not self.requirements:
            return None

        latestVersions: list[str] = []

        try:

            for requirement in self.requirements:

                url: str = f"https://pypi.org/pypi/{requirement}/json"
                response = requests.get(url)

                if response.status_code == 200:
                    version = response.json()["info"]["version"]
                    latestVersions.append(version)

                else:
                    continue

            return latestVersions
        except:
            return None

    @staticmethod
    def getLatestVersion(requirement) -> str:

        if not requirement:
            return None

        try:
            url: str = f"https://pypi.org/pypi/{requirement}/json"
            response = requests.get(url)

            if response.status_code == 200:
                version = response.json()["info"]["version"]
                return version
            else:
                return None
        except:
            return None


def installRequirements(requirements) -> bool:

    try:

        module = RequirementModule(requirements)

        module.installRequirements()

        return True
    except:
        return False


def installRequirement(requirement) -> bool:

    try:

        RequirementModule.installRequirement(requirement)

        return True

    except:
        return False


def getLatestVersion(requirement) -> str:

    try:

        version = RequirementModule.getLatestVersion(requirement)

        return version
    except:
        return None
