# shallow_backup
# alichtman

import os
from os.path import expanduser
import sys
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
	      "                                                                                                        88		\n" +
	      "                                                                                                        dP		\n" +
	      Style.RESET_ALL)


def prompt_yes_no(message, color):
	"""Print question and return True or False depending on user selection from list.
	bottom_line should be used for one liners. Otherwise, it's the second line you want printed."""
	questions = [inquirer.List('choice',
	                           message=color + Style.BRIGHT + message + Fore.BLUE,
	                           choices=[' Yes', ' No'],
	                           ),
	             ]

	answers = inquirer.prompt(questions)
	return answers.get('choice').strip().lower() == 'yes'


def print_section_header(title, COLOR):
	"""Prints variable sized section header"""
	block = "#" * (len(title) + 2)
	print("\n" + COLOR + Style.BRIGHT + block)
	print("#", title)
	print(block + "\n" + Style.RESET_ALL)


def make_dir_warn_overwrite(path):
	"""Make destination dir if path doesn't exist. Warn if it does."""

	if os.path.exists(path):
		print(Fore.RED + Style.BRIGHT + "Directory {} already exists".format(path) + "\n" + Style.RESET_ALL)
		return
	else:
		os.makedirs(path)
		print(Fore.RED + Style.BRIGHT + "CREATED DIR: " + Style.NORMAL + path + Style.RESET_ALL)


def backup_prompt():
	"""Use pick library to prompt user with choice of what to backup."""
	questions = [inquirer.List('choice',
	                           message=Fore.GREEN + Style.BRIGHT + "What would you like to backup?" + Fore.BLUE,
	                           choices=[' Dotfiles', ' Installs', ' Fonts', ' All'],
	                           ),
	             ]

	answers = inquirer.prompt(questions)

	return answers.get('choice').strip().lower()


def backup_dotfiles(path):
	"""Creates `dotfiles` directory and places copies of dotfiles there."""

	print_section_header("DOTFILES", Fore.BLUE)

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

	print_section_header("INSTALLS", Fore.BLUE)

	make_dir_warn_overwrite(path)

	package_managers = [
		"brew",
		"brew cask",
		"npm",
		"gem",
		"pip"
	]

	for mgr in package_managers:
		# deal with package managers that have spaces in them.
		command = "{0} list > {1}/{2}_list.txt".format(mgr, path, mgr.replace(" ", "_"))
		print(command)
		sp.run(command, shell=True, stdout=sp.PIPE)

	# special case for system installs
	sp.run("ls /Applications/ > {}/applications_list.txt".format(path), shell=True, stdout=sp.PIPE)


def backup_fonts(path):
	"""Creates list of all .ttf and .otf files in ~/Library/Fonts"""

	print_section_header("FONTS", Fore.BLUE)
	make_dir_warn_overwrite(path)

	# Get font list

	font_list_path = "{}/installed_fonts.txt".format(path)
	print(font_list_path)

	command = "ls ~/Library/Fonts > " + font_list_path
	sp.run(command, shell=True, stdout=sp.PIPE)

	# read list of fonts
	with open(font_list_path, "r") as f:
		fonts = f.readlines()

	# clear that file
	os.remove(font_list_path)

	with open(font_list_path, "w") as f:
		for font in fonts:
			if ".otf" in font or ".ttf" in font:
				f.write("{}".format(font))

	# Copy fonts
	print(Fore.BLUE + "Copying '.otf' and '.ttf' fonts..." + Style.RESET_ALL)
	copy_ttf = "cp ~/Library/Fonts/*.ttf {}/".format(path)
	copy_otf = "cp ~/Library/Fonts/*.otf {}/".format(path)

	sp.run(copy_otf, shell=True, stdout=sp.PIPE)
	sp.run(copy_ttf, shell=True, stdout=sp.PIPE)

	print(copy_otf)
	print(copy_ttf, "\n")


def backup_all(dotfiles_path, installs_path, fonts_path):
	"""Complete backup"""
	backup_dotfiles(dotfiles_path)
	backup_installs(installs_path)
	backup_fonts(fonts_path)


######
# CLI
######


