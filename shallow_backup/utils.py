import os
import subprocess as sp
from shutil import rmtree, copytree
from .printing import *


def run_cmd(command: str):
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


def run_cmd_write_stdout(command, filepath) -> int:
	"""
	Runs a command and then writes its stdout to a file.
	Returns the returncode if the return value is not 0.
	:param: command str representing command to run
	:param: filepath str file to write command's stdout to
	"""
	process = run_cmd(command)
	if process and process.returncode == 0:
		with open(filepath, "w+") as f:
			f.write(process.stdout.decode('utf-8'))
	elif process:
		print_path_red("An error occurred while running: $", command)
		return process.returncode
	else:
		print_path_red("An error occurred while running: $", command)
		return -1


def run_cmd_return_bool(command: str) -> bool:
	"""Run a bash command and return True if the exit code is 0, False otherwise"""
	return os.system(command) == 0


def evaluate_condition(condition: str, backup_or_reinstall: str, dotfile_path: str) -> bool:
	"""Evaluates the condition, if it exists, in bash and returns True or False, while providing output
	detailing what is going on.
	:param condition: A string that will be evaluated by bash.
	:param backup_or_reinstall: The only valid inputs are: "backup" or "reinstall"
	:param dotfile_path: Path to dotfile (relative to $HOME, or absolute) for which the condition is being evaluated
	"""
	if condition:
		print_blue(f"\n{backup_or_reinstall.capitalize()} condition detected for {dotfile_path}.")
		condition_success = run_cmd_return_bool(condition)
		if not condition_success:
			print_blue(f"SKIPPING {backup_or_reinstall.lower()} based on <{condition}>")
			return False
		else:
			print_blue(f"NOT skipping {backup_or_reinstall.lower()} based on <{condition}>")
			return True
	else:
		return True


def check_if_path_is_valid_dir(abs_path):
	"""Returns False is the path leads to a file, True otherwise."""
	if os.path.isfile(abs_path):
		print_path_red('New path is a file:', abs_path)
		print_red_bold('Please enter a directory.\n')
		return False
	return True


def safe_mkdir(directory):
	"""Makes directory if it doesn't already exist, creating all intermediate directories."""
	if not os.path.isdir(directory):
		os.makedirs(directory, exist_ok=True)


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

		for file in files:
			os.remove(file)

		for directory in dirs:
			rmtree(directory)
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


def overwrite_dir_prompt_if_needed(path: str, no_prompt: bool):
	"""
	Prompts the user before deleting the directory if needed.
	This function lets the CLI args silence the prompts.
	:param path: absolute path
	:param no_prompt: Flag that determines if prompting the user is needed.
	"""
	if not no_prompt:
		mkdir_warn_overwrite(path)
	else:
		mkdir_overwrite(path)


def exit_if_dir_is_empty(backup_path: str, backup_type: str):
	"""Exit if the backup_path is not a directory or contains no files."""
	if not os.path.isdir(backup_path) or not os.listdir(backup_path):
		print_red_bold('No {} backup found.'.format(backup_type))
		sys.exit(1)


def destroy_backup_dir(backup_path):
	"""Deletes the backup directory and its content"""
	try:
		print_path_red("Deleting backup directory:", backup_path)
		rmtree(backup_path)
	except OSError as e:
		print_red_bold("Error: {} - {}".format(e.filename, e.strerror))


def get_abs_path_subfiles(directory: str) -> list:
	"""Returns list of absolute paths of files and folders contained in a directory,
	excluding the .git directory, .gitignore, img/ and README.md in the root dir.
	:param directory: Absolute path to directory to search
	"""
	file_paths = []
	for path, _, files in os.walk(directory):
		for name in files:
			joined = os.path.join(path, name)
			root_git_dir = os.path.join(directory, ".git")
			root_gitignore = os.path.join(directory, ".gitignore")
			img = os.path.join(directory, "img")
			readme = os.path.join(directory, "README.md")
			if not any(x in joined for x in [root_git_dir, root_gitignore, img, readme]):
				file_paths.append(joined)
			else:
				print_path_red("Excluded:", joined)
	return file_paths


def copy_dir_if_valid(source_dir, backup_path):
	"""
	Copy dotfolder from source_dir to backup_path, excluding invalid directories.
	"""
	invalid = {".Trash", ".npm", ".cache", ".rvm"}
	if invalid.intersection(set(source_dir.split("/"))) != set():
		return
	copytree(source_dir, backup_path, symlinks=False)


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

