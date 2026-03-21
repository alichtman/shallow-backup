from unittest.mock import MagicMock, patch, call

from git import GitCommandError

from shallow_backup.git_wrapper import git_add_all_commit_push


def _make_mock_repo():
    """Create a mock repo that looks dirty with an origin remote."""
    mock_repo = MagicMock()
    mock_repo.is_dirty.return_value = True
    mock_repo.active_branch.name = "main"
    mock_repo.remotes.origin.name = "origin"
    mock_repo.remotes.origin.url = "git@github.com:user/repo"
    mock_repo.remotes.__iter__ = lambda self: iter([mock_repo.remotes.origin])
    return mock_repo


@patch("shallow_backup.git_wrapper.install_trufflehog_git_hook")
@patch("shallow_backup.git_wrapper.git_add_all_and_print_status")
@patch("shallow_backup.git_wrapper.prompt_yes_no", side_effect=[True, True])
@patch("subprocess.run", return_value=MagicMock(returncode=0))
@patch("shallow_backup.git_wrapper.print_red_bold")
def test_push_non_fast_forward_error(
    mock_print_red, mock_subprocess, mock_prompt, mock_status, mock_hook
):
    """Non-fast-forward push error prints a specific helpful message."""
    mock_repo = _make_mock_repo()
    mock_repo.git.push.side_effect = GitCommandError(
        "git push", 1, b"non-fast-forward", b""
    )

    git_add_all_commit_push(mock_repo, dry_run=False)

    messages = [c.args[0] for c in mock_print_red.call_args_list]
    assert any("non-fast-forward" not in m and "git pull" in m for m in messages)
    assert any("Exception:" in m for m in messages)


@patch("shallow_backup.git_wrapper.install_trufflehog_git_hook")
@patch("shallow_backup.git_wrapper.git_add_all_and_print_status")
@patch("shallow_backup.git_wrapper.prompt_yes_no", side_effect=[True, True])
@patch("subprocess.run", return_value=MagicMock(returncode=0))
@patch("shallow_backup.git_wrapper.print_red_bold")
def test_push_generic_error(
    mock_print_red, mock_subprocess, mock_prompt, mock_status, mock_hook
):
    """Generic push error prints a generic message with traceback."""
    mock_repo = _make_mock_repo()
    mock_repo.git.push.side_effect = GitCommandError(
        "git push", 1, b"permission denied", b""
    )

    git_add_all_commit_push(mock_repo, dry_run=False)

    messages = [c.args[0] for c in mock_print_red.call_args_list]
    assert any("git push failed!" in m for m in messages)
    assert any("git pull" not in m and "Exception:" in m for m in messages)


@patch("shallow_backup.git_wrapper.install_trufflehog_git_hook")
@patch("shallow_backup.git_wrapper.git_add_all_and_print_status")
@patch("shallow_backup.git_wrapper.prompt_yes_no", side_effect=[True, True])
@patch("subprocess.run", return_value=MagicMock(returncode=0))
@patch("shallow_backup.git_wrapper.print_red_bold")
def test_push_success_no_error(
    mock_print_red, mock_subprocess, mock_prompt, mock_status, mock_hook
):
    """Successful push does not print any error."""
    mock_repo = _make_mock_repo()

    git_add_all_commit_push(mock_repo, dry_run=False)

    mock_print_red.assert_not_called()
