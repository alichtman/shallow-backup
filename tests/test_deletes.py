import os
import sys
import shutil
sys.path.insert(0, "../shallow_backup")
from shallow_backup.utils import destroy_backup_dir

BACKUP_DIR = 'shallow-backup-test-copy-backup-dir'
TEST_BACKUP_TEXT_FILE = os.path.join(BACKUP_DIR, 'test-file.txt')
DIRS = [BACKUP_DIR]


class TestDeleteMethods:
    """
    Test the functionality of deleting
    """

    @staticmethod
    def setup_method():
        for directory in DIRS:
            try:
                os.mkdir(directory)
            except FileExistsError:
                shutil.rmtree(directory)
                os.mkdir(directory)
        f = open(TEST_BACKUP_TEXT_FILE, "w+")
        f.close()

    @staticmethod
    def teardown_method():
        for directory in DIRS:
            try:
                shutil.rmtree(directory)
            except OSError:
                pass

    def test_clean_an_existing_backup_directory(self):
        """
        Test that deleting the backup directory works as expected
        """
        assert os.path.isdir(BACKUP_DIR)
        assert os.path.isfile(TEST_BACKUP_TEXT_FILE)
        destroy_backup_dir(BACKUP_DIR)
        assert not os.path.isdir(BACKUP_DIR)
        assert not os.path.isfile(TEST_BACKUP_TEXT_FILE)

    def test_can_handle_cleaning_non_existing_backup_directory(self):
        """
        Test that we exit gracefully when cleaning an non existing backup directory
        """
        nonexist_backup_dir = BACKUP_DIR + "-dummy"
        assert not os.path.isdir(nonexist_backup_dir)
        destroy_backup_dir(nonexist_backup_dir)
        assert not os.path.isdir(nonexist_backup_dir)
