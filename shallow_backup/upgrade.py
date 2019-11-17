import os
import sys
from shutil import move
from colorama import Fore
from .config import get_config_path, get_xdg_config_path
from .printing import prompt_yes_no, print_green_bold, print_red_bold
from .utils import home_prefix, safe_mkdir


def upgrade_from_pre_v3():
	"""
	Before v3.0, the config file was stored at ~/.shallow-backup. In v3.0,
	the XDG Base Directory specification was adopted and the new config is
	stored in either $XDG_CONFIG_HOME/shallow-backup/shallow-backup.conf or
	~/.config/shallow-backup.conf. This method upgrades from
	v < 3.0 to v3.0 or v3.1 if required.
	"""
	old_config_names = [".shallow-backup", ".config/shallow-backup/shallow-backup.conf"]
	for old_config_path, old_config_name in [(home_prefix(old_config_name), old_config_name) for old_config_name in old_config_names]:
		if os.path.isfile(old_config_path):
			if prompt_yes_no("Config file from a version before v3.1 detected. Would you like to upgrade?", Fore.GREEN):
				new_config_path = get_config_path()
				print_green_bold(f"Moving {old_config_path} to {new_config_path}")
				if os.path.exists(new_config_path):
					print_red_bold(f"ERROR: {new_config_path} already exists. Manual intervention is required.")
					sys.exit(1)

				safe_mkdir(os.path.split(new_config_path)[0])
				move(old_config_path, new_config_path)

				print_green_bold("Replacing old shallow-backup config path with new config path in config file.")
				with open(new_config_path, "r") as f:
					contents = f.read()
					contents = contents.replace(old_config_name,
												new_config_path.replace(os.path.expanduser('~') + "/", ""))

				with open(new_config_path, "w") as f:
					f.write(contents)

				print_green_bold("Successful upgrade.")
			else:
				print_red_bold("Please downgrade to a version of shallow-backup before v3.0 if you do not want to upgrade your config.")
				sys.exit()
		elif os.path.isdir(old_config_path):
			print_red_bold(f"ERROR: {old_config_path} is a directory, when we were expecting a file. Manual intervention is required.")
			sys.exit(1)

	# Clean up ~/.config/shallow-backup
	incorrect_config_dir = os.path.join(get_xdg_config_path(), "shallow-backup")
	if os.path.isdir(incorrect_config_dir):
		os.rmdir(incorrect_config_dir)
