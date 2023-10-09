import click
from .backup import *
from .prompts import *
from .reinstall import *
from .git_wrapper import *
from .utils import (
    mkdir_warn_overwrite,
    destroy_backup_dir,
    expand_to_abs_path,
    check_if_path_is_valid_dir,
)
from .config import *
from .upgrade import check_if_config_upgrade_needed


# custom help options
@click.command(context_settings=dict(help_option_names=["-h", "-help", "--help"]))
@click.option(
    "--add-dot", default=None, help="Add a dotfile or dotfolder to config by path."
)
@click.option(
    "--backup-all", "backup_all_flag", is_flag=True, default=False, help="Full back up."
)
@click.option(
    "--backup-configs",
    "backup_configs_flag",
    is_flag=True,
    default=False,
    help="Back up app config files.",
)
@click.option(
    "--backup-dots",
    "backup_dots_flag",
    is_flag=True,
    default=False,
    help="Back up dotfiles.",
)
@click.option(
    "--backup-fonts",
    "backup_fonts_flag",
    is_flag=True,
    default=False,
    help="Back up installed fonts.",
)
@click.option(
    "--backup-packages",
    "backup_packages_flag",
    is_flag=True,
    default=False,
    help="Back up package libraries.",
)
@click.option(
    "--delete-config", is_flag=True, default=False, help="Delete config file."
)
@click.option(
    "--destroy-backup", is_flag=True, default=False, help="Delete backup directory."
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Don't backup or reinstall any files, just give verbose output.",
)
@click.option("--new-path", default=None, help="Input a new back up directory path.")
@click.option(
    "--no-new-backup-path-prompt",
    is_flag=True,
    default=False,
    help="Skip setting new back up directory path prompt.",
)
@click.option(
    "--no-splash", is_flag=True, default=False, help="Don't display splash screen."
)
@click.option(
    "--reinstall-all", is_flag=True, default=False, help="Full reinstallation."
)
@click.option(
    "--reinstall-configs", is_flag=True, default=False, help="Reinstall configs."
)
@click.option(
    "--reinstall-dots",
    is_flag=True,
    default=False,
    help="Reinstall dotfiles and dotfolders.",
)
@click.option("--reinstall-fonts", is_flag=True, default=False, help="Reinstall fonts.")
@click.option(
    "--reinstall-packages", is_flag=True, default=False, help="Reinstall packages."
)
@click.option("--remote", default=None, help="Set remote URL for the git repo.")
@click.option("--show", is_flag=True, default=False, help="Display config file.")
@click.option(
    "--version",
    "-v",
    is_flag=True,
    default=False,
    help="Display version and author info.",
)
def cli(
    add_dot,
    backup_configs_flag,
    delete_config,
    destroy_backup,
    backup_dots_flag,
    dry_run,
    backup_fonts_flag,
    backup_all_flag,
    new_path,
    no_splash,
    no_new_backup_path_prompt,
    backup_packages_flag,
    reinstall_all,
    reinstall_configs,
    reinstall_dots,
    reinstall_fonts,
    reinstall_packages,
    remote,
    show,
    version,
):
    """
    \b
    Easily back up installed packages, dotfiles, and more.
    You can edit which files are backed up in ~/.shallow-backup.

    Written by Aaron Lichtman (@alichtman).
    """
    safe_create_config()
    check_if_config_upgrade_needed()
    check_insecure_config_permissions()

    # Process CLI args
    admin_action = any([add_dot, delete_config, destroy_backup, show, version])
    has_cli_arg = any(
        [
            no_new_backup_path_prompt,
            backup_all_flag,
            backup_dots_flag,
            backup_packages_flag,
            backup_fonts_flag,
            backup_configs_flag,
            reinstall_dots,
            reinstall_fonts,
            reinstall_all,
            reinstall_configs,
            reinstall_packages,
        ]
    )
    skip_prompt = any(
        [
            backup_all_flag,
            backup_dots_flag,
            backup_configs_flag,
            backup_packages_flag,
            backup_fonts_flag,
            reinstall_packages,
            reinstall_configs,
            reinstall_dots,
            reinstall_fonts,
        ]
    )

    backup_config = get_config()

    # Perform administrative action and exit.
    if admin_action:
        if version:
            print_version_info()
        elif delete_config:
            delete_config_file()
        elif destroy_backup:
            backup_home_path = expand_to_abs_path(get_config()["backup_path"])
            destroy_backup_dir(backup_home_path)
        elif show:
            show_config()
        elif add_dot:
            new_config = add_dot_path_to_config(backup_config, add_dot)
            write_config(new_config)
        sys.exit()

    # Start CLI
    if not no_splash:
        splash_screen()

    # User entered a new path, so update the config
    if new_path:
        abs_path = os.path.abspath(new_path)

        if not check_if_path_is_valid_dir(abs_path):
            sys.exit(1)

        print_path_blue("\nUpdating shallow-backup path to:", abs_path)
        backup_config["backup_path"] = abs_path
        write_config(backup_config)

    # User didn't enter any CLI args so prompt for path update before showing menu
    elif not has_cli_arg:
        path_update_prompt(backup_config)

    # Create backup directory and do git setup
    backup_home_path = expand_to_abs_path(get_config()["backup_path"])
    mkdir_warn_overwrite(backup_home_path)
    repo, new_git_repo_created = safe_git_init(backup_home_path)
    create_gitignore(backup_home_path, "root-gitignore")

    # Prompt user for remote URL if needed
    if new_git_repo_created and not remote:
        git_url_prompt(repo)

    # Set remote URL from CLI arg
    if remote:
        git_set_remote(repo, remote)

    dotfiles_path = os.path.join(backup_home_path, "dotfiles")
    create_gitignore(dotfiles_path, "dotfiles-gitignore")

    configs_path = os.path.join(backup_home_path, "configs")
    packages_path = os.path.join(backup_home_path, "packages")
    fonts_path = os.path.join(backup_home_path, "fonts")

    # Command line options
    if skip_prompt:
        if reinstall_packages:
            reinstall_packages_sb(packages_path, dry_run=dry_run)
        elif reinstall_configs:
            reinstall_configs_sb(configs_path, dry_run=dry_run)
        elif reinstall_fonts:
            reinstall_fonts_sb(fonts_path, dry_run=dry_run)
        elif reinstall_dots:
            reinstall_dots_sb(dotfiles_path, dry_run=dry_run)
        elif reinstall_all:
            reinstall_all_sb(
                dotfiles_path, packages_path, fonts_path, configs_path, dry_run=dry_run
            )
        elif backup_all_flag:
            backup_all(
                dotfiles_path,
                packages_path,
                fonts_path,
                configs_path,
                dry_run=dry_run,
                skip=True,
            )
            if not dry_run:
                git_add_all_commit_push(repo, "full_backup")
        elif backup_dots_flag:
            backup_dotfiles(dotfiles_path, dry_run=dry_run, skip=True)
            # The reason that dotfiles/.git is special cased, and none of the others are is because maintaining a separate git repo for dotfiles is a common use case.
            handle_separate_git_dir_in_dotfiles(dotfiles_path, dry_run)
            if not dry_run:
                git_add_all_commit_push(repo, "dotfiles")
        elif backup_configs_flag:
            backup_configs(configs_path, dry_run=dry_run, skip=True)
            if not dry_run:
                git_add_all_commit_push(repo, "configs")
        elif backup_packages_flag:
            backup_packages(packages_path, dry_run=dry_run, skip=True)
            if not dry_run:
                git_add_all_commit_push(repo, "packages")
        elif backup_fonts_flag:
            backup_fonts(fonts_path, dry_run=dry_run, skip=True)
            if not dry_run:
                git_add_all_commit_push(repo, "fonts")
    # No CL options, show action menu and process selected option.
    else:
        selection = main_menu_prompt()
        action, _, target = selection.rpartition(" ")
        if action == "back up":
            if target == "all":
                backup_all(dotfiles_path, packages_path, fonts_path, configs_path)
                handle_separate_git_dir_in_dotfiles(dotfiles_path, dry_run=dry_run)
                git_add_all_commit_push(repo, target)
            elif target == "dotfiles":
                backup_dotfiles(dotfiles_path)
                handle_separate_git_dir_in_dotfiles(dotfiles_path, dry_run)
                git_add_all_commit_push(repo, target)
            elif target == "configs":
                backup_configs(configs_path)
                git_add_all_commit_push(repo, target)
            elif target == "packages":
                backup_packages(packages_path)
                git_add_all_commit_push(repo, target)
            elif target == "fonts":
                backup_fonts(fonts_path)
                git_add_all_commit_push(repo, target)
        elif action == "reinstall":
            if target == "packages":
                reinstall_packages_sb(packages_path)
            elif target == "configs":
                reinstall_configs_sb(configs_path)
            elif target == "fonts":
                reinstall_fonts_sb(fonts_path)
            elif target == "dotfiles":
                reinstall_dots_sb(dotfiles_path)
            elif target == "all":
                reinstall_all_sb(dotfiles_path, packages_path, fonts_path, configs_path)
        elif target == "config":
            if action.startswith("show"):
                show_config()
            elif action.startswith("add"):
                add_to_config_prompt()
            elif action.startswith("remove"):
                remove_from_config_prompt()
        elif action == "destroy":
            if prompt_yes_no(
                "Erase backup directory: {}?".format(backup_home_path), Fore.RED
            ):
                destroy_backup_dir(backup_home_path)
            else:
                print_red_bold(
                    "Exiting to prevent accidental deletion of backup directory."
                )

    sys.exit()


if __name__ == "__main__":
    cli()
