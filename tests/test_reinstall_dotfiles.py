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
        try:
            os.mkdir(os.path.join(DOTFILES_PATH, "testfolder"))
        except FileExistsError:
            shutil.rmtree(os.path.join(DOTFILES_PATH, "testfolder"))
            os.mkdir(os.path.join(DOTFILES_PATH, "testfolder"))

        # SAMPLE DOTFILE TO REINSTALL
        file = os.path.join(DOTFILES_PATH, ".testrc")
        print(f"Creating {file}")
        with open(file, "w+") as f:
            f.write(TEST_TEXT_CONTENT)

    @staticmethod
    def teardown_method():
        for directory in DIRS:
            shutil.rmtree(directory)

    def test_reinstall_dotfiles(self):
        """
        Test resintalling dotfile to fake home dir
        """
        reinstall_dots_sb(DOTFILES_PATH,home_path=FAKE_HOME_DIR)
        assert os.path.isfile(os.path.join(FAKE_HOME_DIR, '.testrc'))
        assert os.path.isdir(os.path.join(FAKE_HOME_DIR, 'testfolder/'))