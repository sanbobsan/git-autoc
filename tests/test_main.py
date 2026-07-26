from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from autocommit.main import app

runner = CliRunner()


def test_dry_run_generates_message(
    staged_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(staged_repo)
    mock_message = "feat(test): add test feature"
    with patch("autocommit.main.generate", return_value=mock_message):
        result = runner.invoke(app, ["--dry-run"])

    assert result.exit_code == 0
    assert mock_message in result.stdout


def test_no_staged_changes(git_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(git_repo)
    result = runner.invoke(app, ["--dry-run"])
    assert result.exit_code == 0
    assert "No staged changes found" in result.stdout


def test_commit_action_calls_commit(
    staged_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(staged_repo)
    mock_message = "chore: test commit"
    with (
        patch("autocommit.main.generate", return_value=mock_message),
        patch("autocommit.main.commit", return_value="ok") as mock_commit,
    ):
        result = runner.invoke(app, [], input="y\n")

    assert result.exit_code == 0
    mock_commit.assert_called_once_with(mock_message)
    assert mock_message in result.stdout


def test_edit_action_calls_commit_edit(
    staged_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(staged_repo)
    mock_message = "chore: test commit"
    with (
        patch("autocommit.main.generate", return_value=mock_message),
        patch("autocommit.main.commit_edit", return_value=True) as mock_edit,
    ):
        result = runner.invoke(app, [], input="e\n")

    assert result.exit_code == 0
    mock_edit.assert_called_once_with(mock_message)
    assert "Committed" in result.stdout


def test_edit_action_aborted(
    staged_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(staged_repo)
    mock_message = "chore: test commit"
    with (
        patch("autocommit.main.generate", return_value=mock_message),
        patch("autocommit.main.commit_edit", return_value=False),
    ):
        result = runner.invoke(app, [], input="e\n")

    assert result.exit_code == 0
    assert "Commit aborted" in result.stdout


def test_no_action_does_nothing(
    staged_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(staged_repo)
    mock_message = "chore: test commit"
    with (
        patch("autocommit.main.generate", return_value=mock_message),
        patch("autocommit.main.commit") as mock_commit,
    ):
        result = runner.invoke(app, [], input="N\n")

    assert result.exit_code == 0
    mock_commit.assert_not_called()
    assert mock_message in result.stdout


def test_long_flag(staged_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(staged_repo)
    with patch("autocommit.main.generate") as mock:
        mock.return_value = "feat: test"
        runner.invoke(app, ["--dry-run", "--long"])

    args, _ = mock.call_args
    messages = args[0]
    system = messages[0]["content"]
    assert "Body is optional" in system


def test_list_flag(staged_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(staged_repo)
    with patch("autocommit.main.generate") as mock:
        mock.return_value = "feat: test"
        runner.invoke(app, ["--dry-run", "--list"])

    args, _ = mock.call_args
    messages = args[0]
    system = messages[0]["content"]
    assert "bullet list" in system
    assert "Always add a body" in system


def test_desc_flag(staged_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(staged_repo)
    with patch("autocommit.main.generate") as mock:
        mock.return_value = "feat: test"
        runner.invoke(app, ["--dry-run", "--desc"])

    args, _ = mock.call_args
    messages = args[0]
    system = messages[0]["content"]
    assert "single paragraph" in system


def test_mutual_exclusion(staged_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(staged_repo)
    with patch("autocommit.main.generate") as mock:
        mock.return_value = "feat: test"
        result = runner.invoke(app, ["--dry-run", "--long", "--list"])

    assert result.exit_code == 0
    assert "Use only one" in result.stdout
