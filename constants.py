import platform
from enum import Enum
import os


class Constants(Enum):
    def checkPlatform(osName):
        return osName.lower() == platform.system().lower()

    PROJECT_NAME = "shallow-backup"
    VERSION = "1.3"
    AUTHOR_GITHUB = "alichtman"
    AUTHOR_FULL_NAME = "Aaron Lichtman"
    DESCRIPTION = "Easily create lightweight documentation of installed packages, dotfiles, and more."
    URL = "https://github.com/alichtman/shallow-backup"
    AUTHOR_EMAIL = "aaronlichtman@gmail.com"
    CONFIG_PATH = ".shallow-backup"
    INVALID_DIRS = [".Trash", ".npm", ".cache", ".rvm"]
    PACKAGE_MANAGERS = ["gem", "brew-cask", "cargo", "npm", "pip", "brew", "apm"]
    LOGO = """
              dP                dP dP                        dP                         dP
              88                88 88                        88                         88
     ,d8888'  88d888b. .d8888b. 88 88 .d8888b. dP  dP  dP    88d888b. .d8888b. .d8888b. 88  .dP  dP    dP 88d888b.
     Y8ooooo, 88'  `88 88'  `88 88 88 88'  `88 88  88  88    88'  `88 88'  `88 88'  `\"\" 88888\"   88    88 88'  `88
           88 88    88 88.  .88 88 88 88.  .88 88.88b.88'    88.  .88 88.  .88 88.  ... 88  `8b. 88.  .88 88.  .88
     `88888P' dP    dP `88888P8 dP dP `88888P' 8888P Y8P     88Y8888' `88888P8 `88888P' dP   `YP `88888P' 88Y888P'
                                                                                                          88
                                                                                                          dP	"""
    HOME_DIRECTORY = os.path.expanduser('~')
    SUBLIME2_DIRECTORY = "/Library/Application Support/Sublime\ Text\ 2" if checkPlatform(
        "darwin") else "/.config/sublime-text-2"
    SUBLIME3_DIRECTORY = "/Library/Application Support/Sublime\ Text\ 3" if checkPlatform(
        "darwin") else "/.config/sublime-text-3"
    INTELLIJ_DIRECTORY = "Library/Preferences/IntelliJIdea2018.2" if checkPlatform("darwin") \
        else os.path.join(HOME_DIRECTORY, ".IntelliJIdea2018.2")
    PYCHARM_DIRECTORY = "Library/Preferences/PyCharm2018.2" if checkPlatform("darwin") \
        else os.path.join(HOME_DIRECTORY, ".PyCharm2018.2")
    CLION_DIRECTORY = "Library/Preferences/CLion2018.2" if checkPlatform("darwin") \
        else os.path.join(HOME_DIRECTORY, ".CLion2018.2")
    PHPSTORM_DIRECTORY = "Library/Preferences/PhpStorm2018.2" if checkPlatform("darwin") \
        else os.path.join(HOME_DIRECTORY, ".PhpStorm2018.2")
    ATOM_DIRECTORY = ".atom" if checkPlatform("darwin") \
        else os.path.join(HOME_DIRECTORY, ".atom")
    APPLICATIONS_DIRECTORY = "/Applications" if checkPlatform("darwin") else "/usr/share/applications"
    FONTS_DIRECTORY = os.path.join(HOME_DIRECTORY, "Library/Fonts") if checkPlatform("darwin") \
        else os.path.join(HOME_DIRECTORY, ".fonts")
    OS_NAME = "macOS" if checkPlatform("darwin") else "linux"
    IS_MACOS = True if checkPlatform("darwin") else False
