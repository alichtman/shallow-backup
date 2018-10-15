import pytest

def test_backup_prompt():
    choices = [' Back up dotfiles', ' Back up packages', ' Back up fonts', ' Back up everything', ' Reinstall packages']
    return [i.strip().lower() for i in choices]

assert ' ' not in test_backup_prompt()
