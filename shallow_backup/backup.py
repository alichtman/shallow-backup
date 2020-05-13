import os
from shlex import quote
from colorama import Fore
import multiprocessing as mp
from shutil import copyfile
from .utils import *
from .printing import *
from .compatibility import *
from .config import get_config


def backup_dotfiles(backup_dest_path, home_path=os.path.expanduser("~"), skip=False):
	"""
	Create `dotfiles` dir and makes copies of dotfiles and dotfolders.
	Assumes that dotfiles are stored in the home directory.
	:param skip: Boolean flag to skip prompting for overwrite. Used for scripting.
	:param backup_dest_path: Destination path for dotfiles. Like, ~/shallow-backup/dotfiles. Used in tests.
	:param home_path: Path where dotfiles will be found. $HOME by default.
	"""
	print_section_header("DOTFILES", Fore.BLUE)
	overwrite_dir_prompt_if_needed(backup_dest_path, skip)

	# get dotfolders and dotfiles
	config = get_config()["dotfiles"]

	# Aggregate pairs of [(Installed dotfile path, backup dest path)] in a list to be sorted into
	# dotfiles and dotfolders later
	dot_path_pairs = []
	for dotfile_path_from_config, options in config.items():
		# Evaluate condition, if specified. Skip if the command doesn't return true.
		condition_success = evaluate_condition(condition=options["backup_condition"],
											   backup_or_reinstall="backup",
											   dotfile_path=dotfile_path_from_config)
		if not condition_success:
			continue

		# If a file path in the config starts with /, it's a full path like /etc/ssh/
		if dotfile_path_from_config.startswith("/"):
			installed_dotfile_path = dotfile_path_from_config
			installed_dotfile_path = quote(':' + installed_dotfile_path[1:])
			backup_dotfile_path = quote(os.path.join(backup_dest_path, installed_dotfile_path))
			dot_path_pairs.append((dotfile_path_from_config, backup_dotfile_path))

		else:  # Dotfile living in $HOME
			installed_dotfile_path = quote(os.path.join(home_path, dotfile_path_from_config))
			backup_dotfile_path = quote(os.path.join(backup_dest_path, dotfile_path_from_config))
			dot_path_pairs.append((installed_dotfile_path, backup_dotfile_path))

	# Separate dotfiles and dotfolders
	dotfolders_mp_in = []
	dotfiles_mp_in = []
	for path_pair in dot_path_pairs:
		installed_path = path_pair[0]
		if os.path.isdir(installed_path):
			dotfolders_mp_in.append(path_pair)
		else:
			dotfiles_mp_in.append(path_pair)

	# Fix https://github.com/alichtman/shallow-backup/issues/230
	for dest_path in [path_pair[1] for path_pair in dotfiles_mp_in + dotfolders_mp_in]:
		print(f"Creating: {os.path.split(dest_path)[0]}")
		safe_mkdir(os.path.split(dest_path)[0])

	with mp.Pool(mp.cpu_count()):
		print_blue_bold("Backing up dotfolders...")
		for x in dotfolders_mp_in:
			p = mp.Process(target=copy_dir_if_valid, args=(x[0], x[1],))
			p.start()
			p.join()

		print_blue_bold("Backing up dotfiles...")
		for x in dotfiles_mp_in:
			p = mp.Process(target=copyfile, args=(x[0], x[1],))
			p.start()
			p.join()


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

	# backup config files + dirs in backup_path/<target>/
	for path_to_backup, target in config["config_mapping"].items():
		print("BACKUP:", path_to_backup)
		print("TARGET:", target)
		dest = os.path.join(backup_path, target)
		if os.path.isdir(path_to_backup):
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

	# pip3
	print_pkg_mgr_backup("pip3")
	command = "pip3 list --format=freeze"
	dest = "{}/pip3_list.txt".format(backup_path)
	run_cmd_write_stdout(command, dest)

	# npm
	print_pkg_mgr_backup("npm")
	command = "npm ls --global --parseable=true --depth=0"
	temp_file_path = "{}/npm_temp_list.txt".format(backup_path)
	# If command is successful, go to the next parsing step.
	if run_cmd_write_stdout(command, temp_file_path) == 0:
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

	# vscode extensions
	print_pkg_mgr_backup("VSCode")
	command = "code --list-extensions --show-versions"
	dest = "{}/vscode_list.txt".format(backup_path)
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


def backup_fonts(backup_path, skip=False):
	"""
	Copies all .ttf and .otf files in ~/Library/Fonts/ to backup/fonts/
	"""
	print_section_header("FONTS", Fore.BLUE)
	overwrite_dir_prompt_if_needed(backup_path, skip)
	print_blue("Copying '.otf' and '.ttf' fonts...")
	fonts_path = get_fonts_dir()
	if os.path.isdir(fonts_path):
		fonts = [quote(os.path.join(fonts_path, font)) for font in os.listdir(fonts_path) if
				 font.endswith(".otf") or font.endswith(".ttf")]

		for font in fonts:
			if os.path.exists(font):
				copyfile(font, os.path.join(backup_path, font.split("/")[-1]))
	else:
		print_red('Skipping fonts backup. No fonts directory found.')


def backup_all(dotfiles_path, packages_path, fonts_path, configs_path, skip=False):
	"""
	Complete backup procedure.
	"""
	backup_dotfiles(dotfiles_path, skip=skip)
	backup_packages(packages_path, skip)
	backup_fonts(fonts_path, skip)
	backup_configs(configs_path, skip)
