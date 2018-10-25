# NOTE: THIS FILE EXISTS AS PART OF A MAJOR REFACTORING. THESE FUNCTIONS SHOULD NOT BE INCLUDED IN THE NEXT RELEASE


# TODO: Convert these two functions to store info in the actual config and just read from it.
def get_configs_path_mapping():
	"""
	Gets a dictionary mapping directories to back up to their destination path.
	"""
	return {
		"Library/Application Support/Sublime Text 2/Packages/User/": "sublime_2",
		"Library/Application Support/Sublime Text 3/Packages/User/": "sublime_3",
		"Library/Preferences/IntelliJIdea2018.2/": "intellijidea_2018.2",
		"Library/Preferences/PyCharm2018.2/": "pycharm_2018.2",
		"Library/Preferences/CLion2018.2/": "clion_2018.2",
		"Library/Preferences/PhpStorm2018.2": "phpstorm_2018.2",
		".atom/": "atom",
	}


def get_plist_mapping():
	"""
	Gets a dictionary mapping plist files to back up to their destination path.
	"""
	return {
		"Library/Preferences/com.apple.Terminal.plist": "plist/com.apple.Terminal.plist",
	}