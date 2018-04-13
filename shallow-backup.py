# shallow-backup
# alichtman

import os
from os.path import expanduser
import sys
import shutil
import configparser
import subprocess as sp

import click
import inquirer
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

def make_dir_warn_overwrite(path):
	"""Make destination dir if path doesn't exist. Warn if it does."""

	if not os.path.exists(path):
		print(Fore.GREEN + path, "was created." + Style.RESET_ALL)
		os.makedirs(path)
	else:
		# If confirmed, remove directory and recreate it. If not, exit program.
		questions = [ inquirer.List('choice',
	                            message=Fore.RED + "WARNING: {} will be overwritten. Is that okay?".format(path) + Fore.BLUE,
	                            choices=[' YES', ' NO'],
	                            ),
		]

		answers = inquirer.prompt(questions)

		print(Style.RESET_ALL)

		if answers.get('choice').strip().lower() == 'no':
			sys.exit()
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

	make_dir_warn_overwrite(path)

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

	make_dir_warn_overwrite(path)

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
	"""Creates list of all .ttf and .otf files in ~/Library/Fonts"""

	make_dir_warn_overwrite(path)

	font_list_path = "{}/installed_fonts.txt".format(path)
	print(font_list_path)

	command = "ls ~/Library/Fonts > " + font_list_path
	sp.run(command, shell=True, stdout=sp.PIPE)

	fonts = []

	print(Fore.GREEN + "Only including '.otf' and '.ttf' filetypes." + Style.RESET_ALL)

	# read list of fonts
	with open(font_list_path,"r") as f:
		fonts = f.readlines()

	# TODO: Better way to do this.
	# clear that file
	os.remove(font_list_path)

	with open(font_list_path, "w") as f:
		for font in fonts:
			if ".otf" in font or ".ttf" in font:
				f.write("{}".format(font))
			else:
				print("Skipped:", font.strip())


def backup_all(installs_path, dotfiles_path, fonts_path):
	"""Complete backup"""
	backup_dotfiles(dotfiles_path)
	backup_installs(installs_path)
	backup_fonts(fonts_path)


######
# CLI
######


def check_config(config_path, config):
	################
	# CONTROL FLOW #
	################
	#
	# if $HOME/.shallow-backup does not exist, create it.
	#
	# if the path is empty or -new_path flag, prompt for a new path
	# if the path is not empty and no -new_path flag, do nothing.
	#
	################

	new_path = False

	print(config_path)

	# if config file doesn't exist, create it.
	if not os.path.exists(config_path):
		config['USER'] = {'backup_path': 'DEFAULT'}

		with open(config_path, 'w') as f:
				config.write(f)

	# Now, let's check the config file.

	config.read(config_path)

	# path is not empty, user has set it already.
	if not config['USER']['backup_path'] == 'DEFAULT' and not new_path:
		print(Fore.GREEN + Style.DIM + "Reading path from config file..." + Style.RESET_ALL)
		return
	# if path is empty or new_path flag, prompt for new path
	else:
		print(Fore.GREEN + Style.BRIGHT + "Enter absolute path for backup dir or enter '.' to set path to shallow-backup dir here.")

		user_in = input()

		if user_in == ".":
			print(Fore.GREEN + Style.BRIGHT + "Updating config file shallow-backup path to this directory...")
			config['USER']['backup_path'] = os.path.abspath("shallow-backup/")
		else:
			print(Fore.GREEN + Style.BRIGHT + "Updating config file shallow-backup path to {}...").format(user_in)
			config['USER']['backup_path'] = user_in

		# Write to config file
		with open(config_path, 'w') as f:
			config.write(f)


def read_config(config_path, config):
	"""Read config file and make directory if it doesn't exist. Warn if it does."""
	config.read(config_path)
	backup_dir = config['USER']['backup_path']
	make_dir_warn_overwrite(backup_dir)
	return backup_dir


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

	################
	# CONTROL FLOW #
	################
	#
	# Check if $HOME/.shallow-backup exists
	# 	if yes, read it.
	# 		if the path is empty or -new_path flag, prompt for a new path
	# 		if the path is not empty and no -new_path flag, do nothing.
	# 	if no, create it
	# 		prompt for new path
	#
	# Read backup directory path out of $HOME/.shallow-backup
	#
	################

	config_path = os.path.join(expanduser("~"), ".shallow-backup-config")
	config = configparser.ConfigParser()

	check_config(config_path, config)
	path = read_config(config_path, config)

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
