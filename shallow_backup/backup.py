import os
import multiprocessing as mp
from colorama import Fore, Style
from shutil import copytree, copyfile
from shallow_backup.config import get_config
from shallow_backup.printing import print_section_header, print_pkg_mgr_backup
from shallow_backup.utils import home_prefix, mkdir_warn_overwrite, run_cmd_write_stdout, copy_dir, mkdir_or_pass, get_subfiles


def backup_dotfiles(backup_path):
	"""
	Create `dotfiles` dir and makes copies of dotfiles and dotfolders.
	"""
	print_section_header("DOTFILES", Fore.BLUE)
	mkdir_warn_overwrite(backup_path)

	# assumes dotfiles are stored in home directory
	home_path = os.path.expanduser('~')

	# get dotfolders and dotfiles
	config = get_config()
	dotfiles_for_backup = config["dotfiles"]
	dotfolders_for_backup = config["dotfolders"]

	# Add dotfile/folder for backup if it exists on the machine
	dotfiles = [file for file in dotfiles_for_backup if os.path.isfile(
		os.path.join(home_path, file))]
	dotfolders = [folder for folder in dotfolders_for_backup if os.path.exists(
		os.path.join(home_path, folder))]

	# dotfiles/folders multiprocessing format: [(full_dotfile_path, full_dest_path), ...]
	dotfolders_mp_in = []
	for dotfolder in dotfolders:
		dotfolders_mp_in.append(
			(os.path.join(home_path, dotfolder), backup_path))

	dotfiles_mp_in = []
	for dotfile in dotfiles:
		dotfiles_mp_in.append((os.path.join(home_path, dotfile), os.path.join(backup_path, dotfile)))

	# Multiprocessing
	with mp.Pool(mp.cpu_count()):
		print(Fore.BLUE + Style.BRIGHT + "Backing up dotfolders..." + Style.RESET_ALL)
		for x in dotfolders_mp_in:
			x = list(x)
			mp.Process(target=copy_dir, args=(x[0], x[1],)).start()

	with mp.Pool(mp.cpu_count()):
		print(Fore.BLUE + Style.BRIGHT + "Backing up dotfiles..." + Style.RESET_ALL)
		for x in dotfiles_mp_in:
			x = list(x)
			mp.Process(target=copyfile, args=(x[0], x[1],)).start()


def backup_configs(backup_path):
	"""
	Creates `configs` directory and places config backups there.
	Configs are application settings, generally. .plist files count.
	"""
	print_section_header("CONFIGS", Fore.BLUE)
	mkdir_warn_overwrite(backup_path)
	config = get_config()
	configs_dir_mapping = config["config_path_to_dest_map"]
	plist_files = config["plist_path_to_dest_map"]

	print(Fore.BLUE + Style.BRIGHT + "Backing up configs..." + Style.RESET_ALL)

	# backup config dirs in backup_path/<target>/
	for config, target in configs_dir_mapping.items():
		src_dir = home_prefix(config)
		configs_backup_path = os.path.join(backup_path, target)
		if os.path.isdir(src_dir):
			# TODO: Exclude Sublime/Atom/VS Code Packages here to speed things up
			copytree(src_dir, configs_backup_path, symlinks=True)

	# backup plist files in backup_path/configs/plist/
	print(Fore.BLUE + Style.BRIGHT + "Backing up plist files..." + Style.RESET_ALL)
	plist_backup_path = os.path.join(backup_path, "plist")
	mkdir_or_pass(plist_backup_path)
	for plist, dest in plist_files.items():
		plist_path = home_prefix(plist)
		if os.path.exists(plist_path):
			copyfile(plist_path, os.path.join(backup_path, dest))


