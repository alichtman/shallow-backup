import os
import sys
from .testing_utility_functions import (
    setup_dirs_and_env_vars_and_create_config,
    clean_up_dirs_and_env_vars,
    FAKE_HOME_DIR,
)

sys.path.insert(0, "../shallow_backup")
from shallow_backup.config import (
    get_config,
    get_config_path,
    add_dot_path_to_config,
    check_insecure_config_permissions,
)
from shallow_backup.utils import strip_home


class TestConfigMethods:
    """Test the config methods."""

    @staticmethod
    def setup_method():
        setup_dirs_and_env_vars_and_create_config()

    @staticmethod
    def teardown_method():
        clean_up_dirs_and_env_vars()

    def test_add_path(self):
        config = get_config()
        home_path = os.path.expanduser("~")
        invalid_path = "some_random_nonexistent_path"
        path_to_add = os.path.join(home_path, invalid_path)
        new_config = add_dot_path_to_config(config, path_to_add)
        assert strip_home(invalid_path) not in new_config["dotfiles"]

        valid_path = "valid"
        path_to_add = os.path.join(FAKE_HOME_DIR, valid_path)
        os.mkdir(path_to_add)
        new_config = add_dot_path_to_config(config, path_to_add)
        from pprint import pprint

        pprint(new_config)
        stripped_home_path = strip_home(path_to_add)
        assert stripped_home_path in new_config["dotfiles"]
        assert isinstance(new_config["dotfiles"][stripped_home_path], dict)

    def test_detect_insecure_config_permissions(self):
        print(f"Testing config path: {get_config_path()}")
        os.chmod(get_config_path(), 0o777)
        assert check_insecure_config_permissions() == True

    def test_secure_config_created_by_default(self):
        print(f"Testing config path: {get_config_path()}")
        assert check_insecure_config_permissions() == False
