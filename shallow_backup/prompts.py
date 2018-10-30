import os
import inquirer
from utils import *
from printing import *
from colorama import Fore, Style
from config import write_config
from git_wrapper import git_set_remote, move_git_repo


def prompt_for_path_update(config):
	"""
	Ask user if they'd like to update the backup path or not.
	If yes, update. If no... don't.
	"""
	current_path = config["backup_path"]
	print("{}{}Current shallow-backup path: {}{}{}".format(Fore.BLUE, Style.BRIGHT, Style.NORMAL, current_path, Style.RESET_ALL))

	if prompt_yes_no("Would you like to update this?", Fore.GREEN):
		print(Fore.GREEN + Style.BRIGHT + "Enter relative or absolute path:" + Style.RESET_ALL)
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


def add_to_config_prompt():
	"""
	Show selector for dot or config. Then prompt for path, do error
	checking and add it to the config.
	"""
	section = [inquirer.List('choice',
	                         message=Fore.GREEN + Style.BRIGHT + "Which section would you like to add this to?" + Fore.BLUE,
	                         choices=[' Dots',
	                                  ' Configs',
	                                  ])
	]

	section = inquirer.prompt(section).get('choice').strip().lower()
	valid_path = False

	while not valid_path:
		print_green_bold("Enter a path to add to {}:".format(section))
		path = input()

	pass


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
