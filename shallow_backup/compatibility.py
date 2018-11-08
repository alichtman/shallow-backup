import os
import platform


def get_os_name():
	return platform.system().lower()


def get_compatible_paths():
	"""
	Returns a dict of the paths where things should be located on the
	correct OS.
	"""
	HOME_DIR = os.path.expanduser('~')

	mac_paths = {
		"sublime2": "/Library/Application Support/Sublime\ Text\ 2",
		"sublime3": "/Library/Application Support/Sublime\ Text\ 3",
		"intelliJIdea2018.2": "Library/Preferences/IntelliJIdea2018.2",
		"pycharm2018.2": "Library/Preferences/PyCharm2018.2",
		"clion2018.2": "Library/Preferences/CLion2018.2",
		"phpStorm2018.2": "Library/Preferences/PhpStorm2018.2",
		"atom": ".atom",
		"applications": "/Applications",
		"fonts": os.path.join(HOME_DIR, "Library/Fonts")

	}

	linux_paths = {
		"sublime2": "/.config/sublime-text-2",
		"sublime3": "/.config/sublime-text-3",
		"intelliJIdea2018.2": os.path.join(HOME_DIR, ".IntelliJIdea2018.2"),
		"pyCharm2018.2": os.path.join(HOME_DIR, ".PyCharm2018.2"),
		"clion2018.2": os.path.join(HOME_DIR, ".CLion2018.2"),
		"phpStorm2018.2": os.path.join(HOME_DIR, ".PhpStorm2018.2"),
		"atom": os.path.join(HOME_DIR, ".atom"),
		"applications": "/usr/share/applications",
		"fonts": os.path.join(HOME_DIR, ".fonts")
	}

	if "darwin" == get_os_name():
		return mac_paths
	else:
		return linux_paths
