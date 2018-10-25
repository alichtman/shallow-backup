import os
import pytest
import shutil
from shallow_backup.utils import copy_dir

DIR_TO_BACKUP = 'shallow-backup-test-copy-dir'
BACKUP_DIR = 'shallow-backup-test-copy-backup-dir'
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
        for directory in DIRS:
            shutil.rmtree(directory)
        os.remove(TEST_TEXT_FILE)

    def test_copy_dir(self):
        """
        Test that copying a directory works as expected
        """
        # TODO: Test that all subfiles and folders are copied.
        test_dir = 'test/'
        test_path = os.path.join(DIR_TO_BACKUP, test_dir)
        os.mkdir(test_path)
        copy_dir(test_path, BACKUP_DIR)
        assert os.path.isdir(test_path)
        assert os.path.isdir(os.path.join(BACKUP_DIR, test_dir))

    @pytest.mark.parametrize('invalid', {".Trash", ".npm", ".cache", ".rvm"})
    def test_copy_dir_invalid(self, invalid):
        """
        Test that attempting to copy an invalid directory fails
        """
        copy_dir(invalid, DIR_TO_BACKUP)
        assert not os.path.isdir(os.path.join(BACKUP_DIR, invalid))
