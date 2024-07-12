import os
import readline  # Imported to support arrow key navigation during input
import subprocess
import sys
from difflib import unified_diff
from pathlib import Path
from shutil import move, which

import git
from colorama import Fore
from git import GitCommandError

from .config import get_config
from .printing import (
    print_blue_bold,
    print_error_report_github_issue_and_exit,
    print_green_bold,
    print_path_red,
    print_path_yellow,
    print_red_bold,
    print_yellow,
    print_yellow_bold,
    prompt_yes_no,
)
from .utils import safe_mkdir

###########
# FUNCTIONS
###########


def color_diff(diff):
    """Colorizes the diff output. https://chezsoi.org/lucas/blog/colored-diff-output-with-python.html"""
    for line in diff:
        if line.startswith("+"):
            yield Fore.GREEN + line + Fore.RESET
        elif line.startswith("-"):
            yield Fore.RED + line + Fore.RESET
        elif line.startswith("^"):
            yield Fore.BLUE + line + Fore.RESET
        else:
            yield line


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


def create_gitignore(dir_path, key: str):
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
        else:
            print_error_report_github_issue_and_exit()
            # This next line will never be hit, but it is here to silence the lint about files_to_ignore possibly being unset.
            sys.exit(1)
    with open(os.path.join(dir_path, ".gitignore"), "w+") as f:
        for ignore in files_to_ignore:
            f.write("{}\n".format(ignore))


def safe_git_init(dir_path) -> tuple[git.Repo, bool]:
    """
    If there is no git repo inside the dir_path, initialize one.
    Returns tuple of (git.Repo, bool new_git_repo_created)
    """
    if not os.path.isdir(os.path.join(dir_path, ".git")):
        print_yellow_bold("Initializing new git repo...")
        try:
            repo = git.Repo.init(dir_path)
            return repo, True
        except GitCommandError:
            print_red_bold(
                "ERROR: We ran into some trouble creating the git repo. Double check that you have write permissions."
            )
            sys.exit(1)
    else:
        print_yellow_bold("Detected git repo.")
        repo = git.Repo(dir_path)
        return repo, False


def handle_separate_git_dir_in_dotfiles(dotfiles_path: Path, dry_run: bool = False):
    print_yellow_bold("Checking for separate git repo in dotfiles directory...")
    if ".git" in os.listdir(dotfiles_path):
        dotfiles_repo = git.Repo(dotfiles_path)
        if dotfiles_repo.git.status("--porcelain"):
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
                    dotfiles_repo,
                    dry_run=dry_run,
                )
                print_green_bold("Switching back to parent shallow-backup repo...")
        else:
            print_green_bold("Detected a nested dotfiles repo that is clean.")
    else:
        print_yellow_bold("No nested dotfiles repo detected.")


def git_add_all_and_print_status(repo: git.Repo):
    print_yellow("Staging all files for commit...")
    repo.git.add(all=True)
    print_yellow_bold(f"Git status of {repo.working_dir}")
    print(repo.git.status())


def install_trufflehog_git_hook(repo: git.Repo):
    """
    Make sure trufflehog and pre-commit are installed and on the PATH. Then register a pre-commit hook for the repo.
    """

    trufflehog_hook_text = """repos:
  - repo: local
    hooks:
      - id: trufflehog
        name: TruffleHog
        description: Detect secrets in your data.
        entry: bash -c 'trufflehog git file://. --since-commit HEAD --fail --only-verified --no-update'
        language: system
        stages: ["commit", "push"]
"""

    def update_precommit_file():
        with open(precommit_file, "w+") as f:
            f.write(trufflehog_hook_text)

        pass

    if not which("trufflehog"):
        print_red_bold(
            "trufflehog (https://github.com/trufflesecurity/trufflehog) is not installed. Please install it to continue."
        )
        sys.exit()
    if not which("pre-commit"):
        print_red_bold(
            "pre-commit (https://pre-commit.com/) is not installed. Please install it to continue."
        )
        sys.exit()

    precommit_file = Path(repo.working_dir) / ".pre-commit-config.yaml"
    if not precommit_file.exists():
        print_yellow_bold("Adding pre-commit config file...")
        update_precommit_file()
    else:
        # TODO: Add an update check opt out config option
        current_precommit_file_contents = precommit_file.read_text()
        if current_precommit_file_contents != trufflehog_hook_text:
            diff = unified_diff(
                current_precommit_file_contents.splitlines(),
                trufflehog_hook_text.splitlines(),
                lineterm="",
            )

            colored_diff = "\n".join(color_diff(diff))
            if colored_diff.strip() == "":
                print_yellow_bold(
                    "Your pre-commit config file is not up to date, but the only difference is whitespace. Updating automatically."
                )
                update_precommit_file()
            else:
                print_yellow_bold(
                    "Your pre-commit config file is not up to date. Here is the diff:"
                )
                print(colored_diff)

                if prompt_yes_no("Apply update?", Fore.YELLOW):
                    print_yellow_bold("Updating pre-commit config file...")
                    update_precommit_file()

    # Safe to run every time
    subprocess.call("pre-commit install", cwd=repo.working_dir, shell=True)


def git_add_all_commit_push(repo: git.Repo, dry_run: bool = False):
    """
    Stages all changed files in dir_path and its children folders for commit,
    commits them and pushes to a remote if it's configured.

    :param git.repo repo: The repo
    :param str message: The commit message
    """
    install_trufflehog_git_hook(repo)
    if repo.is_dirty():
        git_add_all_and_print_status(repo)
        if not prompt_yes_no(
            "Make a commit (with a trufflehog pre-commit hook)? Ctrl-C to exit",
            Fore.YELLOW,
        ):
            return
        if dry_run:
            print_yellow_bold("Dry run: Would have made a commit!")
            return
        print_yellow_bold("Making new commit...")
        process = subprocess.run(["git", "commit", "--verbose"], cwd=repo.working_dir)
        if process.returncode != 0:
            print_red_bold(
                "Failed to make a commit. The two most likely reasons for this are:\n\t1. No commit message was provided.\n\t2. trufflehog detected secrets in the commit.\nPlease resolve ths issue and try again."
            )
            sys.exit(1)
        else:
            print_yellow_bold("Successful commit.")

        if prompt_yes_no(
            "Push commit to remote? Did you check for secrets carefully? trufflehog is not perfect...",
            Fore.YELLOW,
        ):
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
