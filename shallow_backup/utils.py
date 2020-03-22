import os
import sys
import subprocess as sp
from shutil import rmtree, copytree
from .printing import *


def run_cmd(command):
	"""
	Wrapper on subprocess.run to handle shell commands as either a list of args
	or a single string.
	"""
	try:
		if not isinstance(command, list):
			process = sp.run(command.split(), stdout=sp.PIPE, stderr=sp.DEVNULL)
			return process
		else:
			process = sp.run(command, stdout=sp.PIPE, stderr=sp.DEVNULL)
			return process
	except FileNotFoundError:  # If package manager is missing
		return None


def run_cmd_write_stdout(command, filepath):
	"""
	Runs a command and then writes its stdout to a file
	:param: command str representing command to run
	:param: filepath str file to write command's stdout to
	"""
	process = run_cmd(command)
	if process and process.returncode == 0:
		with open(filepath, "w+") as f:
			f.write(process.stdout.decode('utf-8'))
	else:
		print_path_red("An error occurred while running: $", command)
		return 1


def new_dir_is_valid(abs_path):
	if os.path.isfile(abs_path):
		print_path_red('New path is a file:', abs_path)
		print_red_bold('Please enter a directory.\n')
		return False
	return True


def safe_mkdir(directory):
	"""
	Makes directory if it doesn't already exist.
	"""
	if not os.path.isdir(directory):
		os.makedirs(directory)


def mkdir_overwrite(path):
	"""
	Makes a new directory, destroying the contents of the dir at path, if it exits.
	Ensures .git and .gitignore files inside of directory are not delected.
	"""
	if os.path.isdir(path):
		dirs = []
		files = []
		for f in os.listdir(path):
			full_path = os.path.join(path, f)
			# Allow dotfiles to be a sub-repo, and protect img folder.
			if full_path.endswith(".git") or \
			   full_path.endswith(".gitignore") or \
			   full_path.endswith("README.md") or \
			   full_path.endswith("img"):
				continue

			if os.path.isdir(full_path):
				dirs.append(full_path)
			else:
				files.append(full_path)

		[os.remove(file) for file in files]
		[rmtree(dir) for dir in dirs]
	else:
		os.makedirs(path)


def mkdir_warn_overwrite(path):
	"""
	Make destination dir if path doesn't exist, confirm before overwriting if it does.
	"""
	subdirs = ["dotfiles", "packages", "fonts", "configs"]
	if os.path.exists(path) and path.split("/")[-1] in subdirs:
		print_path_red("Directory already exists:", path)
		if prompt_yes_no("Erase directory and make new back up?", Fore.RED):
			mkdir_overwrite(path)
		else:
			print_red_bold("Exiting to prevent accidental deletion of data.")
			sys.exit()
	elif not os.path.exists(path):
		os.makedirs(path)
		print_path_blue("Created directory:", path)


def overwrite_dir_prompt_if_needed(path, needed):
	"""
	Prompts the user before deleting the directory if needed.
	This function lets the CLI args silence the prompts.
	:param path: absolute path
	:param needed: boolean
	"""
	if not needed:
		mkdir_warn_overwrite(path)
	else:
		mkdir_overwrite(path)


def empty_backup_dir_check(backup_path, backup_type):
	if not os.path.isdir(backup_path) or not os.listdir(backup_path):
		print_red_bold('No {} backup found.'.format(backup_type))
		sys.exit(1)


def destroy_backup_dir(backup_path):
	"""
	Deletes the backup directory and its content
	"""
	try:
		print_path_red("Deleting backup directory:", backup_path)
		rmtree(backup_path)
	except OSError as e:
		print_red_bold("Error: {} - {}".format(e.filename, e.strerror))


def get_abs_path_subfiles(directory):
	"""
	Returns list of absolute paths of files and folders contained in a directory,
	excluding the root .git directory and root .gitignore..
	"""
	file_paths = []
	for path, _, files in os.walk(directory):
		for name in files:
			joined = os.path.join(path, name)
			root_git_dir = os.path.join(directory, ".git")
			root_gitignore = os.path.join(directory, ".gitignore")
			if root_git_dir not in joined and root_gitignore not in joined:
				file_paths.append(joined)
			else:
			    print(f"Excluded: {joined}")
	return file_paths


def copy_dir_if_valid(source_dir, backup_path):
	"""
	Copy dotfolder from $HOME, excluding invalid directories.
	"""
	invalid = {".Trash", ".npm", ".cache", ".rvm"}
	if len(invalid.intersection(set(source_dir.split("/")))) != 0:
		return
	copytree(source_dir, backup_path, symlinks=True)


def home_prefix(path):
	"""
	Appends the path to the user's home path.
	:param path: Path to be appended.
	:return: (str) ~/path
	"""
	home_path = os.path.expanduser('~')
	return os.path.join(home_path, path)


def expand_to_abs_path(path):
	"""
	Expands relative and user's home paths to the respective absolute path. Environment
	variables found on the input path will also be expanded.
	:param path: Path to be expanded.
	:return: (str) The absolute path.
	"""
	expanded_path = os.path.expanduser(path)
	expanded_path = os.path.expandvars(expanded_path)
	return os.path.abspath(expanded_path)


def create_dir_if_doesnt_exist(path):
	os.makedirs(path, exist_ok=True)
