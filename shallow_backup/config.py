import sys
import json
from os import path, environ
from .printing import *
from .compatibility import *
from .utils import safe_mkdir


def get_xdg_config_path():
	return environ.get('XDG_CONFIG_HOME') or path.join(path.expanduser('~'), '.config')


def get_config_path():
	test_config_path = environ.get('SHALLOW_BACKUP_TEST_CONFIG_PATH', None)
	if test_config_path:
		return test_config_path
	else:
		return path.join(get_xdg_config_path(), "shallow-backup.conf")


def get_config():
	"""
	Returns the config.
	:return: dictionary for config
	"""
	config_path = get_config_path()
	with open(config_path) as f:
		try:
			config = json.load(f)
		except json.decoder.JSONDecodeError:
			print_red_bold(f"ERROR: Invalid syntax in {config_path}")
			sys.exit(1)
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
			f"{get_config_path}",
			".tmux.conf",
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
		safe_mkdir(os.path.split(backup_config_path)[0])
		write_config(backup_config)
	else:
		# If it does exist, make sure it's not outdated.
		# TODO: Move this to upgrade.py
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


def add_dot_path_to_config(backup_config: dict, file_path: str) -> dict:
	"""
	Add a path to the config under the correct heading (dotfiles / dotfolders).
	Exits if the filepath parameter is invalid.
	:backup_config: dict representing current config
	:add:           str  relative or absolute path of file to add to config
	:return new backup config
	"""
	def strip_home(full_path):
		"""
		Removes the path to $HOME from the front of the absolute path.
		"""
		return full_path[len(os.path.expanduser("~")) + 1:]

	abs_path = path.abspath(file_path)
	if not path.exists(abs_path):
		print_path_red("Invalid file path:", abs_path)
		sys.exit(1)
	elif path.isdir(abs_path):
		backup_config["dotfolders"] += [strip_home(abs_path)]
	else:  # Otherwise it's a dotfile
		backup_config["dotfiles"] += [strip_home(abs_path)]
	return backup_config


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