def backup_packages(backup_path):
	"""
	Creates `packages` directory and places install list text files there.
	"""
	print_section_header("PACKAGES", Fore.BLUE)
	mkdir_warn_overwrite(backup_path)

	std_package_managers = [
		"brew",
		"brew cask",
		"gem"
	]

	for mgr in std_package_managers:
		# deal with package managers that have spaces in them.
		print_pkg_mgr_backup(mgr)
		command = "{} list".format(mgr)
		dest = "{}/{}_list.txt".format(backup_path, mgr.replace(" ", "-"))
		run_cmd_write_stdout(command, dest)

	# cargo
	print_pkg_mgr_backup("cargo")
	command = "ls {}".format(home_prefix(".cargo/bin/"))
	dest = "{}/cargo_list.txt".format(backup_path)
	run_cmd_write_stdout(command, dest)

	# pip
	print_pkg_mgr_backup("pip")
	command = "pip list --format=freeze".format(backup_path)
	dest = "{}/pip_list.txt".format(backup_path)
	run_cmd_write_stdout(command, dest)

	# npm
	print_pkg_mgr_backup("npm")
	command = "npm ls --global --parseable=true --depth=0"
	temp_file_path = "{}/npm_temp_list.txt".format(backup_path)
	run_cmd_write_stdout(command, temp_file_path)
	npm_dest_file = "{0}/npm_list.txt".format(backup_path)
	# Parse npm output
	with open(temp_file_path, mode="r+") as temp_file:
		# Skip first line of file
		temp_file.seek(1)
		with open(npm_dest_file, mode="w+") as dest:
			for line in temp_file:
				dest.write(line.split("/")[-1])

	os.remove(temp_file_path)

	# atom package manager
	print_pkg_mgr_backup("Atom")
	command = "apm list --installed --bare"
	dest = "{}/apm_list.txt".format(backup_path)
	run_cmd_write_stdout(command, dest)

	# sublime text 2 packages
	sublime_2_path = home_prefix("Library/Application Support/Sublime Text 2/Packages/")
	if os.path.isdir(sublime_2_path):
		print_pkg_mgr_backup("Sublime Text 2")
		command = ["ls", sublime_2_path]
		dest = "{}/sublime2_list.txt".format(backup_path)
		run_cmd_write_stdout(command, dest)

	# sublime text 3 packages
	sublime_3_path = home_prefix("Library/Application Support/Sublime Text 3/Installed Packages/")
	if os.path.isdir(sublime_3_path):
		print_pkg_mgr_backup("Sublime Text 3")
		command = ["ls", sublime_3_path]
		dest = "{}/sublime3_list.txt".format(backup_path)
		run_cmd_write_stdout(command, dest)
	else:
		print(sublime_3_path, "IS NOT DIR")

	# macports
	print_pkg_mgr_backup("macports")
	command = "port installed requested"
	dest = "{}/macports_list.txt".format(backup_path)
	run_cmd_write_stdout(command, dest)

	# system installs
	print_pkg_mgr_backup("macOS Applications")
	command = "ls /Applications/"
	dest = "{}/system_apps_list.txt".format(backup_path)
	run_cmd_write_stdout(command, dest)

	# Clean up empty package list files
	print(Fore.BLUE + "Cleaning up empty package lists..." + Style.RESET_ALL)
	for file in get_subfiles(backup_path):
		if os.path.getsize(file) == 0:
			os.remove(file)


def backup_fonts(path):
	"""
	Creates list of all .ttf and .otf files in ~/Library/Fonts/
	"""
	print_section_header("FONTS", Fore.BLUE)
	mkdir_warn_overwrite(path)
	print(Fore.BLUE + "Copying '.otf' and '.ttf' fonts..." + Style.RESET_ALL)
	fonts_path = home_prefix("Library/Fonts/")
	fonts = [os.path.join(fonts_path, font) for font in os.listdir(fonts_path) if
	         font.endswith(".otf") or font.endswith(".ttf")]

	for font in fonts:
		if os.path.exists(font):
			copyfile(font, os.path.join(path, font.split("/")[-1]))


def backup_all(dotfiles_path, packages_path, fonts_path, configs_path):
	"""
	Complete backup procedure.
	"""
	backup_dotfiles(dotfiles_path)
	backup_packages(packages_path)
	backup_fonts(fonts_path)
	backup_configs(configs_path)
