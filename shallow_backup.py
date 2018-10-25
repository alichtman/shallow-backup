import os
import git
import sys
import json
import click
import inquirer
import subprocess as sp
import multiprocessing as mp
from constants import Constants
from shutil import copyfile, copytree, rmtree, move
from stylize import RED, BRIGHT, RESET, YELLOW, BLUE, NORMAL, GREEN

########
# Globals
########

COMMIT_MSG = {
	"fonts"   : "Back up fonts.",
	"packages": "Back up packages.",
	"configs" : "Back up configs.",
	"complete": "Back up everything.",
	"dotfiles": "Back up dotfiles.,"
}

#########
# Display
#########

def print_version_info(cli=True):
	"""
	Formats version differently for CLI and splash screen.
	"""
	version = "v{} by {} (@{})".format(Constants.VERSION,
	                                   Constants.AUTHOR_FULL_NAME,
	                                   Constants.AUTHOR_GITHUB)
	if not cli:
		print(RED + BRIGHT + "\t{}\n".format(version) + RESET)
	else:
		print(version)


def splash_screen():
	"""
	Display splash graphic, and then stylized version
	"""
	print(YELLOW + BRIGHT + "\n" + Constants.LOGO + RESET)
	print_version_info(False)


def print_section_header(title, COLOR):
	"""
	Prints variable sized section header
	"""
	block = "#" * (len(title) + 2)
	print("\n" + COLOR + BRIGHT + block)
	print("#", title)
	print(block + "\n" + RESET)


def print_pkg_mgr_backup(mgr):
	print("{}Backing up {}{}{}{}{} packages list...{}".format(BLUE, BRIGHT, YELLOW, mgr, BLUE, NORMAL, RESET))


# TODO: Integrate this in the reinstallation section
def print_pkg_mgr_reinstall(mgr):
	print("{}Reinstalling {}{}{}{}{} packages...{}".format(BLUE, BRIGHT, YELLOW, mgr, BLUE, NORMAL, RESET))


def prompt_yes_no(message, color):
	"""
	Print question and return True or False depending on user selection from list.
	"""
	questions = [inquirer.List('choice',
	                           message=color + BRIGHT + message + BLUE,
	                           choices=[' Yes', ' No'],
	                           )
	             ]

	answers = inquirer.prompt(questions)
	return answers.get('choice').strip().lower() == 'yes'


###########
# Utilities
###########


def run_shell_cmd(command):
	"""
	Wrapper on subprocess.run that handles both lists and strings as commands.
	"""
	try:
		if not isinstance(command, list):
			process = sp.run(command.split(), stdout=sp.PIPE)
			return process
		else:
			process = sp.run(command, stdout=sp.PIPE)
			return process
	except FileNotFoundError:  # If package manager is missing
		return None


def run_shell_cmd_write_stdout_to_file(command, filepath):
	"""
	Runs a command and then writes its stdout to a file
	:param: command String representing command to run and write output of to file
	"""
	process = run_shell_cmd(command)
	if process:
		with open(filepath, "w+") as f:
			f.write(process.stdout.decode('utf-8'))


def make_dir_warn_overwrite(path):
	"""
	Make destination dir if path doesn't exist, confirm before overwriting if it does.
	"""
	subdirs = ["dotfiles", "packages", "fonts", "configs"]
	if os.path.exists(path) and path.split("/")[-1] in subdirs:
		print(RED + BRIGHT +
		      "Directory {} already exists".format(path) + "\n" + RESET)
		if prompt_yes_no("Erase directory and make new back up?", RED):
			rmtree(path)
			os.makedirs(path)
		else:
			print(RED + "Exiting to prevent accidental deletion of user data." + RESET)
			sys.exit()
	elif not os.path.exists(path):
		os.makedirs(path)
		print(RED + BRIGHT + "CREATED DIR: " + NORMAL + path + RESET)


def get_subfiles(directory):
	"""
	Returns list of absolute paths of immediate subfiles of a directory
	"""
	file_paths = []
	for path, subdirs, files in os.walk(directory):
		for name in files:
			file_paths.append(os.path.join(path, name))
	return file_paths


