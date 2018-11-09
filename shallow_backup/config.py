import os
import json
from printing import *
from utils import home_prefix


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
			"Library/Preferences/com.apple.Terminal.plist"			   : "plist/com.apple.Terminal.plist",
		},
	}


def safe_create_config():
	"""
	Creates config file if it doesn't exist already.
	"""
	backup_config_path = get_config_path()
	if not os.path.exists(backup_config_path):
		print_path_blue("Creating config file at:", backup_config_path)
		backup_config = get_default_config()
		write_config(backup_config)


def delete_config_file():
	"""
	Deletes config file.
	"""
	config_path = get_config_path()
	if os.path.isfile(config_path):
		print_red_bold("Deleting config file.")
		os.remove(config_path)
	else:
		print_red_bold("ERROR: No config file found.")


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
		# Print section header and then contents indented.
		else:
			print_red_bold("\n{}: ".format(section.capitalize()))
			for item in contents:
				print("    {}".format(item))

	print()
