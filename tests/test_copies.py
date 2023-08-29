import os
import sys
import pytest
from .testing_utility_functions import (
    clean_up_dirs_and_env_vars,
    BACKUP_DEST_DIR,
    FAKE_HOME_DIR,
    create_dir_overwrite,
    setup_env_vars,
    create_config_for_test,
)

sys.path.insert(0, "../shallow_backup")
from shallow_backup.utils import copy_dir_if_valid


class TestCopyMethods:
    """
    Test the functionality of copying
    """

    @staticmethod
    def setup_method():
        setup_env_vars()
        create_config_for_test()
        create_dir_overwrite(FAKE_HOME_DIR)

    @staticmethod
    def teardown_method():
        clean_up_dirs_and_env_vars()

    def test_copy_dir(self):
        """
        Test that copying a directory works as expected
        """
        # TODO: Test that all subfiles and folders are copied.
        test_file_name = "test-file.txt"
        test_dir_name = "subdir-to-copy"
        os.mkdir(os.path.join(FAKE_HOME_DIR, test_dir_name))
        with open(os.path.join(FAKE_HOME_DIR, test_file_name), "w+") as file:
            file.write("TRASH")

        copy_dir_if_valid(FAKE_HOME_DIR, BACKUP_DEST_DIR)
        assert os.path.isfile(os.path.join(BACKUP_DEST_DIR, test_file_name))
        assert os.path.isdir(os.path.join(BACKUP_DEST_DIR, test_dir_name))

    @pytest.mark.parametrize("invalid", {".Trash", ".npm", ".cache", ".rvm"})
    def test_copy_dir_invalid(self, invalid):
        """
        Test that attempting to copy an invalid directory fails
        """
        copy_dir_if_valid(invalid, FAKE_HOME_DIR)
        assert not os.path.isdir(os.path.join(BACKUP_DEST_DIR, invalid))
