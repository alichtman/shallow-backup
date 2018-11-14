import os
import sys
import shutil
sys.path.insert(0, "../shallow_backup")
from shallow_backup.backup import backup_dotfiles
from shallow_backup.config import safe_create_config, get_config_path

BACKUP_DIR = 'shallow-backup-test-backups-dir'
TEST_TEXT_CONTENT = 'THIS IS TEST CONTENT FOR THE DOTFILE'
DIRS = [BACKUP_DIR]
DOTFILES = [
	os.path.join(os.path.expanduser("~"), ".bashrc"),
	os.path.join(os.path.expanduser("~"), ".bash_profile"),
	os.path.join(os.path.expanduser("~"), ".gitconfig"),
	os.path.join(os.path.expanduser("~"), ".profile"),
	os.path.join(os.path.expanduser("~"), ".pypirc"),
	os.path.join(os.path.expanduser("~"), ".shallow-backup"),
	os.path.join(os.path.expanduser("~"), ".vimrc"),
	os.path.join(os.path.expanduser("~"), ".zshrc")
]

DOTFOLDERS = [
	os.path.join(os.path.expanduser("~"), ".ssh"),
	os.path.join(os.path.expanduser("~"), ".vim")
]


class TestBackupMethods:
	"""
	Test the backup methods.
	"""

	@staticmethod
	def setup_method():
		safe_create_config()

		for directory in DIRS:
			try:
				os.mkdir(directory)
			except FileExistsError as e:
				print("NOTE: {} ALREADY EXISTS. REMOVING.".format(e.filename))
				shutil.rmtree(directory)
				os.mkdir(directory)

		# Create all dotfiles and dotfolders
		for file in DOTFILES:
			if not os.path.exists(file):
				with open(file, "w") as f:
					f.write(TEST_TEXT_CONTENT)

		for folder in DOTFOLDERS:
			if not os.path.exists(folder):
				os.mkdir(folder)
				for file in ["test1", "test2"]:
					with open(os.path.join(folder, file), "w+") as f:
						f.write(TEST_TEXT_CONTENT)

	@staticmethod
	def teardown_method():
		print("Not deleting your dotfiles. You're welcome.")
		# for file in DOTFILES:
		# 	os.remove(file)
		# for directory in DIRS:
		# 	shutil.rmtree(directory)
		# os.remove(get_config_path())

	def test_backup_dotfiles(self):
		"""
		Test that backing up a directory works as expected
		"""
		backup_dotfiles(os.path.join(BACKUP_DIR, "dotfiles"), skip=True)

		dotfiles_path = os.path.join(BACKUP_DIR, "dotfiles")
		assert os.path.isdir(dotfiles_path)

		for path in DOTFILES:
			backed_up_dot = os.path.join(dotfiles_path, os.path.split(path)[-1])
			assert os.path.isfile(backed_up_dot)
