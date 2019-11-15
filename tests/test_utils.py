import os
import sys
sys.path.insert(0, "../shallow_backup")
from shallow_backup.config import safe_create_config


def setup_env_vars():
	os.environ["SHALLOW_BACKUP_TEST_DEST_DIR"] = "/tmp/shallow-backup-test-dest-dir"
	os.environ["SHALLOW_BACKUP_TEST_SOURCE_DIR"] = "/tmp/shallow-backup-test-source-dir"
	os.environ["SHALLOW_BACKUP_TEST_CONFIG_PATH"] = "/tmp/shallow-backup.conf"


def unset_env_vars():
	del os.environ["SHALLOW_BACKUP_TEST_DEST_DIR"]
	del os.environ["SHALLOW_BACKUP_TEST_SOURCE_DIR"]
	del os.environ["SHALLOW_BACKUP_TEST_CONFIG_PATH"]


def create_config_for_test():
	config_file = os.environ["SHALLOW_BACKUP_TEST_CONFIG_PATH"]
	if os.path.isfile(config_file):
		os.remove(config_file)
	safe_create_config()


setup_env_vars()
BACKUP_DEST_DIR = os.environ.get("SHALLOW_BACKUP_TEST_DEST_DIR")
FAKE_HOME_DIR = os.environ.get("SHALLOW_BACKUP_TEST_SOURCE_DIR")
DIRS = [BACKUP_DEST_DIR, FAKE_HOME_DIR]

DOTFILES = [
	os.path.join(FAKE_HOME_DIR, ".bashrc"),
	os.path.join(FAKE_HOME_DIR, ".bash_profile"),
	os.path.join(FAKE_HOME_DIR, ".gitconfig"),
	os.path.join(FAKE_HOME_DIR, ".profile"),
	os.path.join(FAKE_HOME_DIR, ".pypirc"),
	os.path.join(FAKE_HOME_DIR, ".vimrc"),
	os.path.join(FAKE_HOME_DIR, ".zshrc")
]

DOTFOLDERS = [
	os.path.join(FAKE_HOME_DIR, ".ssh"),
	os.path.join(FAKE_HOME_DIR, ".vim")
]
