import os
import git
import sys
import json
import click
import inquirer
import shutil
import subprocess as sp
import multiprocessing as mp
from os.path import expanduser
from colorama import Fore, Style
from pprint import pprint
from constants import Constants


def print_version_info():
	version = "{} v{} by {} -> (Github: {})".format(Constants.PROJECT_NAME,
	                                                Constants.VERSION,
	                                                Constants.AUTHOR_FULL_NAME,
	                                                Constants.AUTHOR_GITHUB)
	line = "-" * (len(version))
	print(Fore.RED + Style.BRIGHT + line)
	print(version)
	print(line + "\n" + Style.RESET_ALL)


def splash_screen():
	"""
	Display splash graphic, and then version info
	"""
	print(Fore.YELLOW + Style.BRIGHT + "\n" +
		  "            dP                dP dP                        dP                         dP                         \n" +
		  "            88                88 88                        88                         88                         \n" +
		  "   ,d8888'  88d888b. .d8888b. 88 88 .d8888b. dP  dP  dP    88d888b. .d8888b. .d8888b. 88  .dP  dP    dP 88d888b. \n" +
		  "   Y8ooooo, 88'  `88 88'  `88 88 88 88'  `88 88  88  88    88'  `88 88'  `88 88'  `\"\" 88888\"   88    88 88'  `88 \n" +
		  "         88 88    88 88.  .88 88 88 88.  .88 88.88b.88'    88.  .88 88.  .88 88.  ... 88  `8b. 88.  .88 88.  .88 \n" +
		  "   `88888P' dP    dP `88888P8 dP dP `88888P' 8888P Y8P     88Y8888' `88888P8 `88888P' dP   `YP `88888P' 88Y888P' \n" +
		  "                                                                                                        88		\n" +
		  "                                                                                                        dP		\n" + Style.RESET_ALL)

	print_version_info()


def prompt_yes_no(message, color):
	"""
	Print question and return True or False depending on user selection from list.
	bottom_line should be used for one liners.
	Otherwise, it's the second line you want printed.
	"""
	questions = [inquirer.List('choice',
							   message=color + Style.BRIGHT + message + Fore.BLUE,
							   choices=[' Yes', ' No'],
							   ),
				 ]

	answers = inquirer.prompt(questions)
	return answers.get('choice').strip().lower() == 'yes'


def print_section_header(title, COLOR):
	"""
	Prints variable sized section header
	"""
	block = "#" * (len(title) + 2)
	print("\n" + COLOR + Style.BRIGHT + block)
	print("#", title)
	print(block + "\n" + Style.RESET_ALL)


def get_subfiles(directory):
	"""
	Returns list of immediate subfiles
	"""
	file_paths = []
	for path, subdirs, files in os.walk(directory):
		for name in files:
			file_paths.append(os.path.join(path, name))
	return file_paths


def make_dir_warn_overwrite(path):
	"""
	Make destination dir if path doesn't exist, confirm before overwriting if it does.
	"""
	subdirs = ["dotfiles", "packages", "fonts", "configs"]
	if os.path.exists(path) and path.split("/")[-1] in subdirs:
		print(Fore.RED + Style.BRIGHT +
		      "Directory {} already exists".format(path) + "\n" + Style.RESET_ALL)
		if prompt_yes_no("Erase directory and make new back up?", Fore.RED):
			shutil.rmtree(path)
			os.makedirs(path)
		else:
			print(Fore.RED + "Exiting to prevent accidental deletion of user data." + Style.RESET_ALL)
			sys.exit()
	elif not os.path.exists(path):
		os.makedirs(path)
		print(Fore.RED + Style.BRIGHT + "CREATED DIR: " + Style.NORMAL + path + Style.RESET_ALL)


def backup_prompt():
	"""
	Use pick library to prompt user with choice of what to backup.
	"""
	questions = [inquirer.List('choice',
	                           message=Fore.GREEN + Style.BRIGHT + "What would you like to do?" + Fore.BLUE,
	                           choices=[' Back up dotfiles',
                                      ' Back up configs',
	                                    ' Back up packages', 
                                      ' Back up fonts',
	                                    ' Back up everything',
	                                    ' Reinstall packages', 
                                      ' Reinstall configs'],
	                           ),
	             ]

	answers = inquirer.prompt(questions)
	return answers.get('choice').strip().lower()


