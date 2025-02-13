import os
import sys
import json
import stat
from os import path, environ, chmod
from .printing import *
from .compatibility import *
from .utils import safe_mkdir, strip_home
from .constants import ProjInfo
from functools import lru_cache


def get_xdg_config_path() -> str:
    """Returns path to $SHALLOW_BACKUP_CONFIG_DIR (if set), $XDG_CONFIG_HOME, or ~/.config if none of those exist."""
    return environ.get("SHALLOW_BACKUP_CONFIG_DIR") or environ.get("XDG_CONFIG_HOME") or path.join(path.expanduser("~"), ".config")


@lru_cache(maxsize=1)
def get_config_path() -> str:
    """
    Detects if in testing or prod env, and returns the right config path.
    :return: Path to config.
    """
    test_config_path = environ.get("SHALLOW_BACKUP_TEST_CONFIG_PATH", None)
    legacy_config_path = path.join(get_xdg_config_path(), "shallow-backup.conf")
    new_config_path = path.join(get_xdg_config_path(), "shallow-backup.json")
    if test_config_path:
        return test_config_path
    elif path.exists(legacy_config_path):
        return legacy_config_path
    else:
        return new_config_path


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


def edit_config():
    """
    Open the config in the default editor
    """
    config_path = get_config_path()
    editor = os.environ.get("EDITOR", "vim")
    os.system(f"{editor} {config_path}")
