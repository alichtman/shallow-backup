import os
import sys
import shutil
from .test_utils import FAKE_HOME_DIR, DIRS, setup_env_vars, create_config_for_test
sys.path.insert(0, "../shallow_backup")
from shallow_backup.reinstall import reinstall_dots_sb

TEST_TEXT_CONTENT = 'THIS IS TEST CONTENT FOR THE DOTFILES'
DOTFILES_PATH = os.path.join(FAKE_HOME_DIR, "dotfiles/")


class TestReinstallDotfiles:
    """
    Test the functionality of reinstalling dotfiles
    """

    @staticmethod
    def setup_method():

        def create_dir(parent, name):
            new_dir = os.path.join(parent, name)
            print(f"Creating {new_dir}")
            os.mkdir(new_dir)
            return new_dir

        def create_file(parent, name):
            file = os.path.join(parent, name)
            print(f"Creating {file}")
            with open(file, "w+") as f:
                f.write(TEST_TEXT_CONTENT)

        def create_git_dir(parent):
            git_dir = create_dir(parent, ".git/")
            git_objects = create_dir(git_dir, "objects/")
            create_file(git_dir, "config")
            create_file(git_objects, "obj1")
            return git_dir


        setup_env_vars()
        create_config_for_test()
        for directory in DIRS:
            try:
                os.mkdir(directory)
            except FileExistsError:
                shutil.rmtree(directory)
                os.mkdir(directory)

        # SAMPLE DOTFILES FOLDER PATH
        try:
            os.mkdir(DOTFILES_PATH)
        except FileExistsError:
            shutil.rmtree(DOTFILES_PATH)
            os.mkdir(DOTFILES_PATH)

        # SAMPLE SUBFOLDER IN DOTFILES PATH
        testfolder = create_dir(DOTFILES_PATH, "testfolder1/")
        testfolder2 = create_dir(testfolder, "testfolder2/")

        git_dir_should_not_reinstall = create_git_dir(DOTFILES_PATH)
        git_dir_should_reinstall = create_git_dir(testfolder2)

        # SAMPLE DOTFILES TO REINSTALL
        create_file(testfolder2, ".testsubfolder_rc1")
        create_file(testfolder2, ".gitignore")
        create_file(DOTFILES_PATH, ".gitignore")
        create_file(testfolder2, ".testsubfolder_rc2")
        create_file(DOTFILES_PATH, ".testrc")

    @staticmethod
    def teardown_method():
        for directory in DIRS:
            shutil.rmtree(directory)

    def test_reinstall_dotfiles(self):
        """
        Test resintalling dotfiles to fake home dir
        """
        reinstall_dots_sb(DOTFILES_PATH, home_path=FAKE_HOME_DIR)
        assert os.path.isfile(os.path.join(FAKE_HOME_DIR, '.testrc'))
        testfolder2 = os.path.join(os.path.join(FAKE_HOME_DIR, 'testfolder1'), 'testfolder2')
        assert os.path.isdir(testfolder2)
        assert os.path.isfile(os.path.join(testfolder2, '.testsubfolder_rc1'))
        assert os.path.isfile(os.path.join(testfolder2, '.testsubfolder_rc2'))

        # Don't reinstall root-level git files
        assert not os.path.isdir(os.path.join(FAKE_HOME_DIR, ".git"))
        assert not os.path.isfile(os.path.join(FAKE_HOME_DIR, ".gitignore"))
        # Do reinstall all other git files
        assert os.path.isdir(os.path.join(testfolder2, ".git"))
        assert os.path.isfile(os.path.join(testfolder2, ".gitignore"))