def copy_dir(source_dir, backup_path):
	"""
	Copy dotfolder from $HOME.
	"""
	invalid = {".Trash", ".npm", ".cache", ".rvm"}
	if len(invalid.intersection(set(source_dir.split("/")))) != 0:
		return

	if "Application\ Support" not in source_dir:
		command = "cp -aRp '" + source_dir + "' '" + backup_path + "/" + source_dir.split("/")[-2] + "'"
	elif "Sublime" in source_dir:
		command = "cp -aRp '" + source_dir + "' '" + backup_path + "/" + source_dir.split("/")[-3] + "'"
	else:
		command = "cp -a '" + source_dir + "' '" + backup_path + "/'"

	sp.run(command, shell=True, stdout=sp.PIPE)


def _copy_file(source, target):
	"""
	Copy dotfile from $HOME.
	"""
	command = "cp -a '" + source + "' '" + target + "'"
	# print(command)
	sp.run(command, shell=True, stdout=sp.PIPE)


def _mkdir_or_pass(dir):
	if not os.path.isdir(dir):
		os.makedirs(dir)
	pass


def _home_prefix(path):
	return os.path.join(os.path.expanduser('~'), path)


def backup_dotfiles(backup_path):
	"""
	Create `dotfiles` dir and makes copies of dotfiles and dotfolders.
	"""

	print_section_header("DOTFILES", Fore.BLUE)
	make_dir_warn_overwrite(backup_path)

	# assumes dotfiles are stored in home directory
	home_path = os.path.expanduser('~')

	# get dotfolders and dotfiles
	config = get_config()
	dotfiles_for_backup = config["dotfiles"]
	dotfolders_for_backup = config["dotfolders"]

	# Add dotfile/folder for backup if it exists on the machine
	dotfiles = [file for file in dotfiles_for_backup if os.path.isfile(
		os.path.join(home_path, file))]
	dotfolders = [folder for folder in dotfolders_for_backup if os.path.exists(
		os.path.join(home_path, folder))]

	# dotfiles/dotfolders multiprocessing in list format: [(full_dotfile_path, full_dest_path), ...]

	dotfolders_mp_in = []
	for dotfolder in dotfolders:
		dotfolders_mp_in.append(
			(os.path.join(home_path, dotfolder), backup_path))

	dotfiles_mp_in = []
	for dotfile in dotfiles:
		dotfiles_mp_in.append((os.path.join(home_path, dotfile), backup_path))

	####
	# Back up System and Application Preferences and Settings
	####

	# Sublime Text Configs
	if os.path.isdir(_home_prefix("Library/Application Support/Sublime Text 2")):
		dotfolders_mp_in.append((_home_prefix("Library/Application Support/Sublime Text 2/Packages/User"), backup_path))

	if os.path.isdir(_home_prefix("Library/Application Support/Sublime Text 3")):
		dotfolders_mp_in.append((_home_prefix("Library/Application Support/Sublime Text 3/Packages/User"), backup_path))

	# pprint(dotfiles_mp_in)
	# pprint(dotfolders_mp_in)

	# Multiprocessing
	with mp.Pool(mp.cpu_count()):

		print(Fore.BLUE + Style.BRIGHT +
			  "Backing up dotfolders..." + Style.RESET_ALL)

		for x in dotfolders_mp_in:
			x = list(x)
			mp.Process(target=copy_dir, args=(x[0], x[1],)).start()

	with mp.Pool(mp.cpu_count()):
		print(Fore.BLUE + Style.BRIGHT +
			  "Backing up dotfiles..." + Style.RESET_ALL)
		for x in dotfiles_mp_in:
			x = list(x)
			mp.Process(target=_copy_file, args=(x[0], x[1],)).start()


