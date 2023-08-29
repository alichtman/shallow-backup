import os
import shutil
import sys

sys.path.insert(0, "../shallow_backup")
from shallow_backup.config import safe_create_config


def setup_env_vars():
    os.environ["SHALLOW_BACKUP_TEST_BACKUP_DIR"] = (
        os.path.abspath(BASE_TEST_DIR) + "/backup"
    )
    os.environ["SHALLOW_BACKUP_TEST_HOME_DIR"] = (
        os.path.abspath(BASE_TEST_DIR) + "/home"
    )
    # This env var is referenced in shallow_backup/config.py
    os.environ["SHALLOW_BACKUP_TEST_CONFIG_PATH"] = (
        os.path.abspath(BASE_TEST_DIR) + "/shallow-backup.conf"
    )


def unset_env_vars():
    del os.environ["SHALLOW_BACKUP_TEST_BACKUP_DIR"]
    del os.environ["SHALLOW_BACKUP_TEST_HOME_DIR"]
    del os.environ["SHALLOW_BACKUP_TEST_CONFIG_PATH"]


def create_config_for_test():
    config_file = os.environ["SHALLOW_BACKUP_TEST_CONFIG_PATH"]
    if os.path.isfile(config_file):
        os.remove(config_file)
    safe_create_config()


def create_dir_overwrite(directory):
    if os.path.isdir(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def setup_dirs_and_env_vars_and_create_config():
    setup_env_vars()
    create_config_for_test()
    for directory in DIRS:
        create_dir_overwrite(directory)


def clean_up_dirs_and_env_vars():
    shutil.rmtree(BASE_TEST_DIR)
    unset_env_vars()


# TODO: Update to tempfile and tempdir because testing in the home directory is so stupid.

# These globals must remain at the bottom of this file for some reason
# This global is required to be set for the setup_env_vars call to work properly.
BASE_TEST_DIR = os.path.expanduser("~") + "/SHALLOW-BACKUP-TEST-DIRECTORY"
setup_env_vars()
BACKUP_DEST_DIR = os.environ.get("SHALLOW_BACKUP_TEST_BACKUP_DIR")
FAKE_HOME_DIR = os.environ.get("SHALLOW_BACKUP_TEST_HOME_DIR")
DIRS = [BACKUP_DEST_DIR, FAKE_HOME_DIR]

DOTFILES = [
    os.path.join(FAKE_HOME_DIR, ".ssh/"),
    os.path.join(FAKE_HOME_DIR, ".config/git/"),
    os.path.join(FAKE_HOME_DIR, ".zshenv"),
    os.path.join(FAKE_HOME_DIR, ".pypirc"),
    os.path.join(FAKE_HOME_DIR, ".config/nvim/init.vim"),
    os.path.join(FAKE_HOME_DIR, ".config/zsh/.zshrc"),
]
