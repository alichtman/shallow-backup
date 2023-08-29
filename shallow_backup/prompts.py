import os
import sys
import inquirer
from .utils import *
from .printing import *
from .config import *
from .git_wrapper import git_set_remote, move_git_repo
from .utils import check_if_path_is_valid_dir


def path_update_prompt(config):
    """
    Ask user if they'd like to update the backup path or not.
    If yes, update. If no... don't.
    """
    current_path = config["backup_path"]
    print_path_blue("Current shallow-backup path:", current_path)
    if prompt_yes_no(
        "Would you like to move this somewhere else?", Fore.GREEN, invert=True
    ):
        while True:
            print_green_bold("Enter relative or absolute path:")
            abs_path = expand_to_abs_path(input())

            if not check_if_path_is_valid_dir(abs_path):
                continue

            print_path_blue("\nUpdating shallow-backup path to:", abs_path)
            mkdir_warn_overwrite(abs_path)
            move_git_repo(current_path, abs_path)
            config["backup_path"] = abs_path
            write_config(config)
            return


def git_url_prompt(repo):
    """
    Ask user if they'd like to add a remote URL to their git repo.
    If yes, do it.
    """
    print_red_bold(
        "WARNING: If you back up to a public remote, make sure no sensitive files are included by modifying the .gitignore."
    )
    if prompt_yes_no(
        "Would you like to set a remote URL for this git repo?", Fore.GREEN
    ):
        print_green_bold("Enter URL:")
        remote_url = input()
        git_set_remote(repo, remote_url)


def add_to_config_prompt():
    """
    Prompt sequence for a user to add a path to the config file under
    either the dot or config sections.
    """
    add_prompt = [
        inquirer.List(
            "choice",
            message=Fore.GREEN
            + Style.BRIGHT
            + "Which section would you like to add this to?"
            + Fore.BLUE,
            choices=[
                " Dots",
                " Configs",
            ],
        )
    ]

    section = inquirer.prompt(add_prompt).get("choice").strip().lower()
    config = get_config()

    # Prompt until we get a valid path.
    while True:
        print_green_bold("Enter a path to add to {}:".format(section))
        expanded_path = expand_to_abs_path(input())
        split_path = expanded_path.split("/")

        # Check if path exists.
        if not os.path.exists(expanded_path):
            print_red_bold("ERR: {} doesn't exist.".format(expanded_path))
            continue

        config_key = None
        if section == "dots":
            # Make sure it's actually a dotfile
            if split_path[-1][0] != ".":
                print_red_bold("ERR: Not a dotfile.")
                continue

            # Determine if adding to dotfiles or dotfolders
            if not os.path.isdir(expanded_path):
                config_key = "dotfiles"
                print_blue_bold("Adding {} to dotfile backup.".format(expanded_path))
            else:
                config_key = "dotfolders"
                print_blue_bold("Adding {} to dotfolder backup.".format(expanded_path))

            # Add path to config ensuring no duplicates.
            updated_config_key = set(config[config_key] + [path])
            config[config_key] = list(updated_config_key)
            write_config(config)
            break

        elif section == "config":
            # Prompt for folder name
            print_green_bold("Enter a name for this config:")
            dir_name = input()
            config_key = "config_mapping"
            to_add_to_cfg = (expanded_path, dir_name)
            print_blue_bold("Adding {} to config backup.".format(expanded_path))

            # Get dictionary of {path_to_backup: dest, ...}
            config_path_dict = config[config_key]
            config_path_dict[to_add_to_cfg[0]] = to_add_to_cfg[1]
            config[config_key] = config_path_dict
            write_config(config)
            break


def remove_from_config_prompt():
    """
    Sequence of prompts for a user to remove a path from the config.
    2-layer selection screen. First screen is for choosing dot or
    config, and then next selection is for the specific path.
    """
    # Get section to display.
    section_prompt = [
        inquirer.List(
            "choice",
            message=Fore.GREEN
            + Style.BRIGHT
            + "Which section would you like to remove a path from?"
            + Fore.BLUE,
            choices=[" Dotfiles", " Dotfolders", " Configs"],
        )
    ]

    config = get_config()
    section = inquirer.prompt(section_prompt).get("choice").strip().lower()
    if section == "configs":
        section = "config_mapping"
    paths = config[section]
    # Get only backup paths, not dest paths if it's a dictionary.
    if isinstance(paths, dict):
        paths = list(paths.keys())

    path_prompt = [
        inquirer.List(
            "choice",
            message=Fore.GREEN + Style.BRIGHT + "Select a path to remove." + Fore.BLUE,
            choices=paths,
        )
    ]
    path_to_remove = inquirer.prompt(path_prompt).get("choice")
    print_blue_bold("Removing {} from backup...".format(path_to_remove))
    paths.remove(path_to_remove)
    config[section] = paths
    write_config(config)


def main_menu_prompt():
    """
    Prompt user for an action.
    """
    questions = [
        inquirer.List(
            "choice",
            message=Fore.GREEN
            + Style.BRIGHT
            + "What would you like to do?"
            + Fore.BLUE,
            choices=[
                " Back up all",
                " Back up configs",
                " Back up dotfiles",
                " Back up fonts",
                " Back up packages",
                " Reinstall all",
                " Reinstall configs",
                " Reinstall dotfiles",
                " Reinstall fonts",
                " Reinstall packages",
                " Add path to config",
                " Remove path from config",
                " Show config",
                " Destroy backup",
            ],
        ),
    ]

    answers = inquirer.prompt(questions)

    if answers:
        return answers.get("choice").strip().lower()
    else:
        # KeyboardInterrupts
        sys.exit(1)
