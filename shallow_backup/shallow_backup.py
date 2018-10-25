import os
import sys
import click
from colorama import Fore, Style
from reinstall import reinstall_packages_from_lists, reinstall_config_files
from config import get_config, show_config, add_path_to_config, rm_path_from_config, write_config, create_config_file_if_needed, get_config_path
from utils import make_dir_warn_overwrite, destroy_backup_dir
from printing import print_version_info, prompt_yes_no, splash_screen
from backup import backup_all, backup_configs, backup_dotfiles, backup_fonts, backup_packages
from git_wrapper import git_init_if_needed, git_set_remote, git_add_all_commit_push, create_gitignore_if_needed
from prompts import actions_menu_prompt, prompt_for_git_url, prompt_for_path_update

########
# Globals
########

# TODO: Refactor this to the git file
COMMIT_MSG = {
	"fonts": "Back up fonts.",
	"packages": "Back up packages.",
	"configs": "Back up configs.",
	"complete": "Back up everything.",
	"dotfiles": "Back up dotfiles.,"
}


# TODO: Convert these two functions to store info in the actual config and just read from it.
def get_configs_path_mapping():
	"""
	Gets a dictionary mapping directories to back up to their destination path.
	"""
	return {
		"Library/Application Support/Sublime Text 2/Packages/User/": "sublime_2",
		"Library/Application Support/Sublime Text 3/Packages/User/": "sublime_3",
		"Library/Preferences/IntelliJIdea2018.2/": "intellijidea_2018.2",
		"Library/Preferences/PyCharm2018.2/": "pycharm_2018.2",
		"Library/Preferences/CLion2018.2/": "clion_2018.2",
		"Library/Preferences/PhpStorm2018.2": "phpstorm_2018.2",
		".atom/": "atom",
	}


def get_plist_mapping():
	"""
	Gets a dictionary mapping plist files to back up to their destination path.
	"""
	return {
		"Library/Preferences/com.apple.Terminal.plist": "plist/com.apple.Terminal.plist",
	}


# custom help options
@click.command(context_settings=dict(help_option_names=['-h', '-help', '--help']))
@click.option('--add', nargs=2, default=[None, None], type=(click.Choice(['dot', 'config', 'other']), str),
              help="Add path (relative to home dir) to be backed up. Arg format: [dots, configs, other] <PATH>")
