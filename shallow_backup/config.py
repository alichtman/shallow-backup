import os
import sys
import json
import stat
from os import path, environ, chmod
from .printing import *
from .compatibility import *
from .utils import safe_mkdir, strip_home
from .constants import ProjInfo


def get_xdg_config_path() -> str:
    """Returns path to $XDG_CONFIG_HOME, or ~/.config, if it doesn't exist."""
    return environ.get("XDG_CONFIG_HOME") or path.join(path.expanduser("~"), ".config")


def get_config_path() -> str:
    """
    Detects if in testing or prod env, and returns the right config path.
    :return: Path to config.
    """
    test_config_path = environ.get("SHALLOW_BACKUP_TEST_CONFIG_PATH", None)
    if test_config_path:
        return test_config_path
    else:
        return path.join(get_xdg_config_path(), "shallow-backup.conf")


def get_config() -> dict:
    """
    :return Config.
    """
    config_path = get_config_path()
    with open(config_path) as file:
        try:
            config = json.load(file)
        except json.decoder.JSONDecodeError:
            print_red_bold(f"ERROR: Invalid syntax in {config_path}")
            sys.exit(1)
    return config


def write_config(config) -> None:
    """
    Write to config file
    """
    with open(get_config_path(), "w") as file:
        json.dump(config, file, indent=4)


def get_default_config() -> dict:
    """Returns a default, platform specific config."""
    return {
        "backup_path": "~/shallow-backup",
        "dotfiles": {
            ".bash_profile": {
                "backup_condition": "",
                "reinstall_condition": "",
            },
            ".bashrc": {},
            ".config/git": {},
            ".config/nvim/init.vim": {},
            ".config/tmux": {},
            ".config/zsh": {},
            ".profile": {},
            ".pypirc": {},
            ".ssh": {},
            ".zshenv": {},
            f"{strip_home(get_config_path())}": {},
        },
        "root-gitignore": ["dotfiles/.ssh", "dotfiles/.pypirc", ".DS_Store"],
        "dotfiles-gitignore": [
            ".ssh",
            ".pypirc",
            ".DS_Store",
        ],
        "config_mapping": get_config_paths(),
        "lowest_supported_version": ProjInfo.VERSION,
    }


def safe_create_config() -> None:
    """
    Creates config file (with 644 permissions) if it doesn't exist already. Prompts to update
    it if an outdated version is detected.
    """
    backup_config_path = get_config_path()
    # If it doesn't exist, create it.
    if not os.path.exists(backup_config_path):
        print_path_blue("Creating config file at:", backup_config_path)
        backup_config = get_default_config()
        safe_mkdir(os.path.split(backup_config_path)[0])
        write_config(backup_config)
        # $ chmod 644 config_file
        chmod(
            get_config_path(), stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        )


def check_insecure_config_permissions() -> bool:
    """Checks to see if group/others can write to config file.
    Returns: True if they can, False otherwise."""
    config_path = get_config_path()
    mode = os.stat(config_path).st_mode
    if mode & stat.S_IWOTH or mode & stat.S_IWGRP:
        print_red_bold(
            f"WARNING: {config_path} is writable by group/others and vulnerable to attack. To resolve, run: \n\t$ chmod 644 {config_path}"
        )
        return True
    else:
        return False


def delete_config_file() -> None:
    """Delete config file."""
    config_path = get_config_path()
    if os.path.isfile(config_path):
        print_red_bold("Deleting config file.")
        os.remove(config_path)
    else:
        print_red_bold("ERROR: No config file found.")


def add_dot_path_to_config(backup_config: dict, file_path: str) -> dict:
    """
    Add dotfile to config with default reinstall and backup conditions.
    Exit if the file_path parameter is invalid.
    :backup_config: dict representing current config
    :file_path:		str  relative or absolute path of file to add to config
    :return new backup config
    """
    abs_path = path.abspath(file_path)
    if not path.exists(abs_path):
        print_path_red("Invalid file path:", abs_path)
        return backup_config
    else:
        stripped_home_path = strip_home(abs_path)
        print_path_blue("Added:", stripped_home_path)
        backup_config["dotfiles"][stripped_home_path] = {}
    return backup_config


def show_config():
    """
    Print the config. Colorize section titles and indent contents.
    """
    print_section_header("SHALLOW BACKUP CONFIG", Fore.RED)
    for section, contents in get_config().items():
        # Print backup path on same line
        if section == "backup_path":
            print_path_red("Backup Path:", contents)
        elif section == "config_mapping":
            print_red_bold("\nConfigs:")
            for config_path, dest in contents.items():
                print(f"	{config_path} -> {dest}")
        # Print section header and contents. (Dotfiles)
        elif section == "dotfiles":
            print_path_red(
                "\nDotfiles:",
                "(Backup and Reinstall conditions will be shown if they exist)",
            )
            for dotfile, options in contents.items():
                backup_condition = options.get("backup_condition", "")
                reinstall_condition = options.get("reinstall_condition", "")
                if backup_condition or reinstall_condition:
                    print(f"	{dotfile} ->")
                    print(f'\t\tbackup_condition: "{backup_condition}"')
                    print(f'\t\treinstall_condition: "{reinstall_condition}"')
                else:
                    print(f"	{dotfile}")
        elif section == "lowest_supported_version":
            print_path_red(f"{section.replace('_', ' ').capitalize()}:", contents)
        else:
            print_red_bold(f"\n{section.replace('-', ' ').capitalize()}: ")
            for item in contents:
                print(f"	{item}")