def backup_configs(backup_path):
	make_dir_warn_overwrite(backup_path)

	configs_dir_mapping = {"Library/Application Support/Sublime Text 2/Packages/User/": "sublime_2",
						   "Library/Application Support/Sublime Text 3/Packages/User/": "sublime_3",
						   "Library/Preferences/IntelliJIdea2018.2/":"intellijidea_2018-2",
						   "Library/Preferences/PyCharm2018.2/":"pycharm_2018-2",
						   "Library/Preferences/CLion2018.2/":"clion_2018-2",
						   "Library/Preferences/PhpStorm2018.2":"phpstorm_2018-2",}
	plist_files = ["Library/Preferences/com.apple.Terminal.plist"]

	# backup config dirs in backup_path/configs/<target>/
	for config, target in configs_dir_mapping.items():
		if os.path.isdir(_home_prefix(config)):
			configs_backup_path = os.path.join(backup_path, target)
			_mkdir_or_pass(configs_backup_path)
			_copy_dir_content(_home_prefix(config), configs_backup_path)

	# backup plist files in backup_path/configs/plist/
	plist_backup_path = os.path.join(backup_path, "plist")
	_mkdir_or_pass(plist_backup_path)
	for plist in plist_files:
		if os.path.exists(_home_prefix(plist)):
			_copy_dir_content(_home_prefix(plist), plist_backup_path)


def _copy_dir_content(source, target):
	"""Copies the contents of a dir to a specified target path."""
	cmd = "cp -a '" + source + "' '" + target + "/'"
	# print(cmd)
	sp.run(cmd, shell=True, stdout=sp.PIPE)


def backup_packages(backup_path):
	"""Creates `packages` directory and places install list text files there."""

	print_section_header("PACKAGES", Fore.BLUE)

	make_dir_warn_overwrite(backup_path)

	std_backup_package_managers = [
		"brew",
		"brew cask",
		"gem"
	]

	for mgr in std_backup_package_managers:
		# deal with package managers that have spaces in them.
		print(Fore.BLUE + "Backing up {} package list...".format(mgr) + Style.RESET_ALL)
		command = "{0} list > {1}/{2}_list.txt".format(mgr,
		                                               backup_path, mgr.replace(" ", "-"), True)
		sp.run(command, shell=True, stdout=sp.PIPE)

	# cargo
	print(Fore.BLUE + "Backing up cargo package list..." + Style.RESET_ALL)
	sp.run("ls {0}/.cargo/bin/ > {1}/cargo_list.txt".format(os.path.expanduser('~'),
	                                                        backup_path), shell=True, stdout=sp.PIPE)

	# pip
	print(Fore.BLUE + "Backing up pip package list..." + Style.RESET_ALL)
	sp.run("pip list --format=freeze > {}/pip_list.txt".format(backup_path), shell=True, stdout=sp.PIPE)

	# npm
	print(Fore.BLUE + "Backing up npm package list..." + Style.RESET_ALL)
	sp.run("npm ls --global --parseable=true --depth=0 > {}/npm_temp_list.txt".format(backup_path),
	       shell=True, stdout=sp.PIPE)
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
	os.remove("{}/npm_temp_list.txt".format(backup_path))

	# atom package manager
	print(Fore.BLUE + "Backing up Atom package list..." + Style.RESET_ALL)
	sp.run("apm list --installed --bare > {}/apm_list.txt".format(backup_path), shell=True, stdout=sp.PIPE)

	# sublime text packages
	if os.path.isdir(_home_prefix("Library/Application Support/Sublime Text 2")):
		print(Fore.BLUE + "Backing up Sublime Text package list..." + Style.RESET_ALL)
		source_path = _home_prefix("Library/Application Support/Sublime Text 2/Packages/")
		sp.run("ls {} > {}/sublime2_list.txt".format(source_path, backup_path), shell=True, stdout=sp.PIPE)

	if os.path.isdir(_home_prefix("Library/Application Support/Sublime Text 3")):
		print(Fore.BLUE + "Backing up Sublime Text package list..." + Style.RESET_ALL)
		source_path = _home_prefix("Library/Application Support/Sublime Text 3/Installed Packages/")
		sp.run("ls {} > {}/sublime3_list.txt".format(source_path, backup_path), shell=True, stdout=sp.PIPE)

	# macports
	print(Fore.BLUE + "Backing up macports package list..." + Style.RESET_ALL)
	sp.run("port installed requested > {}/macports_list.txt".format(backup_path),
	       shell=True, stdout=sp.PIPE)

	# system installs
	print(Fore.BLUE + "Backing up system application list..." + Style.RESET_ALL)
	sp.run("ls /Applications/ > {}/installed_apps_list.txt".format(backup_path), shell=True, stdout=sp.PIPE)

	# Clean up empty package list files
	print(Fore.BLUE + "Cleaning up empty package lists..." + Style.RESET_ALL)
	for file in get_subfiles(backup_path):
		if os.path.getsize(file) == 0:
			os.remove(file)


