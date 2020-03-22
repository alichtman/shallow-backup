import os
import sys
import git
from shutil import move
from .printing import *
from .config import get_config

#########
# GLOBALS
#########

COMMIT_MSG = {
	"fonts": "Back up fonts.",
	"packages": "Back up packages.",
	"configs": "Back up configs.",
	"all": "Full back up.",
	"dotfiles": "Back up dotfiles."
}

###########
# FUNCTIONS
###########


def git_set_remote(repo, remote_url):
	"""
	Sets git repo upstream URL and fast-forwards history.
	"""
	print_path_yellow("Setting remote URL to:", "{}...".format(remote_url))

	try:
		origin = repo.create_remote('origin', remote_url)
		origin.fetch()
	except git.CommandError:
		print_yellow_bold("Updating existing remote URL...")
		repo.delete_remote(repo.remotes.origin)
		origin = repo.create_remote('origin', remote_url)
		origin.fetch()


def create_gitignore(dir_path, key):
	"""
	Creates a .gitignore file that ignores all files listed in config.
	Handles backwards compatibility for the default-gitignore -> root-gitignore
	change and the introduction of the dotfiles-gitignore key in v4.0.
	"""
	gitignore_path = os.path.join(dir_path, ".gitignore")
	print_yellow_bold(f"Updating .gitignore file at {gitignore_path} with config from {key}")
	try:
		files_to_ignore = get_config()[key]
	except KeyError:
		if key == "root-gitignore":
			files_to_ignore = get_config()["default-gitignore"]
		elif key == "dotfiles-gitignore":
			pass
	with open(os.path.join(dir_path, ".gitignore"), "w+") as f:
		for ignore in files_to_ignore:
			f.write("{}\n".format(ignore))


def safe_git_init(dir_path):
	"""
	If there is no git repo inside the dir_path, intialize one.
	Returns tuple of (git.Repo, bool new_git_repo_created)
	"""
	if not os.path.isdir(os.path.join(dir_path, ".git")):
		print_yellow_bold("Initializing new git repo...")
		repo = git.Repo.init(dir_path)
		return repo, True
	else:
		print_yellow_bold("Detected git repo.")
		repo = git.Repo(dir_path)
		return repo, False


def git_add_all_commit_push(repo, message, separate_dotfiles_repo=False):
	"""
	Stages all changed files in dir_path and its children folders for commit,
	commits them and pushes to a remote if it's configured.

	:param git.repo repo: The repo
	:param str message: The commit message
	:param bool separate_dotfiles_repo: Flag for denoting a workflow where git submodules are used to maintain a separate repo for just dotfiles.
	"""
	if separate_dotfiles_repo:
		print_yellow_bold("Skipping commit to avoid git submodule error.")
		print_yellow_bold("Issue tracked at: https://github.com/alichtman/shallow-backup/issues/229")
		return

	if repo.index.diff(None) or repo.untracked_files:
		print_yellow_bold("Making new commit...")
		repo.git.add(A=True)
		try:
			repo.git.commit(m=COMMIT_MSG[message])
			# Git submodule issue https://github.com/alichtman/shallow-backup/issues/229
		except git.exc.GitCommandError as e:
			error = e.stdout.strip()
			error = error[error.find("\'") + 1:-1]
			print_red_bold(f"ERROR on Commit: {e.command}\n{error}\n")
			print_red_bold("Issue tracked at: https://github.com/alichtman/shallow-backup/issues/229")
			return

		print_yellow_bold("Successful commit.")

		if "origin" in [remote.name for remote in repo.remotes]:
			print_path_yellow("Pushing to master:", "{}...".format(repo.remotes.origin.url))

			repo.git.fetch()
			repo.git.push("--set-upstream", "origin", "master")
	else:
		print_yellow_bold("No changes to commit...")


def move_git_repo(source_path, dest_path):
	"""
	Moves git folder and .gitignore to the new backup directory.
	Exits if there is already a git repo in the directory.
	"""
	dest_git_dir = os.path.join(dest_path, '.git')
	dest_git_ignore = os.path.join(dest_path, '.gitignore')
	git_exists = os.path.exists(dest_git_dir)
	gitignore_exists = os.path.exists(dest_git_ignore)

	if git_exists or gitignore_exists:
		print_red_bold("Evidence of a git repo has been detected.")
		if git_exists:
			print_path_red("A git repo already exists here:", dest_git_dir)
		if gitignore_exists:
			print_path_red("A gitignore file already exists here:", dest_git_ignore)
		print_red_bold("Exiting to prevent accidental deletion of user data.")
		sys.exit(1)

	git_dir = os.path.join(source_path, '.git')
	git_ignore_file = os.path.join(source_path, '.gitignore')

	try:
		move(git_dir, dest_path)
		move(git_ignore_file, dest_path)
		print_blue_bold("Moving git repo to new location.")
	except FileNotFoundError:
		pass
