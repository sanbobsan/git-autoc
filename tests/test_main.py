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


def test_dry_run_without_flag_shows_prompt(
    staged_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(staged_repo)
    mock_message = "chore: test commit"
    with patch("autocommit.main.generate", return_value=mock_message):
        result = runner.invoke(app, [], input="y\n")

    assert result.exit_code == 0
    assert mock_message in result.stdout
