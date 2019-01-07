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
		sublime2_path = os.path.join(get_home(), "Library/Application Support/Sublime Text 2")
		sublime3_path = os.path.join(get_home(), "Library/Application Support/Sublime Text 3")
		vscode_path_1 = os.path.join(get_home(), "Library/Application Support/Code/User/settings.json")
		vscode_path_2 = os.path.join(get_home(), "Library/Application Support/Code/User/Snippets")
		vscode_path_3 = os.path.join(get_home(), "Library/Application Support/Code/User/keybindings.json")
		atom_path = os.path.join(get_home(), ".atom")
		terminal_path = os.path.join(get_home(), "Library/Preferences/com.apple.Terminal.plist")

		return {
			sublime2_path: "sublime2",
			sublime3_path: "sublime3",
			vscode_path_1: "vscode/settings",
			vscode_path_2: "vscode/Snippets",
			vscode_path_3: "vscode/keybindings",
			atom_path: "atom",
			terminal_path: "terminal_plist"
		}
	else:
		sublime2_path = "/.config/sublime-text-2"
		sublime3_path = "/.config/sublime-text-3"
		vscode_path_1 = "/.config/Code/User/settings.json"
		vscode_path_2 = "/.config/Code/User/Snippets"
		vscode_path_3 = "/.config/Code/User/keybindings.json"
		atom_path = os.path.join(get_home(), ".atom")
		return {
			# TODO: Double check these paths. Not sure these are right.
			sublime2_path: "sublime2",
			sublime3_path: "sublime3",
			vscode_path_1: "vscode/settings",
			vscode_path_2: "vscode/Snippets",
			vscode_path_3: "vscode/keybindings",
			atom_path: "atom"
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
