from colorama import Fore, Style
from constants import ProjInfo
import inquirer


def print_version_info(cli=True):
	"""
	Formats version differently for CLI and splash screen.
	"""
	version = "v{} by {} (@{})".format(ProjInfo.VERSION,
	                                   ProjInfo.AUTHOR_FULL_NAME,
	                                   ProjInfo.AUTHOR_GITHUB)
	if not cli:
		print(Fore.RED + Style.BRIGHT + "\t{}\n".format(version) + Style.RESET_ALL)
	else:
		print(version)


def splash_screen():
	"""
	Display splash graphic, and then stylized version
	"""
	print(Fore.YELLOW + Style.BRIGHT + "\n" + ProjInfo.LOGO + Style.RESET_ALL)
	print_version_info(False)


def print_section_header(title, COLOR):
	"""
	Prints variable sized section header
	"""
	block = "#" * (len(title) + 2)
	print("\n" + COLOR + Style.BRIGHT + block)
	print("#", title)
	print(block + "\n" + Style.RESET_ALL)


def print_pkg_mgr_backup(mgr):
	print("{}Backing up {}{}{}{}{} packages list...{}".format(Fore.BLUE, Style.BRIGHT, Fore.YELLOW, mgr, Fore.BLUE, Style.NORMAL, Style.RESET_ALL))


# TODO: Integrate this in the reinstallation section
def print_pkg_mgr_reinstall(mgr):
	print("{}Reinstalling {}{}{}{}{} packages...{}".format(Fore.BLUE, Style.BRIGHT, Fore.YELLOW, mgr, Fore.BLUE, Style.NORMAL, Style.RESET_ALL))


def prompt_yes_no(message, color):
	"""
	Print question and return True or False depending on user selection from list.
	"""
	questions = [inquirer.List('choice',
	                           message=color + Style.BRIGHT + message + Fore.BLUE,
	                           choices=[' Yes', ' No'],
	                           )
	             ]

	answers = inquirer.prompt(questions)
	return answers.get('choice').strip().lower() == 'yes'
