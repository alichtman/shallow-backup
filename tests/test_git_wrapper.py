from unittest.mock import MagicMock

import pytest
from git import GitCommandError

from shallow_backup.git_wrapper import git_add_all_commit_push


def test_git_add_all_commit_push_push_error(mocker):
    """
    Test that git_add_all_commit_push handles a GitCommandError on push
    correctly.
    """
    # Mock the repo object
    mock_repo = MagicMock()
    mock_repo.is_dirty.return_value = True
    mock_repo.active_branch.name = "test_branch"

    # Mock the remote object
    mock_repo.remotes = MagicMock()
    mock_repo.remotes.origin = MagicMock()
    mock_repo.remotes.origin.name = "origin"
    mock_repo.remotes.origin.url = "test_url"
    mock_repo.remotes.__iter__.return_value = [mock_repo.remotes.origin]

    # Mock the git.push method to raise a GitCommandError
    mocker.patch.object(mock_repo.git, "push",
                        side_effect=GitCommandError("push", 1, b"error", b"error"))
    mocker.patch.object(mock_repo.git, "fetch")

    # Mock the other functions that are called
    mocker.patch("shallow_backup.git_wrapper.install_trufflehog_git_hook")
    mocker.patch("shallow_backup.git_wrapper.git_add_all_and_print_status")
    mocker.patch("shallow_backup.git_wrapper.prompt_yes_no",
                 side_effect=[True, True])
    mocker.patch("subprocess.run", return_value=MagicMock(returncode=0))
    mock_print_red_bold = mocker.patch(
        "shallow_backup.git_wrapper.print_red_bold")  # noqa: E501

    # Call the function and assert that sys.exit is called with 1
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        git_add_all_commit_push(mock_repo, dry_run=False)

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

    # Assert that the error message is printed
    mock_print_red_bold.assert_called_once_with(
        "ERROR: Failed to push to remote. "
        "Check your internet connection, credentials, "
        "and repository permissions."
    )
