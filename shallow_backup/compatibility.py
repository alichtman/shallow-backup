import os
import platform


def get_os_name():
	return platform.system().lower()


def get_home():
	return os.path.expanduser('~')


def get_config_paths():
	"""
	Returns a dict of config paths for the correct OS.
	"""
	if "darwin" == get_os_name():
		return {
			"sublime2": os.path.join(get_home(), "Library/Application Support/Sublime Text 2"),
			"sublime3": os.path.join(get_home(), "Library/Application Support/Sublime Text 3"),
			"atom": os.path.join(get_home(), ".atom"),
			"terminal_plist": os.path.join(get_home(), "Library/Preferences/com.apple.Terminal.plist")
			# "intelliJIdea2018.2": os.path.join(get_home(), "Library/Preferences/IntelliJIdea2018.2"),
			# "pycharm2018.2": os.path.join(get_home(), "Library/Preferences/PyCharm2018.2"),
			# "clion2018.2": os.path.join(get_home(), "Library/Preferences/CLion2018.2"),
			# "phpStorm2018.2": os.path.join(get_home(), "Library/Preferences/PhpStorm2018.2"),
		}
	else:
		return {
			# TODO: Double check these paths. Not sure these are right.
			"sublime2": "/.config/sublime-text-2",
			"sublime3": "/.config/sublime-text-3",
			"atom": os.path.join(get_home(), ".atom"),
			# "intelliJIdea2018.2": os.path.join(get_home(), ".IntelliJIdea2018.2"),
			# "pyCharm2018.2": os.path.join(get_home(), ".PyCharm2018.2"),
			# "clion2018.2": os.path.join(get_home(), ".CLion2018.2"),
			# "phpStorm2018.2": os.path.join(get_home(), ".PhpStorm2018.2"),
		}


def get_fonts_dir():
	os_name = get_os_name()
	if os_name == "darwin":
		return os.path.join(get_home(), "Library/Fonts")
	elif os_name == "linux":
		return os.path.join(get_home(), ".fonts")


def get_applications_dir():
	os_name = get_os_name()
	if os_name == "darwin":
		return "/Applications"
	elif os_name == "linux":
		return "/usr/share/applications"