def backup_fonts(path):
	"""
	Creates list of all .ttf and .otf files in ~/Library/Fonts
	"""

	print_section_header("FONTS", Fore.BLUE)
	make_dir_warn_overwrite(path)

	# Copy fonts
	print(Fore.BLUE + "Copying '.otf' and '.ttf' fonts..." + Style.RESET_ALL)
	copy_ttf = "cp ~/Library/Fonts/*.ttf {}/".format(path)
	copy_otf = "cp ~/Library/Fonts/*.otf {}/".format(path)

	print(copy_otf)
	print(copy_ttf, "\n")

	sp.run(copy_otf, shell=True, stdout=sp.PIPE)
	sp.run(copy_ttf, shell=True, stdout=sp.PIPE)


def backup_all(dotfiles_path, packages_path, fonts_path, configs_path):
	"""
	Complete backup procedure.
	"""
	backup_dotfiles(dotfiles_path)
	backup_packages(packages_path)
	backup_fonts(fonts_path)
	backup_configs(configs_path)


def reinstall_config_files(configs_path):
	"""
	Reinstall all configs from the backup.
	"""

	def backup_prefix(path):
		return os.path.join(configs_path, path)

	configs_dir_mapping = {"Library/Application Support/Sublime Text 2/Packages/User/": "sublime_2",
						   "Library/Application Support/Sublime Text 3/Packages/User/": "sublime_3",
						   "Library/Preferences/IntelliJIdea2018.2/":"intellijidea_2018-2",
						   "Library/Preferences/PyCharm2018.2/":"pycharm_2018-2",
						   "Library/Preferences/CLion2018.2/":"clion_2018-2",
						   "Library/Preferences/PhpStorm2018.2":"phpstorm_2018-2", }
	plist_files = {"Library/Preferences/com.apple.Terminal.plist": "plist/com.apple.Terminal.plist"}

	for target, backup in configs_dir_mapping.items():
		if os.path.isdir(backup_prefix(backup)):
			_copy_dir_content(backup_prefix(backup), _home_prefix(target))

	for target, backup in plist_files.items():
		if os.path.exists(backup_prefix(backup)):
			_copy_file(backup_prefix(backup), _home_prefix(target))


def reinstall_package(packages_path):
	"""
	Reinstall all packages from the files in backup/installs.
	"""

	# Figure out which install lists they have saved
	package_mgrs = set()
	for file in get_subfiles(packages_path):
		# print(file)
		manager = file.split("_")[0].replace("-", " ")
		if manager != "installed":
			package_mgrs.add(file.split("_")[0])

	print(Fore.BLUE + "Package Managers detected:" + Style.RESET_ALL)
	pprint(package_mgrs)

	# construct commands
	for pm in package_mgrs:
		if pm in ["brew", "brew-cask"]:
			cmd = "xargs {0} install < {1}/{2}_list.txt".format(
				pm.replace("-", " "), packages_path, pm)
			print(cmd)
			sp.run(cmd, shell=True, stdout=sp.PIPE)
		elif pm == "npm":
			cmd = "cat {0}/npm_list.txt | xargs npm install -g".format(
				packages_path)
			print(cmd)
			sp.run(cmd, shell=True, stdout=sp.PIPE)
		elif pm == "pip":
			cmd = "pip install -r {0}/pip_list.txt".format(packages_path)
			print(cmd)
			sp.run(cmd, shell=True, stdout=sp.PIPE)
		elif pm == "apm":
			cmd = "apm install --packages-file {0}/apm_list.txt".format(
				packages_path)
			print(cmd)
			sp.run(cmd, shell=True, stdout=sp.PIPE)
		elif pm == "macports":
			print(
				Fore.RED + "WARNING: Macports reinstallation is not supported." + Style.RESET_ALL)
		elif pm == "gem":
			print(
				Fore.RED + "WARNING: Gem reinstallation is not supported." + Style.RESET_ALL)
		elif pm == "cargo":
			print(Fore.RED + "WARNING: Cargo reinstallation is not possible at the moment. "
			                 "\n -> https://github.com/rust-lang/cargo/issues/5593" + Style.RESET_ALL)
	sys.exit()


#####
# Git
#####

