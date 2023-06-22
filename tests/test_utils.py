import sys
from .testing_utility_functions import setup_env_vars, unset_env_vars

sys.path.insert(0, "../shallow_backup")
from shallow_backup.utils import run_cmd_return_bool


class TestUtilMethods:
    """
    Test the functionality of utils
    """

    @staticmethod
    def setup_method():
        setup_env_vars()

    @staticmethod
    def teardown_method():
        unset_env_vars()

    def test_run_cmd_return_bool(self):
        """Test that evaluating bash commands to get booleans works as expected"""

        # Basic bash conditionals with command substitution
        should_fail = "[[ -z $(uname -s) ]]"
        assert run_cmd_return_bool(should_fail) is False

        should_pass = "[[ -n $(uname -s) ]]"
        assert run_cmd_return_bool(should_pass) is True

        # Using env vars
        should_pass = '[[ -n "$SHALLOW_BACKUP_TEST_BACKUP_DIR" ]]'
        assert run_cmd_return_bool(should_pass) is True

        should_pass = "[[ -n $SHALLOW_BACKUP_TEST_BACKUP_DIR ]]"
        assert run_cmd_return_bool(should_pass) is True
