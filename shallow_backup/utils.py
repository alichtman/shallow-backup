import os
import sys
import subprocess as sp
from shutil import rmtree, copytree
from printing import *


def run_cmd(command):
	"""
	Wrapper on subprocess.run to handle shell commands as either a list of args
	or a single string.
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


def run_cmd_write_stdout(command, filepath):
	"""
	Runs a command and then writes its stdout to a file
	:param: command str representing command to run
	"""
	process = run_cmd(command)
	if process:
		with open(filepath, "w+") as f:
			f.write(process.stdout.decode('utf-8'))


def mkdir_overwrite(path):
	"""
	Makes a new directory, destroying the one at the path if it exits.
	"""
	if os.path.isdir(path):
		rmtree(path)
	os.makedirs(path)


def mkdir_warn_overwrite(path):
	"""
	Make destination dir if path doesn't exist, confirm before overwriting if it does.
	"""
	subdirs = ["dotfiles", "packages", "fonts", "configs"]
	if os.path.exists(path) and path.split("/")[-1] in subdirs:
		print_red_bold("Directory {} already exists\n".format(path))
		if prompt_yes_no("Erase directory and make new back up?", Fore.RED):
			mkdir_overwrite(path)
		else:
			print_red_bold("Exiting to prevent accidental deletion of data.")
			sys.exit()
	elif not os.path.exists(path):
		os.makedirs(path)
		print(Fore.BLUE + Style.BRIGHT + "CREATED DIR: " + Style.NORMAL + path + Style.RESET_ALL)


def destroy_backup_dir(backup_path):
	"""
	Deletes the backup directory and its content
	"""
	try:
		# TODO: PRINT PATH STYLING. PATH SHOULD NOT BE BOLDED.
		print_red_bold("Deleting backup directory: {}".format(backup_path))
		rmtree(backup_path)
	except OSError as e:
		print("{} Error: {} - {}. {}".format(Fore.RED, e.filename, e.strerror, Style.RESET_ALL))


def get_abs_path_subfiles(directory):
	"""
	Returns list of absolute paths of immediate files and folders in a directory.
	"""
	file_paths = []
	for path, subdirs, files in os.walk(directory):
		for name in files:
			file_paths.append(os.path.join(path, name))
	return file_paths


def copy_dir_if_valid(source_dir, backup_path):
	"""
	Copy dotfolder from $HOME, excluding invalid directories.
	"""
	invalid = {".Trash", ".npm", ".cache", ".rvm"}
	if len(invalid.intersection(set(source_dir.split("/")))) != 0:
		return
	dest = os.path.join(backup_path, os.path.split(source_dir)[-1])
	copytree(source_dir, dest, symlinks=True)


def safe_mkdir(directory):
	"""
	Makes directory if it doesn't already exist.
	:param directory:
	:return:
	"""
	if not os.path.isdir(directory):
		os.makedirs(directory)


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
	Expands relative and user's home paths to the respective absolute path.
	:param path: Path to be expanded.
	:return: (str) The absolute path.
	"""
	expanded_path = os.path.expanduser(path)
	return os.path.abspath(expanded_path)
