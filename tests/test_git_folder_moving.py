import os
import shutil
from shallow_backup.git_wrapper import move_git_dir_to_path, safe_git_init, safe_create_gitignore
from shallow_backup.config import create_config_file_if_needed

OLD_BACKUP_DIR = 'shallow-backup-test-git-old-backup-dir'
NEW_BACKUP_DIR = 'shallow-backup-test-git-new-backup-backup-dir'
DIRS = [OLD_BACKUP_DIR, NEW_BACKUP_DIR]


class TestGitFolderCopying:
    """
    Test the functionality of .git copying
    """

    @staticmethod
    def setup_method():
        create_config_file_if_needed()
        for directory in DIRS:
            try:
                os.mkdir(directory)
            except FileExistsError:
                shutil.rmtree(directory)
                os.mkdir(directory)

    @staticmethod
    def teardown_method():
        for directory in DIRS:
            shutil.rmtree(directory)

    def test_copy_git_folder(self):
        """
        Test copying the .git folder and .gitignore from an old directory to a new one
        """
        safe_git_init(OLD_BACKUP_DIR)
        safe_create_gitignore(OLD_BACKUP_DIR)
        move_git_dir_to_path(OLD_BACKUP_DIR, NEW_BACKUP_DIR)
        assert os.path.isdir(os.path.join(NEW_BACKUP_DIR, '.git/'))
        assert os.path.isfile(os.path.join(NEW_BACKUP_DIR, '.gitignore'))
        assert not os.path.isdir(os.path.join(OLD_BACKUP_DIR, '.git/'))
        assert not os.path.isfile(os.path.join(OLD_BACKUP_DIR, '.gitignore'))
