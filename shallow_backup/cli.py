import os
import sys
import click
from printing import *
from utils import mkdir_warn_overwrite, destroy_backup_dir, expand_path_to_absolute
from reinstall import reinstall_packages_sb, reinstall_configs_sb, reinstall_all_sb, reinstall_fonts_sb, reinstall_dots_sb
from prompts import actions_menu_prompt, prompt_for_git_url, prompt_for_path_update
from backup import backup_all, backup_configs, backup_dotfiles, backup_fonts, backup_packages
from git_wrapper import safe_git_init, git_set_remote, git_add_all_commit_push, safe_create_gitignore
from config import get_config, show_config, add_to_config, rm_from_config, write_config, safe_create_config, get_config_path


# custom help options
@click.command(context_settings=dict(help_option_names=['-h', '-help', '--help']))
@click.option('--add', nargs=2, default=[None, None], type=(click.Choice(['dot', 'config']), str),
              help="\b Add path to back up. Format: [dot, config] PATH")
@click.option('-all', is_flag=True, default=False, help="Full back up.")
@click.option('-configs', is_flag=True, default=False, help="Back up app config files.")
@click.option('-delete_config', is_flag=True, default=False, help="Delete config file.")
@click.option('-destroy_backup', is_flag=True, default=False, help='Delete backup directory.')
@click.option('-dotfiles', is_flag=True, default=False, help="Back up dotfiles.")
@click.option('-fonts', is_flag=True, default=False, help="Back up installed fonts.")
@click.option('--new_path', default=None, help="Input a new back up directory path.")
@click.option('-old_path', is_flag=True, default=False, help="Skip setting new back up directory path prompt.")
@click.option('-packages', is_flag=True, default=False, help="Back up package libraries.")
@click.option('-reinstall_configs', is_flag=True, default=False, help="Reinstall configs.")
@click.option('-reinstall_dots', is_flag=True, default=False, help="Reinstall dotfiles and dotfolders.")
@click.option('-reinstall_fonts', is_flag=True, default=False, help="Reinstall fonts.")
@click.option('-reinstall_packages', is_flag=True, default=False, help="Reinstall packages.")
@click.option('-reinstall_all', is_flag=True, default=False, help="Full reinstallation.")
@click.option('--remote', default=None, help="Set remote URL for the git repo.")
@click.option('--rm', default=None, type=str, help="Remove path from backup.")
@click.option('-show', is_flag=True, default=False, help="Display config file.")
@click.option('-v', is_flag=True, default=False, help='Display version and author information and exit.')
def cli(add, rm, show, all, dotfiles, configs, packages, fonts, old_path, new_path, remote, reinstall_all,
        reinstall_configs, reinstall_dots, reinstall_fonts, reinstall_packages, delete_config, destroy_backup, v):
	"""
	\b
	Easily back up installed packages, dotfiles, and more.
	You can edit which files are backed up in ~/.shallow-backup.

	Written by Aaron Lichtman (@alichtman).
	"""

	# Process CLI args
	admin_action = any([v, delete_config, destroy_backup, show, rm]) or None not in add
	has_cli_arg = any([old_path, all, dotfiles, packages, fonts, configs,
	                   reinstall_dots, reinstall_fonts, reinstall_all,
	                   reinstall_configs, reinstall_packages])
	skip_prompt = any([all, dotfiles, configs, packages, fonts, reinstall_packages, reinstall_configs, reinstall_dots,
	                   reinstall_fonts])

	# Perform administrative action and exit.
	if admin_action:
		if v:
			print_version_info()
		elif delete_config:
			# TODO: Error checking.
			os.remove(get_config_path())
			print_red_bold("Removed config file...")
		elif destroy_backup:
			backup_home_path = expand_path_to_absolute(get_config()["backup_path"])
			destroy_backup_dir(backup_home_path)
		elif None not in add:
			add_to_config(add[0], add[1])
		elif rm:
			rm_from_config(rm)
		elif show:
			show_config()
		sys.exit()

	# Start CLI
	splash_screen()
	safe_create_config()
	backup_config = get_config()

	# User entered a new path, so update the config
	if new_path:
		abs_path = os.path.abspath(new_path)
		print(Fore.BLUE + Style.NORMAL + "\nUpdating shallow-backup path to -> " + Style.BRIGHT + "{}".format(
			abs_path) + Style.RESET_ALL)
		backup_config["backup_path"] = abs_path
		write_config(backup_config)

	# User didn't enter any CLI args so prompt for path update before showing menu
	elif not has_cli_arg:
		prompt_for_path_update(backup_config)

	# Create backup directory and do git setup
	backup_home_path = expand_path_to_absolute(get_config()["backup_path"])
	mkdir_warn_overwrite(backup_home_path)
	repo, new_git_repo_created = safe_git_init(backup_home_path)

	# Create default gitignore if we just ran git init
	if new_git_repo_created:
		safe_create_gitignore(backup_home_path)
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
	if skip_prompt:
		if reinstall_packages:
			reinstall_packages_sb(packages_path)
		elif reinstall_configs:
			reinstall_configs_sb(configs_path)
		elif reinstall_fonts:
			reinstall_fonts_sb(fonts_path)
		elif reinstall_dots:
			reinstall_dots_sb(dotfiles_path)
		elif reinstall_all:
			reinstall_all_sb(dotfiles_path, packages_path, fonts_path, configs_path)
		elif all:
			backup_all(dotfiles_path, packages_path, fonts_path, configs_path, skip=True)
			git_add_all_commit_push(repo, "all")
		elif dotfiles:
			backup_dotfiles(dotfiles_path, skip=True)
			git_add_all_commit_push(repo, "dotfiles")
		elif configs:
			backup_configs(configs_path, skip=True)
			git_add_all_commit_push(repo, "configs")
		elif packages:
			backup_packages(packages_path, skip=True)
			git_add_all_commit_push(repo, "packages")
		elif fonts:
			backup_fonts(fonts_path, skip=True)
			git_add_all_commit_push(repo, "fonts")
	# No CL options, show action menu and process selected option.
	else:
		selection = actions_menu_prompt().lower().strip()
		selection_words = selection.split()
		if selection.startswith("back up"):
			if selection_words[-1] == "all":
				backup_all(dotfiles_path, packages_path, fonts_path, configs_path)
				git_add_all_commit_push(repo, selection_words[-1])
			elif selection_words[-1] == "dotfiles":
				backup_dotfiles(dotfiles_path)
				git_add_all_commit_push(repo, selection_words[-1])
			elif selection_words[-1] == "configs":
				backup_configs(configs_path)
				git_add_all_commit_push(repo, selection_words[-1])
			elif selection_words[-1] == "packages":
				backup_packages(packages_path)
				git_add_all_commit_push(repo, selection_words[-1])
			elif selection_words[-1] == "fonts":
				backup_fonts(fonts_path)
				git_add_all_commit_push(repo, selection_words[-1])
		elif selection.startswith("reinstall"):
			if selection_words[-1] == "packages":
				reinstall_packages_sb(packages_path)
			elif selection_words[-1] == "configs":
				reinstall_configs_sb(configs_path)
			elif selection_words[-1] == "fonts":
				reinstall_fonts_sb(fonts_path)
			elif selection_words[-1] == "dotfiles":
				reinstall_dots_sb(dotfiles_path)
			elif selection_words[-1] == "all":
				reinstall_all_sb(dotfiles_path, packages_path, fonts_path, configs_path)
		else:
			if selection == "show config":
				show_config()
			elif selection == "destroy backup":
				if prompt_yes_no("Erase backup directory: {}?".format(backup_home_path), Fore.RED):
					destroy_backup_dir(backup_home_path)
				else:
					print_red_bold("Exiting to prevent accidental deletion of backup directory.")

	sys.exit()


if __name__ == "__main__":
	"""
	I'm just here so I don't get fined.
	"""
	cli()
