import sys
import json
from .printing import *
from .compatibility import *
from .utils import home_prefix


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
	Returns a default, platform specific config.
	"""
	return {
		"backup_path"      : "~/shallow-backup",
		"dotfiles"         : [
			".bashrc",
			".bash_profile",
			".gitconfig",
			".profile",
			".pypirc",
			".shallow-backup",
			".vimrc",
			".zlogin",
			".zprofile",
			".zshrc"
		],
		"dotfolders"       : [
			".ssh",
			".vim"
		],
		"default-gitignore": [
			"dotfiles/.ssh",
			"dotfiles/.pypirc",
			".DS_Store"
		],
		"config_mapping"   : get_config_paths()
	}


def safe_create_config():
	"""
	Creates config file if it doesn't exist already. Prompts to update
	it if an outdated version is detected.
	"""
	backup_config_path = get_config_path()
	# If it doesn't exist, create it.
	if not os.path.exists(backup_config_path):
		print_path_blue("Creating config file at:", backup_config_path)
		backup_config = get_default_config()
		write_config(backup_config)
	else:
		# If it does exist, make sure it's not outdated.
		with open(backup_config_path) as config:
			if "[USER]" in config.readline().strip():
				if prompt_yes_no("An outdated config file has been detected. Would you like to update this?",
				                 Fore.GREEN):
					delete_config_file()
					safe_create_config()
				else:
					print_red_bold("ERROR: Outdated config file found.")
					sys.exit(0)


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
	for section, contents in get_config().items():
		# Hide gitignore config
		if section == "default-gitignore":
			continue
		# Print backup path on same line
		elif section == "backup_path":
			print_path_red("Backup Path:", contents)
		elif section == "config_mapping":
			print_red_bold("Configs:")
			for path, dest in contents.items():
				print("    {} -> {}".format(path, dest))
		# Print section header and intent contents. (Dotfiles/folders)
		else:
			print_red_bold("\n{}: ".format(section.capitalize()))
			for item in contents:
				print("    {}".format(item))

