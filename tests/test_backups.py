import os
import sys
from pathlib import Path
from .testing_utility_functions import (
    BACKUP_DEST_DIR,
    FAKE_HOME_DIR,
    DOTFILES,
    setup_dirs_and_env_vars_and_create_config,
    clean_up_dirs_and_env_vars,
)

sys.path.insert(0, "../shallow_backup")
from shallow_backup.backup import backup_dotfiles
from shallow_backup.utils import safe_mkdir
from shallow_backup.config import get_config, write_config

TEST_TEXT_CONTENT = "THIS IS TEST CONTENT FOR THE DOTFILES"


class TestBackupMethods:
    """Test the backup methods."""

    @staticmethod
    def setup_method():
        setup_dirs_and_env_vars_and_create_config()

        # Create all dotfiles and dotfolders
        for file in DOTFILES:
            if not file.endswith("/"):
                print(f"Creating file: {file}")
                os.makedirs(Path(file).parent, exist_ok=True)
                with open(file, "w+") as f:
                    f.write(TEST_TEXT_CONTENT)
            else:
                directory = file
                print(f"Creating dir: {directory}")
                safe_mkdir(directory)
                for file_2 in ["test1", "test2"]:
                    with open(os.path.join(directory, file_2), "w+") as f:
                        f.write(TEST_TEXT_CONTENT)

    @staticmethod
    def teardown_method():
        clean_up_dirs_and_env_vars()

    def test_backup_dotfiles(self):
        """Test backing up dotfiles and dotfolders."""
        backup_dest_path = os.path.join(BACKUP_DEST_DIR, "dotfiles")
        backup_dotfiles(
            backup_dest_path, dry_run=False, home_path=FAKE_HOME_DIR, skip=True
        )
        assert os.path.isdir(backup_dest_path)
        for path in DOTFILES:
            print(
                f"\nBACKUP DESTINATION DIRECTORY: ({backup_dest_path}) CONTENTS:",
                os.listdir(backup_dest_path),
                "",
            )
            print(path + " should already be backed up.")
            backed_up_dot = os.path.join(
                backup_dest_path, path.replace(FAKE_HOME_DIR + "/", "")
            )
            print(f"Backed up dot: {backed_up_dot}\n")
            assert os.path.isfile(backed_up_dot) or os.path.isdir(backed_up_dot)

    def test_conditions(self):
        """Test backing up files based on conditions"""
        # Set false backup condition of all files.
        config = get_config()
        print(config["dotfiles"])
        for dot, _ in config["dotfiles"].items():
            config["dotfiles"][dot][
                "backup_condition"
            ] = "[[ $(uname -s) == 'Made Up OS' ]]"
        write_config(config)

        backup_dest_path = os.path.join(BACKUP_DEST_DIR, "dotfiles")
        backup_dotfiles(
            backup_dest_path, dry_run=False, home_path=FAKE_HOME_DIR, skip=True
        )
        assert os.path.isdir(backup_dest_path)
        for path in DOTFILES:
            print(
                f"\nBACKUP DESTINATION DIRECTORY: ({backup_dest_path}) CONTENTS:",
                os.listdir(backup_dest_path),
                "",
            )
            print(path + " should not be backed up.")
            backed_up_dot = os.path.join(
                backup_dest_path, path.replace(FAKE_HOME_DIR + "/", "")
            )
            assert not (os.path.isfile(backed_up_dot) or os.path.isdir(backed_up_dot))