def git_set_remote(repo, remote_url):
	"""
	Sets git repo upstream URL.
	TODO: Must fast-forward history as well
	"""
	try:
		origin = repo.create_remote('origin', remote_url)
		# origin.fetch()
		# origin.heads.master.set_tracking_branch(origin.refs.master)
		# origin.heads.master.checkout()
	except:
		pass


def create_gitignore(dir_path):
	"""
	Creates a .gitignore file that ignores all files listed in config.
	"""
	files_to_ignore = get_config()["gitignore"]
	with open(os.path.join(dir_path, ".gitignore"), "w+") as f:
		for ignore in files_to_ignore:
			f.write("{}\n".format(ignore))


def git_init_if_needed(dir_path):
	"""
	If there is no git repo inside the dir_path, intialize one.
	Returns a Repo object
	"""
	if not os.path.isdir(os.path.join(dir_path, ".git")):
		repo = git.Repo.init(dir_path)
		return repo
	else:
		repo = git.Repo(dir_path)
		return repo


def git_add_all_commit(repo, dir_path):
	"""
	Stages all changed files in dir_path and its children folders for commit,
	commits them and pushes to a remote if it's configured.
	"""
	dotfiles_path = os.path.join(dir_path, "dotfiles")
	fonts_path = os.path.join(dir_path, "fonts")
	packages_path = os.path.join(dir_path, "packages")
	configs_path = os.path.join(dir_path, "configs")
	gitignore_path = os.path.join(dir_path, ".gitignore")
	repo.index.add([gitignore_path])
	if os.path.exists(dotfiles_path):
		repo.index.add([dotfiles_path])
	if os.path.exists(fonts_path):
		repo.index.add([fonts_path])
	if os.path.exists(packages_path):
		repo.index.add([packages_path])
	if os.path.exists(configs_path):
		repo.index.add([configs_path])
	repo.index.commit("shallow-backup update.")


def git_push_origin(repo):
	"""
	Push commits to remote if remote is configured.
	"""
	# TODO: Fix this method to allow for remotes to be named something other than origin.
	if "origin" in [remote.name for remote in repo.remotes]:
		print(Fore.RED + Style.BRIGHT + "Pushing to remote git repo..." + Style.RESET_ALL)
		repo.remotes.origin.push(refspec='master:master')


######
# Config
######


def get_config_path():
	return _home_prefix(Constants.CONFIG_PATH)


def get_config():
	"""
	Returns the config.
	:return: dictionary for config
	"""
	with open(get_config_path()) as f:
		config = json.load(f)
	return config


def write_config(config):
	"""
	Write to config file
	"""
	with open(get_config_path(), 'w') as f:
		json.dump(config, f, indent=4)


def get_default_config():
	"""
	Returns a default configuration.
	"""
	return {
		"backup_path": "DEFAULT",
		"dotfiles"   : [
			".bashrc",
			".bash_profile",
			".gitconfig",
			".profile",
			".pypirc",
			".shallow-backup",
			".vimrc",
			".zshrc"
		],
		"dotfolders" : [
			".ssh/",
			".vim/"
		],
		"gitignore"  : [
			"dotfiles/.ssh",
			"packages/",
			"dotfiles/.pypirc",
		]
	}


#######
# CLI
#######


def prompt_for_path_update(config):
	"""
	Ask user if they'd like to update the backup path or not.
	If yes, update. If no... don't.
	"""
	print(
		Fore.BLUE + Style.BRIGHT + "Current shallow-backup path -> " + Style.NORMAL + "{}".format(
			config["backup_path"]) + Style.RESET_ALL)

	if prompt_yes_no("Would you like to update this?", Fore.GREEN):
		print(Fore.GREEN + Style.BRIGHT +
		      "Enter relative path:" + Style.RESET_ALL)

		abs_path = os.path.abspath(input())

		print(Fore.BLUE + "\nUpdating shallow-backup path to {}".format(
			abs_path) + Style.RESET_ALL)
		config["backup_path"] = abs_path
		write_config(config)