@click.option('--rm', default=None, type=str, help="Remove path from config.")
@click.option('-show', is_flag=True, default=False, help="Show config file.")
@click.option('-complete', is_flag=True, default=False, help="Back up everything.")
@click.option('-dotfiles', is_flag=True, default=False, help="Back up dotfiles.")
@click.option('-configs', is_flag=True, default=False, help="Back up app config files.")
@click.option('-fonts', is_flag=True, default=False, help="Back up installed fonts.")
@click.option('-packages', is_flag=True, default=False, help="Back up package libraries.")
@click.option('-old_path', is_flag=True, default=False, help="Skip setting new back up directory path.")
@click.option('--new_path', default=None, help="Input a new back up directory path.")
@click.option('--remote', default=None, help="Input a URL for a git repository.")
@click.option('-reinstall_packages', is_flag=True, default=False, help="Reinstall packages from package lists.")
@click.option('-reinstall_configs', is_flag=True, default=False, help="Reinstall configs from configs backup.")
@click.option('-delete_config', is_flag=True, default=False, help="Remove config file.")
@click.option('-destroy_backup', is_flag=True, default=False, help='Removes the backup directory and its content.')
@click.option('-v', is_flag=True, default=False, help='Display version and author information and exit.')
def cli(add, rm, show, complete, dotfiles, configs, packages, fonts, old_path, new_path, remote, reinstall_packages,
        reinstall_configs, delete_config, destroy_backup, v):
	"""
	Easily back up installed packages, dotfiles, and more. You can edit which dotfiles are backed up in ~/.shallow-backup.
	"""
	backup_config_path = get_config_path()

	# No interface going to be displayed
	if any([v, delete_config, destroy_backup, show, rm]) or None not in add:
		if v:
			print_version_info()
		elif delete_config:
			os.remove(backup_config_path)
			print(Fore.RED + Style.BRIGHT + "Removed config file..." + Style.RESET_ALL)
		elif destroy_backup:
			backup_home_path = get_config()["backup_path"]
			destroy_backup_dir(backup_home_path)
		elif None not in add:
			add_path_to_config(add[0], add[1])
		elif rm:
			rm_path_from_config(rm)
		elif show:
			show_config()
		sys.exit()

	# Start CLI
	splash_screen()
	create_config_file_if_needed()
	backup_config = get_config()

	# User entered a new path, so update the config
	if new_path:
		abs_path = os.path.abspath(new_path)
		print(Fore.BLUE + Style.NORMAL + "\nUpdating shallow-backup path to -> " + Style.BRIGHT + "{}".format(
			abs_path) + Style.RESET_ALL)
		backup_config["backup_path"] = abs_path
		write_config(backup_config)

	# User didn't enter any CLI args so prompt for path update before showing menu
	elif not (old_path or complete or dotfiles or packages or fonts):
		prompt_for_path_update(backup_config)

	# Create backup directory and do git setup
	backup_home_path = get_config()["backup_path"]
	make_dir_warn_overwrite(backup_home_path)
	repo, new_git_repo_created = git_init_if_needed(backup_home_path)

	# Create default gitignore if we just ran git init
	if new_git_repo_created:
		create_gitignore_if_needed(backup_home_path)
		# Prompt user for remote URL
		if not remote:
			prompt_for_git_url(repo)

	# Set remote URL from CLI arg
	if remote:
		git_set_remote(repo, remote)

	dotfiles_path = os.path.join(backup_home_path, "dotfiles")
	configs_path = os.path.join(backup_home_path, "configs")
	packages_path = os.path.join(backup_home_path, "packages")
	fonts_path = os.path.join(backup_home_path, "fonts")

	# Command line options
	if any([complete, dotfiles, configs, packages, fonts, reinstall_packages, reinstall_configs]):
		if reinstall_packages:
			reinstall_packages_from_lists(packages_path)
		elif reinstall_configs:
			reinstall_config_files(configs_path)
		elif complete:
			backup_all(dotfiles_path, packages_path, fonts_path, configs_path)
			git_add_all_commit_push(repo, COMMIT_MSG["everything"])
		elif dotfiles:
			backup_dotfiles(dotfiles_path)
			git_add_all_commit_push(repo, COMMIT_MSG["dotfiles"])
		elif configs:
			backup_configs(configs_path)
			git_add_all_commit_push(repo, COMMIT_MSG["configs"])
		elif packages:
			backup_packages(packages_path)
			git_add_all_commit_push(repo, COMMIT_MSG["packages"])
		elif fonts:
			backup_fonts(fonts_path)
			git_add_all_commit_push(repo, COMMIT_MSG["fonts"])
	# No CL options, prompt for selection
	else:
		selection = actions_menu_prompt().lower().strip()
		if selection == "back up everything":
			backup_all(dotfiles_path, packages_path, fonts_path, configs_path)
			git_add_all_commit_push(repo, COMMIT_MSG["everything"])
		elif selection == "back up dotfiles":
			backup_dotfiles(dotfiles_path)
			git_add_all_commit_push(repo, COMMIT_MSG["dotfiles"])
		elif selection == "back up configs":
			backup_configs(configs_path)
			git_add_all_commit_push(repo, COMMIT_MSG["configs"])
		elif selection == "back up packages":
			backup_packages(packages_path)
			git_add_all_commit_push(repo, COMMIT_MSG["packages"])
		elif selection == "back up fonts":
			backup_fonts(fonts_path)
			git_add_all_commit_push(repo, COMMIT_MSG["fonts"])
		elif selection == "reinstall packages":
			reinstall_packages_from_lists(packages_path)
		elif selection == "reinstall configs":
			reinstall_config_files(configs_path)
		elif selection == "show config":
			show_config()
		elif selection == "destroy backup":
			if prompt_yes_no("Erase backup directory: {}?".format(backup_home_path), Fore.RED):
				destroy_backup_dir(backup_home_path)
			else:
				print("{} Exiting to prevent accidental deletion of backup directory... {}".format(
					Fore.RED, Style.RESET_ALL))

	sys.exit()


if __name__ == '__main__':
	"""
	I'm just here so I don't get fined.
	"""
	cli()
