import os
import inquirer
from utils import *
from printing import *
from config import *
from colorama import Fore, Style
from git_wrapper import git_set_remote, move_git_repo


def prompt_for_path_update(config):
	"""
	Ask user if they'd like to update the backup path or not.
	If yes, update. If no... don't.
	"""
	current_path = config["backup_path"]
	print("{}{}Current shallow-backup path: {}{}{}".format(Fore.BLUE, Style.BRIGHT, Style.NORMAL, current_path, Style.RESET_ALL))

	if prompt_yes_no("Would you like to update this?", Fore.GREEN):
		print_green_bold("Enter relative or absolute path:")
		abs_path = expand_to_abs_path(input())
		print(Fore.BLUE + "\nUpdating shallow-backup path to {}".format(abs_path) + Style.RESET_ALL)
		config["backup_path"] = abs_path
		write_config(config)
		mkdir_warn_overwrite(abs_path)
		move_git_repo(current_path, abs_path)


def prompt_for_git_url(repo):
	"""
	Ask user if they'd like to add a remote URL to their git repo.
	If yes, do it.
	"""
	if prompt_yes_no("Would you like to set a remote URL for this git repo?", Fore.GREEN):
		print_green_bold("Enter URL:")
		remote_url = input()
		git_set_remote(repo, remote_url)


def add_to_config():
	"""
	Prompt sequence for a user to add a path to the config file under
	either the dot or config sections.
	"""
	add_prompt = [inquirer.List('choice',
	                            message=Fore.GREEN + Style.BRIGHT + "Which section would you like to add this to?" + Fore.BLUE,
	                            choices=[' Dots',
	                                     ' Configs',
	                                     ])
	]

	section = inquirer.prompt(add_prompt).get('choice').strip().lower()
	config = get_config()

	# Prompt until we get a valid path.
	while True:
		print_green_bold("Enter a path to add to {}:".format(section))
		path = input()
		expanded_path = expand_to_abs_path(path)
		split_path = input_path.split("/")

		# Check if path exists.
		if not os.path.exists(expanded_path):
			print_red_bold("ERR: {} doesn't exist.".format(expanded_path))
			continue

		config_key = None
		if section == "dots":
			# Make sure it's actually a dotfile
			if split_path[-1][0] != ".":
				print_red_bold("ERR: Not a dotfile.")
				continue

			# Determine if adding to dotfiles or dotfolders
			if not os.path.isdir(expanded_path):
				config_key = "dotfiles"
				print_blue_bold("Adding {} to dotfile backup.".format(expanded_path))
			else:
				config_key = "dotfolders"
				print_blue_bold("Adding {} to dotfolder backup.".format(expanded_path))

			# Add path to config ensuring no duplicates.
			updated_config_key = set(config[config_key] + [path])
			config[config_key] = list(updated_config_key)
			write_config(config)
			break

		elif section == "config":
			# Prompt for folder name
			print_green_bold("Enter a name for this config:".format(section))
			dir_name = input()

			# Handle plist and regular config.
			if expanded_path.endswith(".plist"):
				config_key = "plist_path_to_dest_map"
				# Make dest path $SB/config/plist/FILENAME
				to_add_to_cfg = (expanded_path, os.path.join("plist", dir_name))
				print_blue_bold("Adding {} to plist backup.".format(expanded_path))
			else:
				config_key = "config_path_to_dest_map"
				to_add_to_cfg = (expanded_path, dir_name)
				print_blue_bold("Adding {} to config backup.".format(expanded_path))

			# Get dictionary of {path_to_backup: dest, ...}
			config_path_dict = config[config_key]
			config_path_dict[to_add_to_cfg[0]] = to_add_to_cfg[1]
			config[config_key] = config_path_dict
			write_config(config)
			break


def remove_from_config():
	"""
	Sequence of prompts for a user to remove a path from the config.
	2-layer selection screen. First screen is for choosing dot or
	config, and then next selection is for the specific path.
	"""
	# Get section to display.
	section_prompt = [inquirer.List('choice',
	                                message=Fore.GREEN + Style.BRIGHT + "Which section would you like to remove a path from?" + Fore.BLUE,
	                                choices=[' Dotfiles',
	                                         ' Dotfolders',
	                                         ' Configs'
	                                    ])
	]

	section = inquirer.prompt(section_prompt).get('choice').strip().lower()
	config = get_config()
	paths = config[section]
	# Get only backup paths, not dest paths if it's a dictionary.
	if type(paths) is dict:
		paths = list(paths.keys())

	print(paths)
	path_prompt = [inquirer.List('choice',
	                             message=Fore.GREEN + Style.BRIGHT + "Select a path to remove." + Fore.BLUE,
	                             choices=paths)
	]
	path_to_remove = inquirer.prompt(path_prompt).get('choice')
	print(path_to_remove, type(path_to_remove))
	print_blue_bold("Removing {} from backup...".format(path_to_remove))
	print(paths, type(paths))
	paths.remove(path_to_remove)
	config[section] = paths
	write_config(config)


def actions_menu_prompt():
	"""
	Prompt user for an action.
	"""
	questions = [inquirer.List('choice',
	                           message=Fore.GREEN + Style.BRIGHT + "What would you like to do?" + Fore.BLUE,
	                           choices=[' Back up all',
	                                    ' Back up configs',
	                                    ' Back up dotfiles',
	                                    ' Back up fonts',
	                                    ' Back up packages',
	                                    ' Reinstall all',
	                                    ' Reinstall configs',
	                                    ' Reinstall dotfiles',
	                                    ' Reinstall fonts',
	                                    ' Reinstall packages',
	                                    ' Add path to config',
	                                    ' Remove path from config',
	                                    ' Show config',
	                                    ' Destroy backup'
	                                    ],
	                           ),
	             ]

	answers = inquirer.prompt(questions)
	return answers.get('choice').strip().lower()
