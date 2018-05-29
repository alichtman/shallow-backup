# shallow_backup
# alichtman

import os
from os.path import expanduser
import sys
import glob
import shutil
import configparser
import subprocess as sp
import multiprocessing as mp

import click
import inquirer
from colorama import Fore, Style
from pprint import pprint

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
	"""Make destination dir if path doesn't exist, confirm before overwriting if it does."""
	if os.path.exists(path) and path.split("/")[-1] in ["dotfiles", "packages", "fonts"]:
		print(Fore.RED + Style.BRIGHT + "Directory {} already exists".format(path) + "\n" + Style.RESET_ALL)
		if prompt_yes_no("Erase directory and make new back up?", Fore.RED):
			shutil.rmtree(path)
			os.makedirs(path)
		else:
			print(Fore.Red + "Exiting to prevent accidental deletion of user data." + Style.RESET_ALL)
			sys.exit()
	elif not os.path.exists(path):
		os.makedirs(path)
		print(Fore.RED + Style.BRIGHT + "CREATED DIR: " + Style.NORMAL + path + Style.RESET_ALL)

	return


def backup_prompt():
	"""Use pick library to prompt user with choice of what to backup."""
	questions = [inquirer.List('choice',
	                           message=Fore.GREEN + Style.BRIGHT + "What would you like to do?" + Fore.BLUE,
	                           choices=[' Back up dotfiles', ' Back up packages', ' Back up fonts',
	                                    ' Back up everything', ' Reinstall packages'],
	                           ),
	             ]

	answers = inquirer.prompt(questions)

	return answers.get('choice').strip().lower()


def copy_dotfolder(dotfolder, backup_path):
	"""Copy dotfolder from $HOME."""

	print(dotfolder)

	invalid = {".Trash", ".npm", ".cache", ".rvm"}

	if len(invalid.intersection(set(dotfolder.split("/")))) == 0:
		command = ""
		if "Library" in dotfolder.split("/") and "Preferences" in dotfolder.split("/"):
			command = "cp -aRp " + dotfolder + " " + backup_path + "/macOS_Preferences"
			print(Fore.BLUE + command)
		elif "Application\ Support" not in dotfolder or "XCode" in dotfolder:
			command = "cp -aRp " + dotfolder + " " + backup_path + "/" + dotfolder.split("/")[-2]
		elif "Sublime" in dotfolder:
			command = "cp -aRp " + dotfolder + " " + backup_path + "/" + dotfolder.split("/")[-3]
		sp.run(command, shell=True, stdout=sp.PIPE)


def copy_dotfile(dotfile, backup_path):
	"""Copy dotfile from $HOME."""

	command = "cp -a " + dotfile + " " + backup_path
	# print(command)
	sp.run(command, shell=True, stdout=sp.PIPE)


def backup_dotfiles(backup_path):
	"""
	Create `dotfiles` dir and makes copies of dotfiles and dotfolders.
	"""

	print_section_header("DOTFILES", Fore.BLUE)
	make_dir_warn_overwrite(backup_path)

	# assumes dotfiles are stored in home directory
	home_path = os.path.expanduser('~')

	# get dotfolders and dotfiles

	dotfiles_for_backup = [".bashrc", ".bash_profile", ".gitconfig", ".pypirc", ".shallow-backup", ".zshrc"]
	dotfolders_for_backup = [".ssh", ".vim"]

	# Add dotfile/folder for backup if it exists on the machine
	dotfiles = [file for file in dotfiles_for_backup if os.path.isfile(os.path.join(home_path, file))]
	dotfolders = [folder for folder in dotfolders_for_backup if os.path.isdir(os.path.join(home_path, folder))]

	# dotfiles/dotfolders multiprocessing in list format: [(full_backup_path, full dotfolder path), ...]

	dotfiles_mp_in = []
	for dotfile in dotfiles:
		dotfiles_mp_in.append((os.path.join(home_path, dotfile), os.path.join(backup_path, dotfile)))

	dotfolders_mp_in = []
	for dotfolder in dotfolders:
		dotfolders_mp_in.append((dotfolder, backup_path))

	####
	# Back up System and Application Preferences and Settings
	####

	# Sublime Text Configs
	if os.path.isdir("/Users/alichtman/Library/Application Support/Sublime\ Text\ 2"):
		dotfolders_mp_in.append((os.path.join(home_path, "Library/Application\ Support/Sublime\ Text\ 2/Packages/User"), backup_path))

	if os.path.isdir("/Users/alichtman/Library/Application Support/Sublime\ Text\ 3"):
		dotfolders_mp_in.append((os.path.join(home_path, "Library/Application\ Support/Sublime\ Text\ 3/Packages/User"), backup_path))

	# XCode Configs
	if os.path.isdir("/Users/alichtman/Library/Developer/Xcode/UserData"):
		dotfolders_mp_in.append(("/Users/alichtman/Library/Developer/Xcode/UserData", backup_path))

	# Multiprocessing
	with mp.Pool(mp.cpu_count()):

		print(Fore.BLUE + Style.BRIGHT + "Backing up dotfolders..." + Style.RESET_ALL)
		for x in dotfolders_mp_in:
			x = list(x)
			mp.Process(target=copy_dotfolder, args=(x[0], x[1],)).start()

	with mp.Pool(mp.cpu_count()):
		print(Fore.BLUE + Style.BRIGHT + "Backing up dotfiles..." + Style.RESET_ALL)
		for x in dotfiles_mp_in:
			x = list(x)
			mp.Process(target=copy_dotfile, args=(x[0], x[1],)).start()


