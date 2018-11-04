import os
import sys
import git
from shutil import move
from printing import *
from config import get_config

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
	print(Fore.YELLOW + Style.BRIGHT + "Setting remote URL to -> " + Style.NORMAL + "{}...".format(remote_url) + Style.RESET_ALL)

	try:
		origin = repo.create_remote('origin', remote_url)
		origin.fetch()
	except git.CommandError:
		print_yellow_bold("Updating existing remote URL...")
		repo.delete_remote(repo.remotes.origin)
		origin = repo.create_remote('origin', remote_url)
		origin.fetch()


def safe_create_gitignore(dir_path):
	"""
	Creates a .gitignore file that ignores all files listed in config.
	"""
	gitignore_path = os.path.join(dir_path, ".gitignore")
	if os.path.exists(gitignore_path):
		print_yellow_bold("Detected .gitignore file.")
		pass
	else:
		print_yellow_bold("Creating default .gitignore...")
		files_to_ignore = get_config()["default-gitignore"]
		with open(gitignore_path, "w+") as f:
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


def git_add_all_commit_push(repo, message):
	"""
	Stages all changed files in dir_path and its children folders for commit,
	commits them and pushes to a remote if it's configured.
	"""
	if repo.index.diff(None) or repo.untracked_files:
		print_yellow_bold("Making new commit...")
		repo.git.add(A=True)
		repo.git.commit(m=COMMIT_MSG[message])
		print_yellow_bold("Successful commit.")

		if "origin" in [remote.name for remote in repo.remotes]:
			print(Fore.YELLOW + Style.BRIGHT + "Pushing to master: " + Style.NORMAL + "{}...".format(
				repo.remotes.origin.url) + Style.RESET_ALL)
			repo.git.fetch()
			repo.git.push("--set-upstream", "origin", "master")
	else:
		print_yellow_bold("No changes to commit...")


def move_git_repo(source_path, new_path):
	"""
	Moves git folder and .gitignore to the new backup directory.
	"""
	new_git_dir = os.path.join(new_path, '.git')
	new_git_ignore = os.path.join(new_path, '.gitignore')
	if os.path.exists(new_git_dir) or os.path.exists(new_git_ignore):
		print_red_bold("A git repo already exists here: {}".format(new_path))
		print_red_bold("Please choose a different backup path.")
		sys.exit()

	git_dir = os.path.join(source_path, '.git')
	git_ignore_file = os.path.join(source_path, '.gitignore')

	try:
		move(git_dir, new_path)
		move(git_ignore_file, new_path)
		print_blue_bold("Moving git repo to new location.")
	except FileNotFoundError:
		pass
