import os
from shutil import copytree, copyfile
from colorama import Fore, Style
from config import get_config
from utils import home_prefix
from utils import run_cmd, get_abs_path_subfiles
from printing import print_section_header

# NOTE: Naming convention is like this since the CLI flags would otherwise
#       conflict with the function names.


def reinstall_dots_sb(dots_path):
	"""
	Reinstall all dotfiles and folders by copying them to the home dir.
	"""
	print_section_header("REINSTALLING DOTFILES", Fore.BLUE)
	home_path = os.path.expanduser('~')
	for file in get_abs_path_subfiles(dots_path):
		if os.path.isdir(file):
			copytree(file, home_path, symlinks=True)
		else:
			copyfile(file, home_path)
	print_section_header("COMPLETED DOTFILE REINSTALLATION", Fore.BLUE)
	pass


def reinstall_fonts_sb(fonts_path):
	"""
	Reinstall all fonts.
	TODO: MAKE LINUX/WINDOWS COMPATIBLE.
	"""
	print_section_header("REINSTALLING FONTS", Fore.BLUE)
	# Copy every file in fonts_path to ~/Library/Fonts
	for font in get_abs_path_subfiles(fonts_path):
		# TODO: This doesn't work for some reason. (#145)
		copyfile(font, os.path.join("~/Library/Fonts", font.split("/")[-1]))
	print_section_header("COMPLETED FONT REINSTALLATION", Fore.BLUE)


def reinstall_configs_sb(configs_path):
	"""
	Reinstall all configs from the backup.
	"""
	print_section_header("REINSTALLING CONFIG FILES", Fore.BLUE)

	def backup_prefix(path):
		return os.path.join(configs_path, path)

	config = get_config()
	configs_dir_mapping = config["config_path_to_dest_map"]
	plist_files = config["plist_path_to_dest_map"]

	for target, backup in configs_dir_mapping.items():
		if os.path.isdir(backup_prefix(backup)):
			copytree(backup_prefix(backup), home_prefix(target))

	for target, backup in plist_files.items():
		if os.path.exists(backup_prefix(backup)):
			copyfile(backup_prefix(backup), home_prefix(target))

	print_section_header("COMPLETED CONFIG REINSTALLATION", Fore.BLUE)


def reinstall_packages_sb(packages_path):
	"""
	Reinstall all packages from the files in backup/installs.
	"""
	print_section_header("REINSTALLING PACKAGES", Fore.BLUE)

	# Figure out which install lists they have saved
	package_mgrs = set()
	for file in os.listdir(packages_path):
		# print(file)
		manager = file.split("_")[0].replace("-", " ")
		# TODO: Add macports
		if manager in ["gem", "brew-cask", "cargo", "npm", "pip", "brew", "apm"]:
			package_mgrs.add(file.split("_")[0])

	# TODO: USE print_pkg_mgr_reinstall()
	# TODO: Restylize this printing
	print(Fore.BLUE + Style.BRIGHT + "Package Managers detected:" + Style.RESET_ALL)
	for mgr in package_mgrs:
		print(Fore.BLUE + Style.BRIGHT + "\t" + mgr)
	print(Style.RESET_ALL)

	# TODO: Multithreading for reinstallation.
	# construct commands
	for pm in package_mgrs:
		if pm in ["brew", "brew-cask"]:
			pm_formatted = pm.replace("-", " ")
			print(Fore.BLUE + Style.BRIGHT + "Reinstalling {} packages...".format(pm_formatted) + Style.RESET_ALL)
			cmd = "xargs {0} install < {1}/{2}_list.txt".format(pm.replace("-", " "), packages_path, pm_formatted)
			run_cmd(cmd)
		elif pm == "npm":
			print(Fore.BLUE + Style.BRIGHT + "Reinstalling {} packages...".format(pm) + Style.RESET_ALL)
			cmd = "cat {0}/npm_list.txt | xargs npm install -g".format(packages_path)
			run_cmd(cmd)
		elif pm == "pip":
			print(Fore.BLUE + Style.BRIGHT + "Reinstalling {} packages...".format(pm) + Style.RESET_ALL)
			cmd = "pip install -r {0}/pip_list.txt".format(packages_path)
			run_cmd(cmd)
		elif pm == "apm":
			print(Fore.BLUE + Style.BRIGHT + "Reinstalling {} packages...".format(pm) + Style.RESET_ALL)
			cmd = "apm install --packages-file {0}/apm_list.txt".format(packages_path)
			run_cmd(cmd)
		elif pm == "macports":
			print(Fore.RED + "WARNING: Macports reinstallation is not supported." + Style.RESET_ALL)
		elif pm == "gem":
			print(Fore.RED + "WARNING: Gem reinstallation is not supported." + Style.RESET_ALL)
		elif pm == "cargo":
			print(Fore.RED + "WARNING: Cargo reinstallation is not possible at the moment."
			                 "\n -> https://github.com/rust-lang/cargo/issues/5593" + Style.RESET_ALL)

	print_section_header("COMPLETED PACKAGE REINSTALLATION", Fore.BLUE)


def reinstall_all_sb(dotfiles_path, packages_path, fonts_path, configs_path):
	"""
	Call all reinstallation methods.
	"""
	reinstall_dots_sb(dotfiles_path)
	reinstall_packages_sb(packages_path)
	reinstall_fonts_sb(fonts_path)
	reinstall_configs_sb(configs_path)
