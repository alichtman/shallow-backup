import os
import sys
import json
from utils import home_prefix
from printing import *


def get_config_path():
	return home_prefix(".shallow-backup")


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
	# TODO: Cross-platform compatibility
	"""
	return {
		"backup_path": "~/shallow-backup",
		"dotfiles"   : [
			".bashrc",
			".bash_profile",
			".gitconfig",
			".profile",
			".pypirc",
			".shallow-backup",
			".vimrc",
			".zshrc"
		],
		"dotfolders" : [
			".ssh",
			".vim"
		],
		"default-gitignore"  : [
			"dotfiles/.ssh",
			"packages/",
			"dotfiles/.pypirc",
		],
		"config_path_to_dest_map": {
			"Library/Application Support/Sublime Text 2/Packages/User/": "sublime_2",
			"Library/Application Support/Sublime Text 3/Packages/User/": "sublime_3",
			"Library/Preferences/IntelliJIdea2018.2/"                  : "intellijidea_2018.2",
			"Library/Preferences/PyCharm2018.2/"                       : "pycharm_2018.2",
			"Library/Preferences/CLion2018.2/"                         : "clion_2018.2",
			"Library/Preferences/PhpStorm2018.2"                       : "phpstorm_2018.2",
			".atom/"                                                   : "atom",
		},
		"plist_path_to_dest_map" : {
			"Library/Preferences/com.apple.Terminal.plist": "plist/com.apple.Terminal.plist",
		},
	}


def safe_create_config():
	"""
	Creates config file if it doesn't exist already.
	"""
	backup_config_path = get_config_path()
	if not os.path.exists(backup_config_path):
		print_blue_bold("Creating config file at {}".format(backup_config_path))
		backup_config = get_default_config()
		write_config(backup_config)


def add_to_config(section, path, dest=None):
	"""
	Adds the path under the correct section in the config file.
	FIRST ARG: [dot, config]
	SECOND ARG: path, relative to home directory for dotfiles, absolute for configs
	"""
	if section == "dot":
		# Check if the file is in the home directory.
		full_path = home_prefix(path)
		if not os.path.exists(full_path):
			print_red_bold("ERR: {} doesn't exist.".format(full_path))
			sys.exit(1)

		# Make sure dotfile starts with a period
		if path[0] != ".":
			print_red_bold("ERR: Not a dotfile.")
			sys.exit(1)

		if not os.path.isdir(full_path):
			section = "dotfiles"
			print_blue_bold("Adding {} to dotfile backup.".format(full_path))
		else:
			section = "dotfolders"
			if path[-1] != "/":
				full_path += "/"
				path += "/"
			print_blue_bold("Adding {} to dotfolder backup.".format(full_path))

	elif section == "config":
		# TODO: Finish proofing this for which abs/non-abs paths get printed and stored.
		full_path = path
		# Remove home dir path expansion
		home = os.path.expanduser('~')
		if path.startswith(home):
			path = path[len(home) + 1:]
		# Check that the path exists.
		if not os.path.exists(full_path):
			print_red_bold("ERR: {} doesn't exist.".format(full_path))
			sys.exit(1)

		if path.endswith(".plist"):
			section = "plist_path_to_dest_map"
			# Prepend "plist" to the path to put it in config/plist/whatever
			path = (path, os.path.join("plist", path.split("/")[-1]))
			print_blue_bold("Adding {} to plist backup.".format(full_path))
		else:
			section = "config_path_to_dest_map"
			path = (path, dest)
			print_blue_bold("Adding {} to config backup.".format(full_path))
	else:
		print_red_bold("ERR: {} is invalid. \"dot\" and \"config\" are the only valid options.".format(section))
		sys.exit(1)

	# Update config.
	config = get_config()
	if type(path) is not tuple:
		file_set = set(config[section])
		file_set.update([path])
		config[section] = list(file_set)
	else:
		# Get dictionary of {path_to_backup: dest}
		file_set = config[section]
		file_set[path[0]] = path[1]
		config[section] = file_set
	write_config(config)


def rm_from_config(path):
	"""
	Removes the path from a section in the config file. Exits if the path doesn't exist.
	Path, relative to home directory for dotfiles, absolute for configs
	"""
	found = False
	config = get_config()
	for section, items in config.items():
		if path in items:
			print_blue_bold("Removing {} from backup...".format(path))
			items.remove(path)
			config[section] = items
			found = True

	if not found:
		print_red_bold("ERR: Path not found in config file...")
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
		if section == "default-gitignore":
			continue
		# Print backup path on same line
		elif section == "backup_path":
			print(Fore.RED + Style.BRIGHT + "Backup Path: " + Style.RESET_ALL + contents)
		elif section == "config_path_to_dest_map":
			print_red_bold("Configs to Backup Path Mapping: ")
			for path, dest in contents.items():
				print("    {} -> {}".format(path, dest))
		elif section == "plist_path_to_dest_map":
			print_red_bold("Plist to Backup Path Mapping: ")
			for path, dest in contents.items():
				print("    {} -> {}".format(path, dest))
		# Print section header and then contents indented.
		else:
			print_red_bold("\n{}: ".format(section.capitalize()))
			for item in contents:
				print("    {}".format(item))

	print()
