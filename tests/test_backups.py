import os
import sys
import shutil
sys.path.insert(0, "../shallow_backup")
from shallow_backup.backup import backup_dotfiles
from shallow_backup.config import safe_create_config

BACKUP_DIR = 'shallow-backup-test-backups-dir'
FAKE_HOME_DIR = 'shallow-backup-test-backups-src-dir'
TEST_TEXT_CONTENT = 'THIS IS TEST CONTENT FOR THE DOTFILE'
DIRS = [BACKUP_DIR, FAKE_HOME_DIR]
DOTFILES = [
	os.path.join(FAKE_HOME_DIR, ".bashrc"),
	os.path.join(FAKE_HOME_DIR, ".bash_profile"),
	os.path.join(FAKE_HOME_DIR, ".gitconfig"),
	os.path.join(FAKE_HOME_DIR, ".profile"),
	os.path.join(FAKE_HOME_DIR, ".pypirc"),
	os.path.join(FAKE_HOME_DIR, ".shallow-backup"),
	os.path.join(FAKE_HOME_DIR, ".vimrc"),
	os.path.join(FAKE_HOME_DIR, ".zshrc")
]

DOTFOLDERS = [
	os.path.join(FAKE_HOME_DIR, ".ssh"),
	os.path.join(FAKE_HOME_DIR, ".vim")
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
			except Exception:
				shutil.rmtree(directory)
				os.mkdir(directory)

		# Create all dotfiles and dotfolders
		for file in DOTFILES:
			print(f"Creating {file}")
			with open(file, "w+") as f:
				f.write(TEST_TEXT_CONTENT)

		for folder in DOTFOLDERS:
			os.mkdir(folder)
			for file in ["test1", "test2"]:
				with open(os.path.join(folder, file), "w+") as f:
					f.write(TEST_TEXT_CONTENT)

	@staticmethod
	def teardown_method():
		for folder in DIRS:
			print(f"Removing {folder}")
			shutil.rmtree(folder)

	def test_backup_dotfiles(self):
		"""
		Test backing up dotfiles and dotfolders.
		"""
		backup_dest_path = os.path.join(BACKUP_DIR, "dotfiles")
		backup_dotfiles(backup_dest_path, home_path=FAKE_HOME_DIR, skip=True)
		assert os.path.isdir(backup_dest_path)
		for path in DOTFILES:
			print(f"BACKUP DESTINATION DIRECTORY ({backup_dest_path}) CONTENTS:", os.listdir(backup_dest_path))
			print(path + " should already be backed up.")
			print("CWD:", os.getcwd())
			backed_up_dot = os.path.join(backup_dest_path, os.path.split(path)[-1])
			print(f"Backed up dot: {backed_up_dot}")
			assert os.path.isfile(backed_up_dot)
