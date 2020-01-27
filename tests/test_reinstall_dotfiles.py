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
        testfolder = os.path.join(DOTFILES_PATH, "testfolder1/")
        print(f"Creating {testfolder}")
        os.mkdir(testfolder)

        testfolder2 = os.path.join(testfolder, "testfolder2/")
        print(f"Creating {testfolder2}")
        os.mkdir(testfolder2)

        # SAMPLE DOTFILES TO REINSTALL
        file = os.path.join(testfolder2, ".testsubfolder_rc1")
        print(f"Creating {file}")
        with open(file, "w+") as f:
            f.write(TEST_TEXT_CONTENT)

        file = os.path.join(testfolder2, ".testsubfolder_rc2")
        print(f"Creating {file}")
        with open(file, "w+") as f:
            f.write(TEST_TEXT_CONTENT)

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
        Test resintalling dotfiles to fake home dir
        """
        reinstall_dots_sb(DOTFILES_PATH, home_path=FAKE_HOME_DIR)
        assert os.path.isfile(os.path.join(FAKE_HOME_DIR, '.testrc'))
        testfolder2 = os.path.join(os.path.join(FAKE_HOME_DIR, 'testfolder1'), 'testfolder2')
        assert os.path.isdir(testfolder2)
        assert os.path.isfile(os.path.join(testfolder2, '.testsubfolder_rc1'))
        assert os.path.isfile(os.path.join(testfolder2, '.testsubfolder_rc2'))
