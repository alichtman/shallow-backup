import unittest
import os
import shutil
from shallow_backup import _copy_file, copy_dir

TEST_DIR = 'test-directory'
TEST_BACKUP_DIR = 'test-backup-dir'
TEST_TEXT_FILE = 'test-file.txt'
DIRS = [TEST_DIR, TEST_BACKUP_DIR]


class TestCopyMethods(unittest.TestCase):
    """
    Test the functionality of copying
    """

    def setUp(self):
        for directory in DIRS:
            try:
                os.mkdir(directory)
            except FileExistsError:
                shutil.rmtree(directory)
                os.mkdir(directory)
        f = open(TEST_TEXT_FILE, "w+")
        f.close()

    def tearDown(self):
        shutil.rmtree(TEST_DIR)
        os.remove(TEST_TEXT_FILE)

    def test_copy_file(self):
        """
        Test that copying a file is working as expected
        """
        process =_copy_file(TEST_TEXT_FILE, TEST_DIR)
        assert process.returncode == 0
        assert os.path.isfile(TEST_TEXT_FILE)
        assert os.path.isfile(TEST_DIR + '/' + TEST_TEXT_FILE)

    def test_copy_dir(self):
        """
        Test that copying a directory works as expected
        """
        dir_to_copy = '/test/'
        os.mkdir(TEST_DIR + dir_to_copy)
        process = copy_dir(TEST_DIR + dir_to_copy, TEST_BACKUP_DIR)
        assert process.returncode == 0
        assert os.path.isdir(TEST_DIR + dir_to_copy)
        assert os.path.isdir(TEST_BACKUP_DIR + dir_to_copy)

    def test_copy_dir_invalid(self):
        """
        Test that attempting to copy an invalid directory fails
        """
        invalids = [".Trash", ".npm", ".cache", ".rvm"]
        for invalid in invalids:
            process = copy_dir(invalid, TEST_DIR)
            assert process is None
