import os
from utils import run_shell_cmd
from shutil import copytree, copyfile
from colorama import Fore, Style
from printing import print_section_header
from backup_paths_temp import get_configs_path_mapping, get_plist_mapping
from utils import _home_prefix


def reinstall_config_files(configs_path):
	"""
	Reinstall all configs from the backup.
	"""
	print_section_header("REINSTALLING CONFIG FILES", Fore.BLUE)

	def backup_prefix(path):
		return os.path.join(configs_path, path)

	configs_dir_mapping = get_configs_path_mapping()
	plist_files = get_plist_mapping()

	for target, backup in configs_dir_mapping.items():
		if os.path.isdir(backup_prefix(backup)):
			copytree(backup_prefix(backup), _home_prefix(target))

	for target, backup in plist_files.items():
		if os.path.exists(backup_prefix(backup)):
			copyfile(backup_prefix(backup), _home_prefix(target))

	print_section_header("SUCCESSFUL CONFIG REINSTALLATION", Fore.BLUE)


def reinstall_packages_from_lists(packages_path):
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
			run_shell_cmd(cmd)
		elif pm == "npm":
			print(Fore.BLUE + Style.BRIGHT + "Reinstalling {} packages...".format(pm) + Style.RESET_ALL)
			cmd = "cat {0}/npm_list.txt | xargs npm install -g".format(packages_path)
			run_shell_cmd(cmd)
		elif pm == "pip":
			print(Fore.BLUE + Style.BRIGHT + "Reinstalling {} packages...".format(pm) + Style.RESET_ALL)
			cmd = "pip install -r {0}/pip_list.txt".format(packages_path)
			run_shell_cmd(cmd)
		elif pm == "apm":
			print(Fore.BLUE + Style.BRIGHT + "Reinstalling {} packages...".format(pm) + Style.RESET_ALL)
			cmd = "apm install --packages-file {0}/apm_list.txt".format(packages_path)
			run_shell_cmd(cmd)
		elif pm == "macports":
			print(Fore.RED + "WARNING: Macports reinstallation is not supported." + Style.RESET_ALL)
		elif pm == "gem":
			print(Fore.RED + "WARNING: Gem reinstallation is not supported." + Style.RESET_ALL)
		elif pm == "cargo":
			print(Fore.RED + "WARNING: Cargo reinstallation is not possible at the moment."
			                 "\n -> https://github.com/rust-lang/cargo/issues/5593" + Style.RESET_ALL)

	print_section_header("SUCCESSFUL PACKAGE REINSTALLATION", Fore.BLUE)
