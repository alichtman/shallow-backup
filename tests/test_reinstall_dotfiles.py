import os
import sys
from .testing_utility_functions import (
    FAKE_HOME_DIR,
    setup_dirs_and_env_vars_and_create_config,
    clean_up_dirs_and_env_vars,
)

sys.path.insert(0, "../shallow_backup")
from shallow_backup.reinstall import reinstall_dots_sb

TEST_TEXT_CONTENT = "THIS IS TEST CONTENT FOR THE DOTFILES"
DOTFILES_PATH = os.path.join(FAKE_HOME_DIR, "dotfiles/")


class TestReinstallDotfiles:
    """
    Test the functionality of reinstalling dotfiles
    """

    @staticmethod
    def setup_method():
        def create_nested_dir(parent, name):
            new_dir = os.path.join(parent, name)
            print(f"Creating {new_dir}")
            if not os.path.isdir(new_dir):
                os.makedirs(new_dir)
            return new_dir

        def create_file(parent, name):
            file = os.path.join(parent, name)
            print(f"Creating {file}")
            with open(file, "w+") as f:
                f.write(TEST_TEXT_CONTENT)

        def create_git_dir(parent):
            git_dir = create_nested_dir(parent, ".git/")
            git_objects = create_nested_dir(git_dir, "objects/")
            create_file(git_dir, "config")
            create_file(git_objects, "obj1")
            return git_dir

        setup_dirs_and_env_vars_and_create_config()

        # Dotfiles / dirs to NOT reinstall
        create_git_dir(DOTFILES_PATH)  # Should NOT reinstall DOTFILES_PATH/.git
        img_dir_should_not_reinstall = create_nested_dir(DOTFILES_PATH, "img")
        create_file(img_dir_should_not_reinstall, "test.png")
        create_file(DOTFILES_PATH, "README.md")
        create_file(DOTFILES_PATH, ".gitignore")

        # Dotfiles / dirs to reinstall
        testfolder = create_nested_dir(DOTFILES_PATH, ".config/tmux/")
        testfolder2 = create_nested_dir(testfolder, "testfolder2/")
        create_file(testfolder2, "test.sh")
        create_git_dir(testfolder2)
        git_config = create_nested_dir(DOTFILES_PATH, ".config/git")
        create_file(git_config, "test")
        create_file(testfolder2, ".gitignore")
        create_file(DOTFILES_PATH, ".zshenv")

    @staticmethod
    def teardown_method():
        clean_up_dirs_and_env_vars()

    def test_reinstall_dotfiles(self):
        """
        Test reinstalling dotfiles to fake home dir
        """
        reinstall_dots_sb(
            dots_path=DOTFILES_PATH, home_path=FAKE_HOME_DIR, dry_run=False
        )
        assert os.path.isfile(os.path.join(FAKE_HOME_DIR, ".zshenv"))
        testfolder2 = os.path.join(
            os.path.join(FAKE_HOME_DIR, ".config/tmux/"), "testfolder2"
        )
        assert os.path.isdir(testfolder2)
        assert os.path.isfile(os.path.join(testfolder2, "test.sh"))
        assert os.path.isdir(os.path.join(FAKE_HOME_DIR, ".config/git/"))

        # Do reinstall other git files
        assert os.path.isdir(os.path.join(testfolder2, ".git"))
        assert os.path.isfile(os.path.join(testfolder2, ".gitignore"))

        # Don't reinstall root-level git files
        assert not os.path.isdir(os.path.join(FAKE_HOME_DIR, ".git"))
        assert not os.path.isfile(os.path.join(FAKE_HOME_DIR, ".gitignore"))

        # Don't reinstall img or README.md
        assert not os.path.isdir(os.path.join(FAKE_HOME_DIR, "img"))
        assert not os.path.isfile(os.path.join(FAKE_HOME_DIR, "README.md"))