def prompt_for_path_update(config_path, config):
	"""Ask user if they'd like to update the backup path or not. If yes, update. If no... don't."""
	config.read(config_path)

	# Prompt for update
	print(Fore.BLUE + Style.BRIGHT + "Current shallow-backup path -> " + Style.NORMAL + "{}".format(
		config['USER']['backup_path']) + Style.RESET_ALL)

	if prompt_yes_no("Would you like to update this?", Fore.GREEN):
		print(Fore.GREEN + Style.BRIGHT + "Enter relative path:" + Style.RESET_ALL)

		abs_path = os.path.abspath(input())

		print(Fore.BLUE + "\nUpdating shallow-backup path to {}".format(abs_path) + Style.RESET_ALL)
		config['USER']['backup_path'] = abs_path

		# Write to config file
		with open(config_path, 'w') as f:
			config.write(f)


def read_config(config_path, config):
	"""Read config file. Make home backup directory if it doesn't exist. Warn user if it already exists."""
	config.read(config_path)
	backup_dir = config['USER']['backup_path']
	make_dir_warn_overwrite(backup_dir)
	return backup_dir


# custom help options
@click.command(context_settings=dict(help_option_names=['-h', '-help']))
@click.option('-complete', is_flag=True, default=False, help="Backup everything.")
@click.option('-dotfiles', is_flag=True, default=False, help="Create backup of dotfiles.")
@click.option('-fonts', is_flag=True, default=False, help="Create backup of installed fonts.")
@click.option('-installs', is_flag=True, default=False, help="Create backup of installs.")
@click.option('-old_path', is_flag=True, default=False, help="Decline setting new backup directory path.")
@click.option('--new_path', default="DEFAULT", help="Input a new backup directory path.")
@click.option('-delete_config', is_flag=True, default=False, help="Remove config file.")
@click.option('-v', is_flag=True, default=False, help='Display version and author information and exit.')
def cli(complete, dotfiles, installs, fonts, old_path, new_path, delete_config, v):
	"""Easily create text documentation of installed applications, dotfiles, and more."""

	config_path = os.path.join(expanduser("~"), ".shallow-backup")

	# Print version information
	if v:
		print(
			'{} v{} by {} -> (Github: {})'.format(Constants.PROJECT_NAME,
			                                      Constants.VERSION,
			                                      Constants.AUTHOR_FULL_NAME,
			                                      Constants.AUTHOR_GITHUB))
		sys.exit()

	elif delete_config:
		command = "rm {}".format(config_path)
		sp.run(command, shell=True, stdout=sp.PIPE)
		print(Fore.RED + Style.BRIGHT + "Removed config file...")
		sys.exit()

	splash_screen()

	# CONFIG FILE

	config = configparser.ConfigParser()

	# if config file doesn't exist, create it.
	if not os.path.exists(config_path):
		print(Fore.BLUE + Style.BRIGHT + "Creating config file at {}".format(config_path))
		config['USER'] = {'backup_path': 'DEFAULT'}
		with open(config_path, 'w') as f:
			config.write(f)

	# Decide to update path from CLI args, prompt user, or skip updating

	# User entered a new path in, update the config
	if not new_path == "DEFAULT":

		abs_path = os.path.abspath(new_path)

		print(Fore.BLUE + "\nUpdating shallow-backup path to -> " + Style.BRIGHT + "{}".format(
			abs_path) + Style.RESET_ALL)
		config.read(config_path)
		config['USER']['backup_path'] = abs_path

		# Write to config file
		with open(config_path, 'w') as f:
			config.write(f)

	# User didn't enter the same_path flag but entered a backup option, so no path update prompt
	elif old_path or complete or dotfiles or installs or fonts:
		pass

	# User didn't enter a new path, didn't use the same_path flag or any backup options, so prompt
	else:
		prompt_for_path_update(config_path, config)

	backup_home_path = read_config(config_path, config)

	dotfiles_path = os.path.join(backup_home_path, "dotfiles")
	installs_path = os.path.join(backup_home_path, "installs")
	fonts_path = os.path.join(backup_home_path, "fonts")

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

	# No CL options, prompt for selection
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
