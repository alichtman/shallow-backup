import os
import sys
import pytest
import shutil
from .test_utils import setup_env_vars, unset_env_vars, BACKUP_DEST_DIR, FAKE_HOME_DIR, DIRS
sys.path.insert(0, "../shallow_backup")
from shallow_backup.utils import copy_dir_if_valid

TEST_TEXT_FILE = os.path.join(FAKE_HOME_DIR, 'test-file.txt')


class TestCopyMethods:
    """
    Test the functionality of copying
    """

    @staticmethod
    def setup_method():
        setup_env_vars()
        try:
            os.mkdir(FAKE_HOME_DIR)
        except FileExistsError:
            shutil.rmtree(FAKE_HOME_DIR)
            os.mkdir(FAKE_HOME_DIR)
        print(f"Created {TEST_TEXT_FILE}")
        open(TEST_TEXT_FILE, "w+").close()

    @staticmethod
    def teardown_method():
        for directory in DIRS:
            if os.path.isdir(directory):
                shutil.rmtree(directory)
        unset_env_vars()

    def test_copy_dir(self):
        """
        Test that copying a directory works as expected
        """
        # TODO: Test that all subfiles and folders are copied.
        test_dir = 'subdir-to-copy'
        test_path = os.path.join(FAKE_HOME_DIR, test_dir)
        os.mkdir(test_path)
        copy_dir_if_valid(FAKE_HOME_DIR, BACKUP_DEST_DIR)
        assert os.path.isdir(test_path)
        assert os.path.isfile(os.path.join(BACKUP_DEST_DIR, os.path.split(TEST_TEXT_FILE)[1]))
        assert os.path.isdir(os.path.join(BACKUP_DEST_DIR, test_dir))

    @pytest.mark.parametrize('invalid', {".Trash", ".npm", ".cache", ".rvm"})
    def test_copy_dir_invalid(self, invalid):
        """
        Test that attempting to copy an invalid directory fails
        """
        copy_dir_if_valid(invalid, FAKE_HOME_DIR)
        assert not os.path.isdir(os.path.join(BACKUP_DEST_DIR, invalid))