def _copy_dir(source_dir, backup_path):
	"""
	Copy dotfolder from $HOME.
	"""
	invalid = set(Constants.INVALID_DIRS)
	if len(invalid.intersection(set(source_dir.split("/")))) != 0:
		return

	if "Application Support" not in source_dir:
		copytree(source_dir, os.path.join(backup_path, source_dir.split("/")[-2]), symlinks=True)
	elif "Sublime" in source_dir:
		copytree(source_dir, os.path.join(backup_path, source_dir.split("/")[-3]), symlinks=True)
	else:
		copytree(source_dir, backup_path, symlinks=True)


def _mkdir_or_pass(dir):
	if not os.path.isdir(dir):
		os.makedirs(dir)
	pass


def _home_prefix(path):
	return os.path.join(os.path.expanduser('~'), path)


################
# BACKUP METHODS
################

def get_configs_path_mapping():
	"""
	Gets a dictionary mapping directories to back up to their destination path.
	"""
	return {
		"Library/Application Support/Sublime Text 2/Packages/User/": "sublime_2",
		"Library/Application Support/Sublime Text 3/Packages/User/": "sublime_3",
		"Library/Preferences/IntelliJIdea2018.2/"                  : "intellijidea_2018.2",
		"Library/Preferences/PyCharm2018.2/"                       : "pycharm_2018.2",
		"Library/Preferences/CLion2018.2/"                         : "clion_2018.2",
		"Library/Preferences/PhpStorm2018.2"                       : "phpstorm_2018.2",
		".atom/"                                                   : "atom",
	}


def get_plist_mapping():
	"""
	Gets a dictionary mapping plist files to back up to their destination path.
	"""
	return {
		"Library/Preferences/com.apple.Terminal.plist": "plist/com.apple.Terminal.plist",
	}


def backup_dotfiles(backup_path):
	"""
	Create `dotfiles` dir and makes copies of dotfiles and dotfolders.
	"""
	print_section_header("DOTFILES", BLUE)
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

	# dotfiles/folders multiprocessing format: [(full_dotfile_path, full_dest_path), ...]
	dotfolders_mp_in = []
	for dotfolder in dotfolders:
		dotfolders_mp_in.append(
			(os.path.join(home_path, dotfolder), backup_path))

	dotfiles_mp_in = []
	for dotfile in dotfiles:
		dotfiles_mp_in.append((os.path.join(home_path, dotfile), os.path.join(backup_path, dotfile)))

	# Multiprocessing
	with mp.Pool(mp.cpu_count()):
		print(BLUE + BRIGHT + "Backing up dotfolders..." + RESET)
		for x in dotfolders_mp_in:
			x = list(x)
			mp.Process(target=_copy_dir, args=(x[0], x[1],)).start()

	with mp.Pool(mp.cpu_count()):
		print(BLUE + BRIGHT + "Backing up dotfiles..." + RESET)
		for x in dotfiles_mp_in:
			x = list(x)
			mp.Process(target=copyfile, args=(x[0], x[1],)).start()


def backup_configs(backup_path):
	"""
	Creates `configs` directory and places config backups there.
	Configs are application settings, generally. .plist files count.
	"""
	print_section_header("CONFIGS", BLUE)
	make_dir_warn_overwrite(backup_path)

	configs_dir_mapping = get_configs_path_mapping()
	plist_files = get_plist_mapping()

	print(BLUE + BRIGHT + "Backing up configs..." + RESET)

	# backup config dirs in backup_path/<target>/
	for config, target in configs_dir_mapping.items():
		src_dir = _home_prefix(config)
		configs_backup_path = os.path.join(backup_path, target)
		if os.path.isdir(src_dir):
			# TODO: Exclude Sublime/Atom/VS Code Packages here to speed things up
			copytree(src_dir, configs_backup_path, symlinks=True)

	# backup plist files in backup_path/configs/plist/
	print(BLUE + BRIGHT + "Backing up plist files..." + RESET)
	plist_backup_path = os.path.join(backup_path, "plist")
	_mkdir_or_pass(plist_backup_path)
	for plist, dest in plist_files.items():
		plist_path = _home_prefix(plist)
		if os.path.exists(plist_path):
			copyfile(plist_path, os.path.join(backup_path, dest))