# custom help options
@click.command(context_settings=dict(help_option_names=['-h', '-help', '--help']))
@click.option('-complete', is_flag=True, default=False, help="Back up everything.")
@click.option('-dotfiles', is_flag=True, default=False, help="Back up dotfiles.")
@click.option('-configs', is_flag=True, default=False, help="Back up app config files.")
@click.option('-fonts', is_flag=True, default=False, help="Back up installed fonts.")
@click.option('-packages', is_flag=True, default=False, help="Back up package libraries and installed applications.")
@click.option('-old_path', is_flag=True, default=False, help="Skip setting new back up directory path.")
@click.option('--new_path', default="DEFAULT", help="Input a new back up directory path.")
@click.option('--remote', default="", help="Input a URL for a git repository.")
@click.option('-reinstall_packages', is_flag=True, default=False, help="Reinstall packages from package lists.")
@click.option('-reinstall_configs', is_flag=True, default=False, help="Reinstall configs from configs backup.")
@click.option('-delete_config', is_flag=True, default=False, help="Remove config file.")
@click.option('-v', is_flag=True, default=False, help='Display version and author information and exit.')
def cli(complete, dotfiles, configs, packages, fonts, old_path, new_path, remote, reinstall_packages, reinstall_configs,
		delete_config, v):
	"""
	Easily back up installed packages, dotfiles, and more. You can edit which dotfiles are backed up in ~/.shallow-backup.
	"""

	backup_config_path = get_config_path()

	# Print version information
	if v:
		print_version_info()
		sys.exit()

	elif delete_config:
		os.remove(backup_config_path)
		print(Fore.RED + Style.BRIGHT +
		      "Removed config file..." + Style.RESET_ALL)
		sys.exit()

	splash_screen()

	# If config file doesn't exist, create it.
	if not os.path.exists(backup_config_path):
		print(Fore.BLUE + Style.BRIGHT + "Creating config file at {}".format(backup_config_path))
		backup_config = get_default_config()
		write_config(backup_config)
    
	#####
	# Update backup path from CLI args, prompt user, or skip updating
	#####

	backup_config = get_config()

	# User entered a new path, so update the config
	if new_path != "":
		abs_path = os.path.abspath(new_path)

		print(Fore.BLUE + Style.NORMAL + "\nUpdating shallow-backup path to -> " + Style.BRIGHT + "{}".format(
			abs_path) + Style.RESET_ALL)
		backup_config["backup_path"] = abs_path
		write_config(backup_config)

	# User didn't enter the same_path flag but entered a backup option, so no path update prompt
	elif old_path or complete or dotfiles or packages or fonts:
		pass
	# User didn't enter a new path, didn't use the same_path flag or any backup options, so prompt
	else:
		prompt_for_path_update(backup_config)

	###
	# Create backup directory and set up git stuff
	###

	backup_home_path = get_config()["backup_path"]
	make_dir_warn_overwrite(backup_home_path)
	repo = git_init_if_needed(backup_home_path)
	create_gitignore(backup_home_path)
	if remote != "":
		git_set_remote(repo, remote)

	dotfiles_path = os.path.join(backup_home_path, "dotfiles")
	configs_path = os.path.join(backup_home_path, "configs")
	packages_path = os.path.join(backup_home_path, "packages")
	fonts_path = os.path.join(backup_home_path, "fonts")

	# Command line options
	if complete or dotfiles or configs or packages or fonts or reinstall_packages or reinstall_configs:
		if reinstall_packages:
			reinstall_package(packages_path)
		elif reinstall_configs:
			reinstall_config_files(configs_path)
		elif complete:
			backup_all(dotfiles_path, packages_path, fonts_path, configs_path)
		elif dotfiles:
			backup_dotfiles(dotfiles_path)
		elif configs:
			backup_configs(configs_path)
		elif packages:
			backup_packages(packages_path)
		elif fonts:
			backup_fonts(fonts_path)

		git_add_all_commit(repo, backup_home_path)
		git_push_origin(repo)
		sys.exit()

	# No CL options, prompt for selection
	else:
		selection = backup_prompt().lower().strip()
		if selection == "back up everything":
			backup_all(dotfiles_path, packages_path, fonts_path, configs_path)
		elif selection == "back up dotfiles":
			backup_dotfiles(dotfiles_path)
		elif selection == "back up configs":
			backup_configs(configs_path)
		elif selection == "back up packages":
			backup_packages(packages_path)
		elif selection == "back up fonts":
			backup_fonts(fonts_path)
		elif selection == "reinstall packages":
			reinstall_package(packages_path)
		elif selection == "reinstall configs":
			reinstall_config_files(configs_path)

		git_add_all_commit(repo, backup_home_path)
		git_push_origin(repo)
		sys.exit()


if __name__ == '__main__':
	"""
	I'm just here so I don't get fined.
	"""
	cli()
