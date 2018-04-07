# shallow-backup
# alichtman

import os
import sys
import click
import inquirer
import subprocess as sp
from colorama import Fore, Style
from constants import Constants


def splash_screen():

	print(Fore.YELLOW + Style.BRIGHT + "\n" +
"            dP                dP dP                              dP                         dP                         \n" +
"            88                88 88                              88                         88                         \n" +
"   ,d8888'  88d888b. .d8888b. 88 88 .d8888b. dP  dP  dP          88d888b. .d8888b. .d8888b. 88  .dP  dP    dP 88d888b. \n" +
"   Y8ooooo, 88'  `88 88'  `88 88 88 88'  `88 88  88  88 88888888 88'  `88 88'  `88 88'  `\"\" 88888\"   88    88 88'  `88 \n" +
"         88 88    88 88.  .88 88 88 88.  .88 88.88b.88'          88.  .88 88.  .88 88.  ... 88  `8b. 88.  .88 88.  .88 \n" +
"   `88888P' dP    dP `88888P8 dP dP `88888P' 8888P Y8P           88Y8888' `88888P8 `88888P' dP   `YP `88888P' 88Y888P' \n" +
"                                                                                                              88		\n" +
"                                                                                                              dP		\n" + Style.RESET_ALL)


def backup_prompt():
	"""Use pick library to prompt user with choice of what to backup."""
	questions = [ inquirer.List('choice',
	                            message=Fore.BLUE + "What would you like to backup?" + Fore.RED,
	                            choices=[' Dotfiles', ' Installs', ' All'],
	                            ),
		]

	answers = inquirer.prompt(questions)

	return answers.get('choice').strip().lower()


def backup_dotfiles():
	"""Creates `dotfiles` directory and places copies of dotfiles there."""

	sp.run("mkdir text_backup/dotfiles", shell=True, stdout=sp.PIPE)

	source_dest = [
		"/.pypirc text_backup/dotfiles/pypirc.txt",
		"/.zshrc text_backup/dotfiles/zshrc.txt",
		"/.bashrc text_backup/dotfiles/bashrc.txt",
		"/.ssh text_backup/dotfiles/ssh",
		"/.vim text_backup/dotfiles/vim"
	]

	home_path = os.path.expanduser('~')

	for x in source_dest:
		# directory copy
		if ".ssh" in x or ".vim" in x:
			command = "cp -R " + home_path + x
			print(command)
			sp.run(command, shell=True, stdout=sp.PIPE)
		else:
			command = "cp " + home_path + x
			print(command)
			sp.run(command, shell=True, stdout=sp.PIPE)


def backup_installs():
	"""Creates `installs` directory and places install list text files there."""
	sp.run("mkdir text_backup/installs", shell=True, stdout=sp.PIPE)

	command_list = [
		"brew",
		"brew cask",
		"npm",
		"gem",
		"pip"
	]

	for x in command_list:
		command = x + " list > text_backup/installs/" + x.replace(" ", "_") + "_list.txt"
		print("CMD", command)
		sp.run(command, shell=True, stdout=sp.PIPE)

	# special case for system installs
	sp.run("ls /Applications/ > text_backup/installs/applications_list.txt", shell=True, stdout=sp.PIPE)


######
# CLI
######

# custom help options
CONTEXT_SETTINGS = dict(help_option_names=['-h', '-help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-complete', is_flag=True, default=False, help="Backup everything.")
@click.option('-dotfiles', is_flag=True, default=False, help="Create backup folder of dotfiles.")
@click.option('-installs', is_flag=True, default=False, help="Create backup text files of app install lists.")
@click.option('-v', 	   is_flag=True, default=False, help='Display version and author information and exit.')
def cli(complete, dotfiles, installs, v):
	"""Easily create text documentation of installed applications, dotfiles, and more."""

	# Print version information
	if v:
		print('{} v{} by {} -> (Github: {})'.format(Constants.PROJECT_NAME, Constants.VERSION, Constants.AUTHOR_FULL_NAME, Constants.AUTHOR_GITHUB))
		sys.exit()

	splash_screen()

	# create text_backup dir
	sp.run("mkdir text_backup", shell=True, stdout=sp.PIPE)

	selection = ""

	# No CL options, input in terminal
	if not complete and not dotfiles and not installs:
		selection = backup_prompt()

	# CL options
	else:
		if complete:
			selection = "all"
		if dotfiles:
			selection = "dotfiles"
		if installs:
			selection = "installs"

	# Control Flow
	if selection == "all":
		backup_dotfiles()
		backup_installs()

	elif selection == "dotfiles":
		backup_dotfiles()

	elif selection == "installs":
		backup_installs()


if __name__ == '__main__':
	cli()