def backup_packages(backup_path):
	"""
	Creates `packages` directory and places install list text files there.
	"""
	print_section_header("PACKAGES", BLUE)
	make_dir_warn_overwrite(backup_path)

	std_package_managers = [
		"brew",
		"brew cask",
		"gem"
	]

	for mgr in std_package_managers:
		# deal with package managers that have spaces in them.
		print_pkg_mgr_backup(mgr)
		command = "{} list".format(mgr)
		dest = "{}/{}_list.txt".format(backup_path, mgr.replace(" ", "-"))
		run_shell_cmd_write_stdout_to_file(command, dest)

	# cargo
	print_pkg_mgr_backup("cargo")
	command = "ls {}".format(_home_prefix(".cargo/bin/"))
	dest = "{}/cargo_list.txt".format(backup_path)
	run_shell_cmd_write_stdout_to_file(command, dest)

	# pip
	print_pkg_mgr_backup("pip")
	command = "pip list --format=freeze".format(backup_path)
	dest = "{}/pip_list.txt".format(backup_path)
	run_shell_cmd_write_stdout_to_file(command, dest)

	# npm
	print_pkg_mgr_backup("npm")
	command = "npm ls --global --parseable=true --depth=0"
	temp_file_path = "{}/npm_temp_list.txt".format(backup_path)
	run_shell_cmd_write_stdout_to_file(command, temp_file_path)
	npm_dest_file = "{0}/npm_list.txt".format(backup_path)
	# Parse npm output
	with open(temp_file_path, mode="r+") as temp_file:
		# Skip first line of file
		temp_file.seek(1)
		with open(npm_dest_file, mode="w+") as dest:
			for line in temp_file:
				dest.write(line.split("/")[-1])

	os.remove(temp_file_path)

	# atom package manager
	print_pkg_mgr_backup("Atom")
	command = "apm list --installed --bare"
	dest = "{}/apm_list.txt".format(backup_path)
	run_shell_cmd_write_stdout_to_file(command, dest)

	# sublime text 2 packages
	sublime_2_path = _home_prefix("Library/Application Support/Sublime Text 2/Packages/")
	if os.path.isdir(sublime_2_path):
		print_pkg_mgr_backup("Sublime Text 2")
		command = ["ls", sublime_2_path]
		dest = "{}/sublime2_list.txt".format(backup_path)
		run_shell_cmd_write_stdout_to_file(command, dest)

	# sublime text 3 packages
	sublime_3_path = _home_prefix("Library/Application Support/Sublime Text 3/Installed Packages/")
	if os.path.isdir(sublime_3_path):
		print_pkg_mgr_backup("Sublime Text 3")
		command = ["ls", sublime_3_path]
		dest = "{}/sublime3_list.txt".format(backup_path)
		run_shell_cmd_write_stdout_to_file(command, dest)
	else:
		print(sublime_3_path, "IS NOT DIR")

	# macports
	print_pkg_mgr_backup("macports")
	command = "port installed requested"
	dest = "{}/macports_list.txt".format(backup_path)
	run_shell_cmd_write_stdout_to_file(command, dest)

	# system installs
	print_pkg_mgr_backup("macOS Applications")
	command = "ls /Applications/"
	dest = "{}/system_apps_list.txt".format(backup_path)
	run_shell_cmd_write_stdout_to_file(command, dest)

	# Clean up empty package list files
	print(BLUE + "Cleaning up empty package lists..." + RESET)
	for file in get_subfiles(backup_path):
		if os.path.getsize(file) == 0:
			os.remove(file)


def backup_fonts(path):
	"""
	Creates list of all .ttf and .otf files in ~/Library/Fonts/
	"""
	print_section_header("FONTS", BLUE)
	make_dir_warn_overwrite(path)
	print(BLUE + "Copying '.otf' and '.ttf' fonts..." + RESET)
	fonts_path = _home_prefix("Library/Fonts/")
	fonts = [os.path.join(fonts_path, font) for font in os.listdir(fonts_path) if
	         font.endswith(".otf") or font.endswith(".ttf")]

	for font in fonts:
		if os.path.exists(font):
			copyfile(font, os.path.join(path, font.split("/")[-1]))


