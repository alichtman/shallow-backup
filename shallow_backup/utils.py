import os
import sys
import subprocess as sp
from shutil import rmtree, copytree
from .printing import *


def run_cmd(command):
	"""
	Wrapper on subprocess.run that handles both lists and strings as shell commands.
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
	:param: command String representing command to run and write output of to file
	"""
	process = run_cmd(command)
	if process:
		with open(filepath, "w+") as f:
			f.write(process.stdout.decode('utf-8'))


def mkdir_warn_overwrite(path):
	"""
	Make destination dir if path doesn't exist, confirm before overwriting if it does.
	"""
	subdirs = ["dotfiles", "packages", "fonts", "configs"]
	if os.path.exists(path) and path.split("/")[-1] in subdirs:
		print_bright_red("Directory {} already exists\n".format(path))
		if prompt_yes_no("Erase directory and make new back up?", Fore.RED):
			rmtree(path)
			os.makedirs(path)
		else:
			print_bright_red("Exiting to prevent accidental deletion of data.")
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
		print_bright_red("Deleting backup directory: {}".format(backup_path))
		rmtree(backup_path)
	except OSError as e:
		print("{} Error: {} - {}. {}".format(Fore.RED, e.filename, e.strerror, Style.RESET_ALL))


def get_subfiles(directory):
	"""
	Returns list of absolute paths of immediate subfiles of a directory
	"""
	file_paths = []
	for path, subdirs, files in os.walk(directory):
		for name in files:
			file_paths.append(os.path.join(path, name))
	return file_paths


def copy_dir(source_dir, backup_path):
	"""
	Copy dotfolder from $HOME.
	"""
	invalid = {".Trash", ".npm", ".cache", ".rvm"}
	if len(invalid.intersection(set(source_dir.split("/")))) != 0:
		return

	if "Application Support" not in source_dir:
		copytree(source_dir, os.path.join(backup_path, source_dir.split("/")[-2]), symlinks=True)
	elif "Sublime" in source_dir:
		copytree(source_dir, os.path.join(backup_path, source_dir.split("/")[-3]), symlinks=True)
	else:
		copytree(source_dir, backup_path, symlinks=True)


def mkdir_or_pass(directory):
	if not os.path.isdir(directory):
		os.makedirs(directory)
	pass


def home_prefix(path):
	"""
	Appends the path to the user's home path.
	:param path: Path to be appended.
	:return: (str) ~/path
	"""
	return os.path.join(os.path.expanduser('~'), path)