def backup_packages(backup_path):
	"""Creates `packages` directory and places install list text files there."""

	print_section_header("PACKAGES", Fore.BLUE)

	make_dir_warn_overwrite(backup_path)

	package_managers = [
		"brew",
		"brew cask",
		"gem"
	]

	for mgr in package_managers:
		# deal with package managers that have spaces in them.
		print(Fore.BLUE + "Backing up {} package list...".format(mgr) + Style.RESET_ALL)
		command = "{0} list > {1}/{2}_list.txt".format(mgr, backup_path, mgr.replace(" ", "-"))
		sp.run(command, shell=True, stdout=sp.PIPE)

	# pip
	print(Fore.BLUE + "Backing up {} package list...".format(mgr) + Style.RESET_ALL)
	sp.run("pip list --format=freeze > {}/pip_list.txt".format(backup_path), shell=True, stdout=sp.PIPE)

	# npm
	print(Fore.BLUE + "Backing up npm package list..." + Style.RESET_ALL)
	sp.run("npm ls --parseable=true > {}/npm_temp_list.txt".format(backup_path), shell=True, stdout=sp.PIPE)
	# Parse npm output
	with open("{0}/npm_temp_list.txt".format(backup_path), mode="r+") as f:
		# Skip first line of file
		skip = True
		sp.run("touch {0}/npm_list.txt".format(backup_path), shell=True, stdout=sp.PIPE)
		with open("{0}/npm_list.txt".format(backup_path), mode="r+") as dest:
			for line in f:
				if not skip:
					dest.write(line.split("/")[-1])
				skip = False

	# remove temp file
	sp.run("rm {}/npm_temp_list.txt".format(backup_path), shell=True, stdout=sp.PIPE)

	# atom package manager
	print(Fore.BLUE + "Backing up Atom package list..." + Style.RESET_ALL)
	sp.run("apm list --installed --bare > {}/apm_list.txt".format(backup_path), shell=True, stdout=sp.PIPE)

	# sublime text packages
	if os.path.isdir("/Users/alichtman/Library/Application Support/Sublime Text 2"):
		print(Fore.BLUE + "Backing up Sublime Text package list..." + Style.RESET_ALL)
		sp.run("ls /Users/alichtman/Library/Application\ Support/Sublime\ Text\ 2/Packages/ > {}/sublime2_list.txt"
		       .format(backup_path), shell=True, stdout=sp.PIPE)

	if os.path.isdir("/Users/alichtman/Library/Application Support/Sublime Text 3"):
		print(Fore.BLUE + "Backing up Sublime Text package list..." + Style.RESET_ALL)
		sp.run("ls /Users/alichtman/Library/Application\ Support/Sublime\ Text\ 3/Installed\ Packages/ > {}/sublime3_list.txt"
		       .format(backup_path), shell=True, stdout=sp.PIPE)

	# macports
	print(Fore.BLUE + "Backing up macports package list..." + Style.RESET_ALL)
	sp.run("port installed requested > {}/macports_list.txt".format(backup_path), shell=True, stdout=sp.PIPE)

	# system installs
	print(Fore.BLUE + "Backing up system application list..." + Style.RESET_ALL)
	sp.run("ls /Applications/ > {}/installed_apps_list.txt".format(backup_path), shell=True, stdout=sp.PIPE)


def backup_fonts(path):
	"""Creates list of all .ttf and .otf files in ~/Library/Fonts"""

	print_section_header("FONTS", Fore.BLUE)
	make_dir_warn_overwrite(path)

	# Copy fonts
	print(Fore.BLUE + "Copying '.otf' and '.ttf' fonts..." + Style.RESET_ALL)
	copy_ttf = "cp ~/Library/Fonts/*.ttf {}/".format(path)
	copy_otf = "cp ~/Library/Fonts/*.otf {}/".format(path)

	sp.run(copy_otf, shell=True, stdout=sp.PIPE)
	sp.run(copy_ttf, shell=True, stdout=sp.PIPE)

	print(copy_otf)
	print(copy_ttf, "\n")