def backup_all(dotfiles_path, packages_path, fonts_path, configs_path):
	"""
	Complete backup procedure.
	"""
	backup_dotfiles(dotfiles_path)
	backup_packages(packages_path)
	backup_fonts(fonts_path)
	backup_configs(configs_path)


################
# Reinstallation
################


def reinstall_config_files(configs_path):
	"""
	Reinstall all configs from the backup.
	"""
	print_section_header("REINSTALLING CONFIG FILES", BLUE)

	def backup_prefix(path):
		return os.path.join(configs_path, path)

	configs_dir_mapping = get_configs_path_mapping()
	plist_files = get_plist_mapping()

	for target, backup in configs_dir_mapping.items():
		if os.path.isdir(backup_prefix(backup)):
			copytree(backup_prefix(backup), _home_prefix(target))

	for target, backup in plist_files.items():
		if os.path.exists(backup_prefix(backup)):
			copyfile(backup_prefix(backup), _home_prefix(target))

	print_section_header("SUCCESSFUL CONFIG REINSTALLATION", BLUE)
	sys.exit()


def reinstall_packages_from_lists(packages_path):
	"""
	Reinstall all packages from the files in backup/installs.
	"""
	print_section_header("REINSTALLING PACKAGES", BLUE)

	# Figure out which install lists they have saved
	package_mgrs = set()
	for file in os.listdir(packages_path):
		# print(file)
		manager = file.split("_")[0].replace("-", " ")
		if manager in Constants.PACKAGE_MANAGERS:
			package_mgrs.add(file.split("_")[0])

	# TODO: USE print_pkg_mgr_reinstall()
	# TODO: Restylize this printing
	print(BLUE + BRIGHT + "Package Managers detected:" + RESET)
	for mgr in package_mgrs:
		print(BLUE + BRIGHT + "\t" + mgr)
	print(RESET)

	# TODO: Multithreading for reinstallation.
	# construct commands
	for pm in package_mgrs:
		if pm in ["brew", "brew-cask"]:
			pm_formatted = pm.replace("-", " ")
			print(BLUE + BRIGHT + "Reinstalling {} packages...".format(pm_formatted) + RESET)
			cmd = "xargs {0} install < {1}/{2}_list.txt".format(pm.replace("-", " "), packages_path, pm_formatted)
			run_shell_cmd(cmd)
		elif pm == "npm":
			print(BLUE + BRIGHT + "Reinstalling {} packages...".format(pm) + RESET)
			cmd = "cat {0}/npm_list.txt | xargs npm install -g".format(packages_path)
			run_shell_cmd(cmd)
		elif pm == "pip":
			print(BLUE + BRIGHT + "Reinstalling {} packages...".format(pm) + RESET)
			cmd = "pip install -r {0}/pip_list.txt".format(packages_path)
			run_shell_cmd(cmd)
		elif pm == "apm":
			print(BLUE + BRIGHT + "Reinstalling {} packages...".format(pm) + RESET)
			cmd = "apm install --packages-file {0}/apm_list.txt".format(packages_path)
			run_shell_cmd(cmd)
		elif pm == "macports":
			print(RED + "WARNING: Macports reinstallation is not supported." + RESET)
		elif pm == "gem":
			print(RED + "WARNING: Gem reinstallation is not supported." + RESET)
		elif pm == "cargo":
			print(RED + "WARNING: Cargo reinstallation is not possible at the moment."
			                 "\n -> https://github.com/rust-lang/cargo/issues/5593" + RESET)

	print_section_header("SUCCESSFUL PACKAGE REINSTALLATION", BLUE)
	sys.exit()


#####
# Git
#####


def git_set_remote(repo, remote_url):
	"""
	Sets git repo upstream URL and fast-forwards history.
	"""
	print(YELLOW + BRIGHT + "Setting remote URL to -> " + NORMAL + "{}...".format(
		remote_url) + RESET)

	try:
		origin = repo.create_remote('origin', remote_url)
		origin.fetch()
	except git.CommandError:
		print(YELLOW + BRIGHT + "Updating existing remote URL..." + RESET)
		repo.delete_remote(repo.remotes.origin)
		origin = repo.create_remote('origin', remote_url)
		origin.fetch()


