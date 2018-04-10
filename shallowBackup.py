# shallowBackup
# alichtman

import os
import sys
import click
import shutil
import inquirer
import configparser
import subprocess as sp
from colorama import Fore, Style
from constants import Constants


def splash_screen():

	print(Fore.YELLOW + Style.BRIGHT + "\n" +
"            dP                dP dP                        dP                         dP                         \n" +
"            88                88 88                        88                         88                         \n" +
"   ,d8888'  88d888b. .d8888b. 88 88 .d8888b. dP  dP  dP    88d888b. .d8888b. .d8888b. 88  .dP  dP    dP 88d888b. \n" +
"   Y8ooooo, 88'  `88 88'  `88 88 88 88'  `88 88  88  88    88'  `88 88'  `88 88'  `\"\" 88888\"   88    88 88'  `88 \n" +
"         88 88    88 88.  .88 88 88 88.  .88 88.88b.88'    88.  .88 88.  .88 88.  ... 88  `8b. 88.  .88 88.  .88 \n" +
"   `88888P' dP    dP `88888P8 dP dP `88888P' 8888P Y8P     88Y8888' `88888P8 `88888P' dP   `YP `88888P' 88Y888P' \n" +
"                                                                                                         88		\n" +
"                                                                                                         dP		\n" + Style.RESET_ALL)

def overwrite_make_dir(path):
	"""Make destination dir if it doesn't exist. Overwrite if it does."""

	if not os.path.exists(path):
		print(Fore.GREEN + path, "was created." + Style.RESET_ALL)
		os.makedirs(path)
	else:
		shutil.rmtree(path)
		os.makedirs(path)
		print(Fore.RED + path, "was removed and an updated directory was created." + Style.RESET_ALL)

def backup_prompt():
	"""Use pick library to prompt user with choice of what to backup."""
	questions = [ inquirer.List('choice',
	                            message=Fore.BLUE + "What would you like to backup?" + Fore.RED,
	                            choices=[' Dotfiles', ' Installs', ' Fonts', ' All'],
	                            ),
		]

	answers = inquirer.prompt(questions)

	return answers.get('choice').strip().lower()


def backup_dotfiles(path):
	"""Creates `dotfiles` directory and places copies of dotfiles there."""

	overwrite_make_dir(path)

	source_dest = [
		"/.pypirc {}/pypirc.txt".format(path),
		"/.zshrc {}/zshrc.txt".format(path),
		"/.bashrc {}/bashrc.txt".format(path),
		"/.ssh {}/ssh".format(path),
		"/.vim {}/vim".format(path)
	]

	# assumes dotfiles are stored in home directory
	home_path = os.path.expanduser('~')

	for x in source_dest:
		# directory copy
		if ".ssh" in x or ".vim" in x:
			command = "cp -R " + home_path + x
			print(command)
			sp.run(command, shell=True, stdout=sp.PIPE)

		# file copy
		else:
			command = "cp " + home_path + x
			print(command)
			sp.run(command, shell=True, stdout=sp.PIPE)


def backup_installs(path):
	"""Creates `installs` directory and places install list text files there."""

	overwrite_make_dir(path)

	command_list = [
		"brew",
		"brew cask",
		"npm",
		"gem",
		"pip"
	]

	for x in command_list:
		command = ""

		if " " not in x:
			command = x + " list > {}/".format(path) + "_list.txt"
		else:
			command = x + " list > {}/".format(path) + x.replace(" ", "_") + "_list.txt"

		print(command)
		sp.run(command, shell=True, stdout=sp.PIPE)

	# special case for system installs
	sp.run("ls /Applications/ > {}/applications_list.txt".format(path), shell=True, stdout=sp.PIPE)


def backup_fonts(path):

	overwrite_make_dir(path)

	command = "ls /Library/Fonts > {}/installed_fonts.txt".format(path)
	sp.run(command, shell=True, stdout=sp.PIPE)


def backup_all(installs_path, dotfiles_path, fonts_path):
	"""Complete backup"""
	backup_dotfiles(dotfiles_path)
	backup_installs(installs_path)
	backup_fonts(fonts_path)


######
# CLI
######

# custom help options
CONTEXT_SETTINGS = dict(help_option_names=['-h', '-help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-complete', is_flag=True, default=False, help="Backup everything.")
@click.option('-dotfiles', is_flag=True, default=False, help="Create backup of dotfiles.")
@click.option('-fonts',    is_flag=True, default=False, help="Create backup of installed fonts.")
@click.option('-installs', is_flag=True, default=False, help="Create backup of installs.")
@click.option('-v', 	   is_flag=True, default=False, help='Display version and author information and exit.')
def cli(complete, dotfiles, installs, fonts, v):
	"""Easily create text documentation of installed applications, dotfiles, and more."""

	# Print version information
	if v:
		print('{} v{} by {} -> (Github: {})'.format(Constants.PROJECT_NAME, Constants.VERSION, Constants.AUTHOR_FULL_NAME, Constants.AUTHOR_GITHUB))
		sys.exit()

	splash_screen()

	# Read config file
	config = configparser.ConfigParser()
	config.read("config.ini")
	path = config['Paths']['backup_dir']
	# print("Backup Dir", path)

	# if path is "", that means that user has never run before.
	if path == "":
		# Make sure folder with that path doesn't exist already
		if not os.path.exists("shallow_backup"):
			print(Fore.GREEN + Style.BRIGHT + "Creating default shallow_backup directory in this folder.")
			overwrite_make_dir("shallow_backup")

			# get absolute path, write it to config file, set for later in program
			path = os.path.abspath("./shallow_backup")
			config['Paths']['backup_dir'] = path

			with open('config.ini', 'w') as configfile:
				config.write(configfile)

			# print("Abs path:", path)

		# Edge case: User has shallow_backup dir that was not created by this program (or by an older version of this program)
		else:
			print(Fore.GREEN + Style.BRIGHT + "ERROR: shallow_backup directory already in this folder.")
			sys.exit()

	# path is not "". Use absolute path in config file.
	else:
		print(Fore.GREEN + Style.BRIGHT + "Reading config file to get `shallow_backup` directory path." + Style.RESET_ALL, end="\n\n")

	dotfiles_path = os.path.join(path, "dotfiles")
	installs_path = os.path.join(path, "installs")
	fonts_path = os.path.join(path, "fonts")

	# print("Dots:", dotfiles_path)
	# print("Installs:", installs_path)

	# Command line options
	if complete or dotfiles or installs or fonts:
		if complete:
			backup_all(dotfiles_path, installs_path, fonts_path)
		elif dotfiles:
			backup_dotfiles(dotfiles_path)
		elif installs:
			backup_installs(installs_path)
		elif fonts:
			backup_fonts(fonts_path)

		return

	# No CL options, input in terminal
	else:
		selection = backup_prompt()

		if selection == "all":
			backup_all(dotfiles_path, installs_path, fonts_path)
		elif selection == "dotfiles":
			backup_dotfiles(dotfiles_path)
		elif selection == "installs":
			backup_installs(installs_path)
		elif selection == "fonts":
			backup_fonts(fonts_path)
		return


if __name__ == '__main__':
	cli()
