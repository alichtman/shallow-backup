import os
import sys
import json
from colorama import Fore, Style
import constants as Constants
from printing import print_section_header
from utils import _home_prefix


def get_config_path():
	return _home_prefix(Constants.CONFIG_PATH)


def get_config():
	"""
	Returns the config.
	:return: dictionary for config
	"""
	with open(get_config_path()) as f:
		config = json.load(f)
	return config


def write_config(config):
	"""
	Write to config file
	"""
	with open(get_config_path(), 'w') as f:
		json.dump(config, f, indent=4)


def get_default_config():
	"""
	Returns a default configuration.
	"""
	return {
		"backup_path": "~/shallow-backup",
		"dotfiles": [
			".bashrc",
			".bash_profile",
			".gitconfig",
			".profile",
			".pypirc",
			".shallow-backup",
			".vimrc",
			".zshrc"
		],
		"dotfolders": [
			".ssh",
			".vim"
		],
		"gitignore": [
			"dotfiles/.ssh",
			"packages/",
			"dotfiles/.pypirc",
		]
	}


def create_config_file_if_needed():
	"""
	Creates config file if it doesn't exist already.
	"""
	backup_config_path = get_config_path()
	if not os.path.exists(backup_config_path):
		print(Fore.BLUE + Style.BRIGHT + "Creating config file at {}".format(backup_config_path) + Style.RESET_ALL)
		backup_config = get_default_config()
		write_config(backup_config)


def add_path_to_config(section, path):
	"""
	Adds the path under the correct section in the config file.
	FIRST ARG: [dot, config, other]
	SECOND ARG: path, relative to home directory for dotfiles, absolute for configs
	"""
	full_path = _home_prefix(path)
	if not os.path.exists(full_path):
		print(Fore.RED + Style.BRIGHT + "ERR: {} doesn't exist.".format(full_path) + Style.RESET_ALL)
		sys.exit(1)

	if section == "dot":
		# Make sure dotfile starts with a period
		if path[0] != ".":
			print(Fore.RED + Style.BRIGHT + "ERR: Not a dotfile." + Style.RESET_ALL)
			sys.exit(1)

		if not os.path.isdir(full_path):
			section = "dotfiles"
			print(Fore.BLUE + Style.BRIGHT + "Adding {} to dotfile backup.".format(full_path) + Style.RESET_ALL)
		else:
			section = "dotfolders"
			if path[-1] != "/":
				full_path += "/"
				path += "/"
			print(Fore.BLUE + Style.BRIGHT + "Adding {} to dotfolder backup.".format(full_path) + Style.RESET_ALL)

	# TODO: Add config section once configs backup prefs are moved to the config file
	elif section == "config":
		print(Fore.RED + Style.BRIGHT + "ERR: Option not currently supported." + Style.RESET_ALL)
		sys.exit(1)
	elif section == "other":
		print(Fore.RED + Style.BRIGHT + "ERR: Option not currently supported." + Style.RESET_ALL)
		sys.exit(1)

	config = get_config()
	file_set = set(config[section])
	file_set.update([path])
	config[section] = list(file_set)
	write_config(config)


def rm_path_from_config(path):
	"""
	Removes the path from a section in the config file. Exits if the path doesn't exist.
	Path, relative to home directory for dotfiles, absolute for configs
	"""
	flag = False
	config = get_config()
	for section, items in config.items():
		if path in items:
			print(Fore.BLUE + Style.BRIGHT + "Removing {} from backup...".format(path) + Style.RESET_ALL)
			items.remove(path)
			config[section] = items
			flag = True

	if not flag:
		print(Fore.RED + Style.BRIGHT + "ERR: Not currently backing that path up..." + Style.RESET_ALL)
	else:
		write_config(config)


def show_config():
	"""
	Print the config. Colorize section titles and indent contents.
	"""
	print_section_header("SHALLOW BACKUP CONFIG", Fore.RED)
	config = get_config()
	for section, contents in config.items():
		# Hide gitignore config
		if section == "gitignore":
			continue
		# Print backup path on same line
		if section == "backup_path":
			print(Fore.RED + Style.BRIGHT + "Backup Path:" + Style.RESET_ALL + contents)
		# Print section header and then contents indented.
		else:
			print(Fore.RED + Style.BRIGHT + "\n{}: ".format(section.capitalize()) + Style.RESET_ALL)
			for item in contents:
				print("    {}".format(item))

	print()
