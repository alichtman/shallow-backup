import os
import shutil
import pytest
from shallow_backup import git_add_all_commit, git_init_if_needed, create_gitignore_if_needed

BACKUP_DIR = 'shallow-backup-test-git-backup-dir'


class TestGitFunctionality:
    """
    Test the git functionality
    """

    def setup_method(self):
        try:
            os.mkdir(BACKUP_DIR)
        except FileExistsError:
            shutil.rmtree(BACKUP_DIR)
            os.mkdir(BACKUP_DIR)

    def teardown_method(self):
        shutil.rmtree(BACKUP_DIR)

    def test_directory_can_be_git_initialized(self):
        assert not os.path.isdir(os.path.join(BACKUP_DIR, '.git/'))
        git_init_if_needed(BACKUP_DIR)
        assert os.path.isdir(os.path.join(BACKUP_DIR, '.git/'))

    def test_commiting_works_for_git_repo(self):
        file_of_commits = os.path.join(BACKUP_DIR, 'default/.git/logs/refs/heads/master')
        assert not os.path.isfile(file_of_commits)
        repo = git_init_if_needed(BACKUP_DIR)
        create_gitignore_if_needed(BACKUP_DIR)
        git_add_all_commit(repo, BACKUP_DIR)
        assert os.path.isfile(file_of_commits)