def create_gitignore_if_needed(dir_path):
	"""
	Creates a .gitignore file that ignores all files listed in config.
	"""
	gitignore_path = os.path.join(dir_path, ".gitignore")
	if os.path.exists(gitignore_path):
		print(YELLOW + BRIGHT + ".gitignore detected." + RESET)
		pass
	else:
		print(YELLOW + BRIGHT + "Creating default .gitignore..." + RESET)
		files_to_ignore = get_config()["gitignore"]
		with open(gitignore_path, "w+") as f:
			for ignore in files_to_ignore:
				f.write("{}\n".format(ignore))


def git_init_if_needed(dir_path):
	"""
	If there is no git repo inside the dir_path, intialize one.
	Returns tuple of (git.Repo, bool new_git_repo_created)
	"""
	if not os.path.isdir(os.path.join(dir_path, ".git")):
		print(YELLOW + BRIGHT + "Initializing new git repo..." + RESET)
		repo = git.Repo.init(dir_path)
		return repo, True
	else:
		print(YELLOW + BRIGHT + "Detected git repo." + RESET)
		repo = git.Repo(dir_path)
		return repo, False


def git_add_all_commit_push(repo, message):
	"""
	Stages all changed files in dir_path and its children folders for commit,
	commits them and pushes to a remote if it's configured.
	"""
	if repo.index.diff(None) or repo.untracked_files:
		print(YELLOW + BRIGHT + "Making new commit..." + RESET)
		repo.git.add(A=True)
		repo.git.commit(m=message)

		if "origin" in [remote.name for remote in repo.remotes]:
			print(YELLOW + BRIGHT + "Pushing to master: " + NORMAL + "{}...".format(
				repo.remotes.origin.url) + RESET)
			repo.git.fetch()
			repo.git.push("--set-upstream", "origin", "master")
	else:
		print(YELLOW + BRIGHT + "No changes to commit..." + RESET)


########
# Config
########


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
		"backup_path": "~/shallow-backup",
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
			".ssh",
			".vim"
		],
		"gitignore"  : [
			"dotfiles/.ssh",
			"packages/",
			"dotfiles/.pypirc",
		]
	}


def create_config_file_if_needed():
	"""
	Creates config file if it doesn't exist already.
	"""
	backup_config_path = get_config_path()
	if not os.path.exists(backup_config_path):
		print(BLUE + BRIGHT + "Creating config file at {}".format(backup_config_path) + RESET)
		backup_config = get_default_config()
		write_config(backup_config)


def add_path_to_config(section, path):
	"""
	Adds the path under the correct section in the config file.
	FIRST ARG: [dot, config, other]
	SECOND ARG: path, relative to home directory for dotfiles, absolute for configs
	"""
	full_path = _home_prefix(path)
	if not os.path.exists(full_path):
		print(RED + BRIGHT + "ERR: {} doesn't exist.".format(full_path) + RESET)
		sys.exit(1)

	if section == "dot":
		# Make sure dotfile starts with a period
		if path[0] != ".":
			print(RED + BRIGHT + "ERR: Not a dotfile." + RESET)
			sys.exit(1)

		if not os.path.isdir(full_path):
			section = "dotfiles"
			print(BLUE + BRIGHT + "Adding {} to dotfile backup.".format(full_path) + RESET)
		else:
			section = "dotfolders"
			if path[-1] != "/":
				full_path += "/"
				path += "/"
			print(BLUE + BRIGHT + "Adding {} to dotfolder backup.".format(full_path) + RESET)

	# TODO: Add config section once configs backup prefs are moved to the config file
	elif section == "config":
		print(RED + BRIGHT + "ERR: Option not currently supported." + RESET)
		sys.exit(1)
	elif section == "other":
		print(RED + BRIGHT + "ERR: Option not currently supported." + RESET)
		sys.exit(1)

	config = get_config()
	file_set = set(config[section])
	file_set.update([path])
	config[section] = list(file_set)
	write_config(config)


