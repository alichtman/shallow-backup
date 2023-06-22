import os
import sys
import inquirer
from colorama import Fore, Style
from .constants import ProjInfo


def print_blue(text):
    print(Fore.BLUE + text + Style.RESET_ALL)


def print_red(text):
    print(Fore.RED + text + Style.RESET_ALL)


def print_yellow(text):
    print(Fore.YELLOW + text + Style.RESET_ALL)


def print_green(text):
    print(Fore.GREEN + text + Style.RESET_ALL)


def print_blue_bold(text):
    print(Fore.BLUE + Style.BRIGHT + text + Style.RESET_ALL)


def print_red_bold(text):
    print(Fore.RED + Style.BRIGHT + text + Style.RESET_ALL)


def print_yellow_bold(text):
    print(Fore.YELLOW + Style.BRIGHT + text + Style.RESET_ALL)


def print_green_bold(text):
    print(Fore.GREEN + Style.BRIGHT + text + Style.RESET_ALL)


def print_path_blue(text, path):
    print(Fore.BLUE + Style.BRIGHT + text, Style.NORMAL + path + Style.RESET_ALL)


def print_path_red(text, path):
    print(Fore.RED + Style.BRIGHT + text, Style.NORMAL + path + Style.RESET_ALL)


def print_path_yellow(text, path):
    print(Fore.YELLOW + Style.BRIGHT + text, Style.NORMAL + path + Style.RESET_ALL)


def print_path_green(text, path):
    print(Fore.GREEN + Style.BRIGHT + text, Style.NORMAL + path + Style.RESET_ALL)


def print_dry_run_copy_info(source, dest):
    """Show source -> dest copy. Replaces expanded ~ with ~ if it's at the beginning of paths.
    source and dest are trimmed in the middle if needed. Removed characters will be replaced by ...
    :param source: Can be of type str or Path
    :param dest: Can be of type str or Path
    """

    def shorten_home(path):
        expanded_home = os.path.expanduser("~")
        path = str(path)
        if path.startswith(expanded_home):
            return path.replace(expanded_home, "~")
        return path

    def truncate_middle(path: str, acceptable_len: int):
        """Middle truncate a string
        https://www.xormedia.com/string-truncate-middle-with-ellipsis/
        """
        if len(path) <= acceptable_len:
            return path
        # half of the size, minus the 3 .'s
        n_2 = int(acceptable_len / 2 - 3)
        # whatever's left
        n_1 = int(acceptable_len - n_2 - 3)
        return f"{path[:n_1]}...{path[-n_2:]}"

    trimmed_source = shorten_home(source)
    trimmed_dest = shorten_home(dest)
    longest_allowed_path_len = 87
    if len(trimmed_source) + len(trimmed_dest) > longest_allowed_path_len:
        trimmed_source = truncate_middle(trimmed_source, longest_allowed_path_len)
        trimmed_dest = truncate_middle(trimmed_dest, longest_allowed_path_len)
    print(
        Fore.YELLOW + Style.BRIGHT + trimmed_source + Style.NORMAL,
        "->",
        Style.BRIGHT + trimmed_dest + Style.RESET_ALL,
    )


def print_version_info(cli=True):
    """
    Formats version differently for CLI and splash screen.
    """
    version = "v{} by {} (@{})".format(
        ProjInfo.VERSION, ProjInfo.AUTHOR_FULL_NAME, ProjInfo.AUTHOR_GITHUB
    )
    if not cli:
        print(Fore.RED + Style.BRIGHT + "\t{}\n".format(version) + Style.RESET_ALL)
    else:
        print(version)


def splash_screen():
    """Display splash graphic, and then stylized version and author info."""
    print(Fore.YELLOW + Style.BRIGHT + "\n" + ProjInfo.LOGO + Style.RESET_ALL)
    print_version_info(False)


def print_section_header(title, color):
    """Prints variable sized section header."""
    block = "#" * (len(title) + 2)
    print("\n" + color + Style.BRIGHT + block)
    print("#", title)
    print(block + "\n" + Style.RESET_ALL)


def print_pkg_mgr_backup(mgr):
    print(
        "{}Backing up {}{}{}{}{} packages list...{}".format(
            Fore.BLUE,
            Style.BRIGHT,
            Fore.YELLOW,
            mgr,
            Fore.BLUE,
            Style.NORMAL,
            Style.RESET_ALL,
        )
    )


def print_pkg_mgr_reinstall(mgr):
    print(
        "{}Reinstalling {}{}{}{}{}...{}".format(
            Fore.BLUE,
            Style.BRIGHT,
            Fore.YELLOW,
            mgr,
            Fore.BLUE,
            Style.NORMAL,
            Style.RESET_ALL,
        )
    )


# TODO: BUG: Why does moving this to prompts.py cause circular imports?
def prompt_yes_no(message, color, invert=False):
    """
    Print question and return True or False depending on user selection from list.
    """
    questions = [
        inquirer.List(
            "choice",
            message=color + Style.BRIGHT + message + Fore.BLUE,
            choices=(" No", " Yes") if invert else (" Yes", " No"),
        )
    ]

    answers = inquirer.prompt(questions)
    if answers:
        return answers.get("choice").strip().lower() == "yes"
    else:
        sys.exit(1)