def backup_all(dotfiles_path, packages_path, fonts_path):
	"""Complete backup"""
	backup_dotfiles(dotfiles_path)
	backup_packages(packages_path)
	backup_fonts(fonts_path)


def get_subfiles(directory):
	"""Returns list of immediate subfiles"""
	return next(os.walk(directory))[2]


def reinstall_packages(packages_path):
	"""Reinstall all packages from the files in backup/installs."""

	# Figure out which install lists they have saved
	package_mgrs = set()
	for file in get_subfiles(packages_path):
		print(file)
		manager = file.split("_")[0].replace("-", " ")
		if manager != "installed":
			package_mgrs.add(file.split("_")[0])

	pprint(package_mgrs)

	# construct commands
	for pm in package_mgrs:
		if pm in ["brew", "brew-cask"]:
			cmd = "xargs {0} install < {1}/{2}_list.txt".format(pm.replace("-", " "), packages_path, pm)
			print(cmd)
			sp.call(cmd, shell=True, stdout=sp.PIPE)
		elif pm == "npm":
			cmd = "cat {0}/npm_list.txt | xargs npm install -g".format(packages_path)
			print(cmd)
			sp.call(cmd, shell=True, stdout=sp.PIPE)
		elif pm == "pip":
			cmd = "pip install -r {0}/pip_list.txt".format(packages_path)
			print(cmd)
			sp.call(cmd, shell=True, stdout=sp.PIPE)
		elif pm == "apm":
			cmd = "apm install --packages-file {0}/apm_list.txt".format(packages_path)
			print(cmd)
			sp.call(cmd, shell=True, stdout=sp.PIPE)
		elif pm == "macports":
			print(Fore.RED + "WARNING: Macports reinstallation is not supported." + Style.RESET_ALL)
		elif pm == "gem":
			print(Fore.RED + "WARNING: Gem reinstallation is not supported." + Style.RESET_ALL)

	sys.exit()


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
@click.option('-complete', is_flag=True, default=False, help="Back up everything.")
@click.option('-dotfiles', is_flag=True, default=False, help="Back up dotfiles.")
@click.option('-fonts', is_flag=True, default=False, help="Back up installed fonts.")
@click.option('-packages', is_flag=True, default=False, help="Back up package libraries and installed applications.")
@click.option('-old_path', is_flag=True, default=False, help="Skip setting new back up directory path.")
@click.option('--new_path', default="DEFAULT", help="Input a new back up directory path.")
@click.option('-reinstall', is_flag=True, default=False, help="Reinstall packages from package lists.")
@click.option('-delete_config', is_flag=True, default=False, help="Remove config file.")
@click.option('-v', is_flag=True, default=False, help='Display version and author information and exit.')
def cli(complete, dotfiles, packages, fonts, old_path, new_path, reinstall, delete_config, v):
	"""Easily back up installed packages, dotfiles, and more."""

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
		print(Fore.RED + Style.BRIGHT + "Removed config file..." + Style.RESET_ALL)
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
	elif old_path or complete or dotfiles or packages or fonts:
		pass

	# User didn't enter a new path, didn't use the same_path flag or any backup options, so prompt
	else:
		prompt_for_path_update(config_path, config)

	backup_home_path = read_config(config_path, config)

	dotfiles_path = os.path.join(backup_home_path, "dotfiles")
	packages_path = os.path.join(backup_home_path, "packages")
	fonts_path = os.path.join(backup_home_path, "fonts")

	print(packages_path)

	# Command line options
	if complete or dotfiles or packages or fonts or reinstall:
		if reinstall:
			reinstall_packages(packages_path)
		elif complete:
			backup_all(dotfiles_path, packages_path, fonts_path)
		elif dotfiles:
			backup_dotfiles(dotfiles_path)
		elif packages:
			backup_packages(packages_path)
		elif fonts:
			backup_fonts(fonts_path)

		return

	# No CL options, prompt for selection
	else:
		selection = backup_prompt().lower().strip()

		if selection == "back up everything":
			backup_all(dotfiles_path, packages_path, fonts_path)
		elif selection == "back up dotfiles":
			backup_dotfiles(dotfiles_path)
		elif selection == "back up packages":
			backup_packages(packages_path)
		elif selection == "back up fonts":
			backup_fonts(fonts_path)
		elif selection == "reinstall packages":
			reinstall_packages(packages_path)
		return


if __name__ == '__main__':
	cli()
