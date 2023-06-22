import sys
from .config import get_config
from .printing import print_red_bold, print_red
from .constants import ProjInfo


def check_if_config_upgrade_needed():
    """Checks if a config is supported by the current version of shallow-backup"""
    config = get_config()
    # If this key is not in the config, that means the config was installed pre-v5.0.0a
    if "lowest_supported_version" not in config:
        print_red_bold(
            f"ERROR: Config version detected as incompatible with current shallow-backup version ({ProjInfo.VERSION})."
        )
        print_red("There are two possible fixes.")
        print_red(
            "1. Backup your config file to another location and remove the original config."
        )
        print_red("\tshallow-backup will recreate a compatible config on the next run.")
        print_red("\tYou can then add in your custom backup paths manually.")
        print_red("2. Manually upgrade the config.")
        print_red_bold(
            "Please downgrade to a version of shallow-backup before v5.0.0a if you do not want to upgrade your config."
        )
        sys.exit()
