import os
import sys
from .testing_utility_functions import (
    FAKE_HOME_DIR,
    clean_up_dirs_and_env_vars,
    setup_dirs_and_env_vars_and_create_config,
)

sys.path.insert(0, "../shallow_backup")
from shallow_backup.utils import destroy_backup_dir

TEST_BACKUP_TEXT_FILE = os.path.join(FAKE_HOME_DIR, "test-file.txt")


class TestDeleteMethods:
    """
    Test the functionality of deleting
    """

    @staticmethod
    def setup_method():
        setup_dirs_and_env_vars_and_create_config()
        with open(TEST_BACKUP_TEXT_FILE, "w+") as file:
            file.write("RANDOM TEXT")

    @staticmethod
    def teardown_method():
        clean_up_dirs_and_env_vars()

    def test_clean_an_existing_backup_directory(self):
        """
        Test that deleting the backup directory works as expected
        """
        assert os.path.isdir(FAKE_HOME_DIR)
        assert os.path.isfile(TEST_BACKUP_TEXT_FILE)
        destroy_backup_dir(FAKE_HOME_DIR)
        assert not os.path.isdir(FAKE_HOME_DIR)
        assert not os.path.isfile(TEST_BACKUP_TEXT_FILE)

    def test_can_handle_cleaning_non_existing_backup_directory(self):
        """
        Test that we exit gracefully when cleaning an non existing backup directory
        """
        nonexist_backup_dir = os.path.join(FAKE_HOME_DIR, "NON-EXISTENT")
        assert not os.path.isdir(nonexist_backup_dir)
        destroy_backup_dir(nonexist_backup_dir)
        assert not os.path.isdir(nonexist_backup_dir)
