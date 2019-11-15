import os
import sys
import shutil
from .test_utils import BACKUP_DEST_DIR, FAKE_HOME_DIR, DIRS, DOTFILES, DOTFOLDERS, setup_env_vars, unset_env_vars, create_config_for_test
sys.path.insert(0, "../shallow_backup")
from shallow_backup.backup import backup_dotfiles

TEST_TEXT_CONTENT = 'THIS IS TEST CONTENT FOR THE DOTFILES'


class TestBackupMethods:
	"""
	Test the backup methods.
	"""

	@staticmethod
	def setup_method():
		setup_env_vars()
		create_config_for_test()
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
		unset_env_vars()

	def test_backup_dotfiles(self):
		"""
		Test backing up dotfiles and dotfolders.
		"""
		backup_dest_path = os.path.join(BACKUP_DEST_DIR, "dotfiles")
		backup_dotfiles(backup_dest_path, home_path=FAKE_HOME_DIR, skip=True)
		assert os.path.isdir(backup_dest_path)
		for path in DOTFILES:
			print(f"BACKUP DESTINATION DIRECTORY ({backup_dest_path}) CONTENTS:", os.listdir(backup_dest_path))
			print(path + " should already be backed up.")
			print("CWD:", os.getcwd())
			backed_up_dot = os.path.join(backup_dest_path, os.path.split(path)[-1])
			print(f"Backed up dot: {backed_up_dot}")
			assert os.path.isfile(backed_up_dot)