def rm_path_from_config(path):
	"""
	Removes the path from a section in the config file. Exits if the path doesn't exist.
	Path, relative to home directory for dotfiles, absolute for configs
	"""
	flag = False
	config = get_config()
	for section, items in config.items():
		if path in items:
			print(BLUE + BRIGHT + "Removing {} from backup...".format(path) + RESET)
			items.remove(path)
			config[section] = items
			flag = True

	if not flag:
		print(RED + BRIGHT + "ERR: Not currently backing that path up..." + RESET)
	else:
		write_config(config)


def show_config():
	"""
	Print the config. Colorize section titles and indent contents.
	"""
	print_section_header("SHALLOW BACKUP CONFIG", RED)
	config = get_config()
	for section, contents in config.items():
		# Hide gitignore config
		if section == "gitignore":
			continue
		# Print backup path on same line
		if section == "backup_path":
			print(RED + BRIGHT + "Backup Path:" + RESET + contents)
		# Print section header and then contents indented.
		else:
			print(RED + BRIGHT + "\n{}: ".format(section.capitalize()) + RESET)
			for item in contents:
				print("    {}".format(item))

	print()


#####
# CLI
#####

def move_git_folder_to_path(source_path, new_path):
	"""
	Moves git folder and .gitignore to the new backup directory.
	"""
	git_dir = os.path.join(source_path, '.git')
	git_ignore_file = os.path.join(source_path, '.gitignore')

	try:
		move(git_dir, new_path)
		move(git_ignore_file, new_path)
		print(BLUE + BRIGHT + "Moving git repo to new destination" + RESET)
	except FileNotFoundError:
		pass


def prompt_for_path_update(config):
	"""
	Ask user if they'd like to update the backup path or not.
	If yes, update. If no... don't.
	"""
	current_path = config["backup_path"]
	print("{}{}Current shallow-backup path: {}{}{}".format(BLUE, BRIGHT, NORMAL, current_path, RESET))

	if prompt_yes_no("Would you like to update this?", GREEN):
		print(GREEN + BRIGHT + "Enter relative path:" + RESET)
		abs_path = os.path.abspath(input())
		print(BLUE + "\nUpdating shallow-backup path to {}".format(abs_path) + RESET)
		config["backup_path"] = abs_path
		write_config(config)
		make_dir_warn_overwrite(abs_path)
		move_git_folder_to_path(current_path, abs_path)


def prompt_for_git_url(repo):
	"""
	Ask user if they'd like to add a remote URL to their git repo.
	If yes, do it.
	"""
	if prompt_yes_no("Would you like to set a remote URL for this git repo?", GREEN):
		print(GREEN + BRIGHT + "Enter URL:" + RESET)
		remote_url = input()
		git_set_remote(repo, remote_url)


def destroy_backup_dir(backup_path):
	"""
	Deletes the backup directory and its content
	"""
	try:
		print("{} Deleting backup directory {} {}...".format(RED, backup_path, BRIGHT))
		rmtree(backup_path)
	except OSError as e:
		print("{} Error: {} - {}. {}".format(RED, e.filename, e.strerror, RESET))


def actions_menu_prompt():
	"""
	Prompt user for an action.
	"""
	# TODO: Implement `add` and `rm` path here.
	questions = [inquirer.List('choice',
	                           message=GREEN + BRIGHT + "What would you like to do?" + BLUE,
	                           choices=[' Back up dotfiles',
	                                    ' Back up configs',
	                                    ' Back up packages',
	                                    ' Back up fonts',
	                                    ' Back up everything',
	                                    ' Reinstall configs',
	                                    ' Reinstall packages',
	                                    ' Show config',
	                                    ' Destroy backup'
	                                    ],
	                           ),
	             ]

	answers = inquirer.prompt(questions)
	return answers.get('choice').strip().lower()


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
			print(RED + BRIGHT + "Removed config file..." + RESET)
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
		print(BLUE + NORMAL + "\nUpdating shallow-backup path to -> " + BRIGHT + "{}".format(
			abs_path) + RESET)
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
			if prompt_yes_no("Erase backup directory: {}?".format(backup_home_path), RED):
				destroy_backup_dir(backup_home_path)
			else:
				print("{} Exiting to prevent accidental deletion of backup directory... {}".format(
					RED, RESET))

	sys.exit()


if __name__ == '__main__':
	"""
	I'm just here so I don't get fined.
	"""
	cli()
