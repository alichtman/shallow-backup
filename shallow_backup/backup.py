import os
from shlex import quote
from colorama import Fore
import multiprocessing as mp
from shutil import copytree, copyfile

from .utils import *
from .printing import *
from .compatibility import *
from .config import get_config


def overwrite_dir_prompt_if_needed(path, needed):
	"""
	Prompts the user before deleting the directory if needed.
	This function lets the CLI args silence the prompts.
	:param path: absolute path
	:param needed: boolean
	"""
	if not needed:
		mkdir_warn_overwrite(path)
	else:
		mkdir_overwrite(path)


def backup_dotfiles(backup_path, skip=False):
	"""
	Create `dotfiles` dir and makes copies of dotfiles and dotfolders.
	"""
	print_section_header("DOTFILES", Fore.BLUE)
	overwrite_dir_prompt_if_needed(backup_path, skip)

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
		dotfolder_path = quote(os.path.join(home_path, dotfolder))
		dotfolders_mp_in.append((dotfolder_path, backup_path))

	dotfiles_mp_in = []
	for dotfile in dotfiles:
		dotfile_path = quote(os.path.join(home_path, dotfile))
		dest_path = quote(os.path.join(backup_path, dotfile))
		dotfiles_mp_in.append((dotfile_path, dest_path))

	# Multiprocessing
	with mp.Pool(mp.cpu_count()):
		print_blue_bold("Backing up dotfolders...")
		for x in dotfolders_mp_in:
			x = list(x)
			mp.Process(target=copy_dir_if_valid, args=(x[0], x[1],)).start()

	with mp.Pool(mp.cpu_count()):
		print_blue_bold("Backing up dotfiles...")
		for x in dotfiles_mp_in:
			x = list(x)
			mp.Process(target=copyfile, args=(x[0], x[1],)).start()


def backup_configs(backup_path, skip=False):
	"""
	Creates `configs` directory and places config backups there.
	Configs are application settings, generally. .plist files count.
	In the config file, the value of the configs dictionary is the dest
	path relative to the configs/ directory.
	"""
	print_section_header("CONFIGS", Fore.BLUE)
	overwrite_dir_prompt_if_needed(backup_path, skip)
	config = get_config()

	print_blue_bold("Backing up configs...")

	# backup config files + dirs in backup_path/configs/<target>/
	for path_to_backup, target in config["config_mapping"].items():
		dest = os.path.join(backup_path, target)
		if os.path.isdir(path_to_backup):
			# TODO: Exclude Sublime/Atom/VS Code Packages here to speed things up
			copytree(path_to_backup, quote(dest), symlinks=True)
		elif os.path.isfile(path_to_backup):
			parent_dir = dest[:dest.rfind("/")]
			safe_mkdir(parent_dir)
			copyfile(path_to_backup, quote(dest))


def backup_packages(backup_path, skip=False):
	"""
	Creates `packages` directory and places install list text files there.
	"""
	print_section_header("PACKAGES", Fore.BLUE)
	overwrite_dir_prompt_if_needed(backup_path, skip)

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
	command = "pip list --format=freeze"
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

	config_paths = get_config_paths()

	# sublime text 2 packages
	sublime_2_path = os.path.join(config_paths["sublime2"], "Packages")
	if os.path.isdir(sublime_2_path):
		print_pkg_mgr_backup("Sublime Text 2")
		command = ["ls", sublime_2_path]
		dest = "{}/sublime2_list.txt".format(backup_path)
		run_cmd_write_stdout(command, dest)

	# sublime text 3 packages
	sublime_2_path = os.path.join(config_paths["sublime3"], "Installed Packages")
	if os.path.isdir(sublime_3_path):
		print_pkg_mgr_backup("Sublime Text 3")
		command = ["ls", sublime_3_path]
		dest = "{}/sublime3_list.txt".format(backup_path)
		run_cmd_write_stdout(command, dest)

	# macports
	print_pkg_mgr_backup("macports")
	command = "port installed requested"
	dest = "{}/macports_list.txt".format(backup_path)
	run_cmd_write_stdout(command, dest)

	# system installs
	print_pkg_mgr_backup("System Applications")
	applications_path = get_applications_dir()
	command = "ls {}".format(applications_path)
	dest = "{}/system_apps_list.txt".format(backup_path)
	run_cmd_write_stdout(command, dest)

	# Clean up empty package list files
	print_blue("Cleaning up empty package lists...")
	for file in get_abs_path_subfiles(backup_path):
		if os.path.getsize(file) == 0:
			os.remove(file)


def backup_fonts(backup_path, skip=False):
	"""
	Copies all .ttf and .otf files in ~/Library/Fonts/ to backup/fonts/
	"""
	print_section_header("FONTS", Fore.BLUE)
	overwrite_dir_prompt_if_needed(backup_path, skip)
	print_blue("Copying '.otf' and '.ttf' fonts...")
	fonts_path = get_fonts_dir()
	fonts = [quote(os.path.join(fonts_path, font)) for font in os.listdir(fonts_path) if
	         font.endswith(".otf") or font.endswith(".ttf")]

	for font in fonts:
		if os.path.exists(font):
			copyfile(font, os.path.join(backup_path, font.split("/")[-1]))


def backup_all(dotfiles_path, packages_path, fonts_path, configs_path, skip=False):
	"""
	Complete backup procedure.
	"""
	backup_dotfiles(dotfiles_path, skip)
	backup_packages(packages_path, skip)
	backup_fonts(fonts_path, skip)
	backup_configs(configs_path, skip)
