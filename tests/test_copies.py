import os
import pytest
import shutil
from shallow_backup import _copy_file, _copy_dir
from constants import Constants

DIR_TO_BACKUP = 'shallow-backup-test-dir'
BACKUP_DIR = 'shallow-backup-test-backup-dir'
TEST_TEXT_FILE = 'test-file.txt'
DIRS = [DIR_TO_BACKUP, BACKUP_DIR]


class TestCopyMethods:
    """
    Test the functionality of copying
    """

    def setup_method(self):
        for directory in DIRS:
            try:
                os.mkdir(directory)
            except FileExistsError:
                shutil.rmtree(directory)
                os.mkdir(directory)
        f = open(TEST_TEXT_FILE, "w+")
        f.close()

    def teardown_method(self):
        shutil.rmtree(DIR_TO_BACKUP)
        shutil.rmtree(BACKUP_DIR)
        os.remove(TEST_TEXT_FILE)

    def test_copy_file(self):
        """
        Test that copying a file is working as expected
        """
        # TODO: Test that the files are the same.
        process =_copy_file(TEST_TEXT_FILE, BACKUP_DIR)
        assert process.returncode == 0
        assert os.path.isfile(TEST_TEXT_FILE)
        assert os.path.isfile(os.path.join(BACKUP_DIR, TEST_TEXT_FILE))

    def test_copy_dir(self):
        """
        Test that copying a directory works as expected
        """
        # TODO: Test that all subfiles and folders are copied.
        test_dir = 'test/'
        test_path = os.path.join(DIR_TO_BACKUP, test_dir)
        os.mkdir(test_path)
        process = _copy_dir(test_path, BACKUP_DIR)
        assert process.returncode == 0
        assert os.path.isdir(test_path)
        assert os.path.isdir(os.path.join(BACKUP_DIR, test_dir))

    @pytest.mark.parametrize('invalid', Constants.INVALID_DIRS)
    def test_copy_dir_invalid(self, invalid):
        """
        Test that attempting to copy an invalid directory fails
        """
        process = _copy_dir(invalid, DIR_TO_BACKUP)
        assert process is None
