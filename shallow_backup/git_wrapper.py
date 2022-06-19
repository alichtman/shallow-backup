import os
from pathlib import Path
import sys
import git
from git import GitCommandError
from shutil import move
from .printing import *
from .config import get_config
from .utils import safe_mkdir

#########
# GLOBALS
#########

COMMIT_MSG = {
    "all": "Back up everything.",
    "configs": "Back up configs.",
    "dotfiles": "Back up dotfiles.",
    "fonts": "Back up fonts.",
    "full_backup": "Full back up.",
    "packages": "Back up packages.",
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
        origin = repo.create_remote("origin", remote_url)
        origin.fetch()
    except git.CommandError:
        print_yellow_bold("Updating existing remote URL...")
        repo.delete_remote(repo.remotes.origin)
        origin = repo.create_remote("origin", remote_url)
        origin.fetch()


def create_gitignore(dir_path, key):
    """
    Creates a .gitignore file that ignores all files listed in config.
    Handles backwards compatibility for the default-gitignore -> root-gitignore
    change and the introduction of the dotfiles-gitignore key in v4.0.
    """
    safe_mkdir(dir_path)
    gitignore_path = os.path.join(dir_path, ".gitignore")
    print_yellow_bold(
        f"Updating .gitignore file at {gitignore_path} with config from {key}"
    )
    try:
        files_to_ignore = get_config()[key]
    except KeyError:
        if key == "root-gitignore":
            files_to_ignore = get_config()["default-gitignore"]
        elif key == "dotfiles-gitignore":
            files_to_ignore = []
    with open(os.path.join(dir_path, ".gitignore"), "w+") as f:
        for ignore in files_to_ignore:
            f.write("{}\n".format(ignore))


def safe_git_init(dir_path) -> (git.Repo, bool):
    """
    If there is no git repo inside the dir_path, intialize one.
    Returns tuple of (git.Repo, bool new_git_repo_created)
    """
    if not os.path.isdir(os.path.join(dir_path, ".git")):
        print_yellow_bold("Initializing new git repo...")
        try:
            repo = git.Repo.init(dir_path)
            return repo, True
        except GitCommandError:
            print_red_bold("ERROR: We ran into some trouble creating the git repo. Double check that you have write permissions.")
            sys.exit(1)
    else:
        print_yellow_bold("Detected git repo.")
        repo = git.Repo(dir_path)
        return repo, False


def handle_separate_git_dir_in_dotfiles(dotfiles_path: Path, dry_run: bool = False):
    print_yellow_bold("Checking for separate git repo in dotfiles directory...")
    if ".git" in os.listdir(dotfiles_path):
        dotfiles_repo = git.Repo(dotfiles_path)
        if dotfiles_repo.is_dirty():
            print_green_bold("Detected a nested dotfiles repo that is dirty!!")
            print_green_bold(
                "Do you want to create and push a commit in this repo first, before dealing with the parent?"
            )
            if prompt_yes_no(
                "If you do not, the parent repo will not be able to commit the dotfile changes (due to a dirty submodule)",
                Fore.YELLOW,
            ):
                print_green_bold("Okay, switching into dotfiles subrepo...")
                git_add_all_commit_push(
                    dotfiles_repo, message="dotfiles", dry_run=dry_run
                )
                print_green_bold("Switching back to parent shallow-backup repo...")


def prompt_to_show_git_diff(repo):
    if prompt_yes_no("Show git diff?", Fore.BLUE):
        print(repo.git.diff(staged=True, color="always"))


def git_add_all_and_print_status(repo):
    print_yellow("Staging all files for commit...")
    repo.git.add(all=True)
    print(repo.git.status())
    prompt_to_show_git_diff(repo)


def git_add_all_commit_push(repo: git.Repo, message: str, dry_run: bool = False):
    """
    Stages all changed files in dir_path and its children folders for commit,
    commits them and pushes to a remote if it's configured.

    :param git.repo repo: The repo
    :param str message: The commit message
    """
    if repo.is_dirty():
        git_add_all_and_print_status(repo)
        if not prompt_yes_no("Make a commit? Ctrl-C to exit", Fore.BLUE):
            return
        if dry_run:
            print_yellow_bold("Dry run: Would have made a commit!")
            return
        print_yellow_bold("Making new commit...")
        repo.git.add(A=True)
        try:
            repo.git.commit(m=COMMIT_MSG[message])
        except git.exc.GitCommandError as e:
            error = e.stdout.strip()
            error = error[error.find("'") + 1 : -1]
            print_red_bold(f"ERROR on Commit: {e.command}\n{error}\n")
            print_red_bold(
                "Please open a new issue at https://github.com/alichtman/shallow-backup/issues/new"
            )
            return

        print_yellow_bold("Successful commit.")

        if "origin" in [remote.name for remote in repo.remotes]:
            print_path_yellow(
                "Pushing to remote:",
                f"{repo.remotes.origin.url}[origin/{repo.active_branch.name}]...",
            )
            repo.git.fetch()
            repo.git.push("--set-upstream", "origin", "HEAD")
    else:
        print_yellow_bold("No changes to commit...")


def move_git_repo(source_path, dest_path):
    """
    Moves git folder and .gitignore to the new backup directory.
    Exits if there is already a git repo in the directory.
    """
    dest_git_dir = os.path.join(dest_path, ".git")
    dest_git_ignore = os.path.join(dest_path, ".gitignore")
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

    git_dir = os.path.join(source_path, ".git")
    git_ignore_file = os.path.join(source_path, ".gitignore")

    try:
        move(git_dir, dest_path)
        move(git_ignore_file, dest_path)
        print_blue_bold("Moving git repo to new location.")
    except FileNotFoundError:
        pass
