import os
import sys
from .testing_utility_functions import (
    BACKUP_DEST_DIR,
    FAKE_HOME_DIR,
    clean_up_dirs_and_env_vars,
    setup_dirs_and_env_vars_and_create_config,
)

sys.path.insert(0, "../shallow_backup")
from shallow_backup.git_wrapper import move_git_repo, safe_git_init, create_gitignore


class TestGitFolderCopying:
    """
    Test the functionality of .git copying
    """

    @staticmethod
    def setup_method():
        setup_dirs_and_env_vars_and_create_config()

    @staticmethod
    def teardown_method():
        clean_up_dirs_and_env_vars()

    def test_copy_git_folder(self):
        """
        Test copying the .git folder and .gitignore from an old directory to a new one
        """
        safe_git_init(FAKE_HOME_DIR)
        create_gitignore(FAKE_HOME_DIR, "root-gitignore")
        move_git_repo(FAKE_HOME_DIR, BACKUP_DEST_DIR)
        assert os.path.isdir(os.path.join(BACKUP_DEST_DIR, ".git/"))
        assert os.path.isfile(os.path.join(BACKUP_DEST_DIR, ".gitignore"))
        assert not os.path.isdir(os.path.join(FAKE_HOME_DIR, ".git/"))
        assert not os.path.isfile(os.path.join(FAKE_HOME_DIR, ".gitignore"))
