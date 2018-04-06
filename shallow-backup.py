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

	# TODO splash
	pass


def backup_prompt():
	"""Use pick library to prompt user with choice of what to backup."""
	questions = [ inquirer.List('choice',
	                            message=Fore.BLUE + "What would you like to backup?" + Fore.YELLOW,
	                            choices=[' Dotfiles', ' Installs'],
	                            ),
		]

	answers = inquirer.prompt(questions)

	return answers.get('choice').strip().lower()


def backup_dotfiles():
	"""Creates `dotfiles` directory and places copies of dotfiles there."""

	sp.run("mkdir dotfiles", shell=True, stdout=sp.PIPE)


	home_path = os.path.expanduser('~')

	command_suffixes = [
		"/.pypirc ./dotfiles/pypirc.txt",
		"/.zshrc ./dotfiles/zshrc.txt",
		"/.bashrc ./dotfiles/bashrc.txt",
		"/.ssh ./dotfiles/ssh",
		"/.vim ./dotfiles/vim"
	]

	for x in command_suffixes:
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

	sp.run("mkdir installs", shell=True, stdout=sp.PIPE)

	command_list = [
		"brew",
		"brew cask",
		"npm",
		"gem",
		"pip"
	]

	for x in command_list:
		command = x + " list > installs/" + x + "_list.txt"
		sp.run(command, shell=True, stdout=sp.PIPE)

	# special case for system installs
	sp.run("ls /Applications/ > installs/applications_list.txt", stdout=sp.PIPE)


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

	# if any CL options, process those
	if complete or dotfiles or installs:

		# Complete backup, set everything to true.
		if complete:
			dotfiles, installs = True

		if dotfiles:
			backup_dotfiles()

		if installs:
			backup_installs()

	# no command line options, pick an option
	else:
		selection = backup_prompt()

		if selection == "dotfiles":
			backup_dotfiles()
		if selection == "installs":
			backup_installs()

def main():
	selection = backup_prompt()

	if selection is "dotfiles":
		backup_dotfiles()
	if selection is "installs":
		backup_installs()


if __name__ == '__main__':
	cli()
