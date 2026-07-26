from pathlib import Path

from autocommit.git.utils import (
    commit,
    get_recent_commits,
    get_staged_diff,
    has_staged_changes,
)


def test_no_staged_changes(git_repo: Path) -> None:
    assert has_staged_changes(git_repo) is False


def test_has_staged_changes(staged_repo: Path) -> None:
    assert has_staged_changes(staged_repo) is True


def test_staged_diff_empty(git_repo: Path) -> None:
    assert get_staged_diff(git_repo) == ""


def test_staged_diff_content(staged_repo: Path) -> None:
    diff = get_staged_diff(staged_repo)
    assert "feature.py" in diff
    assert "def foo():" in diff
    assert "+" in diff


def test_recent_commits(git_repo: Path) -> None:
    commits = get_recent_commits(5, git_repo)
    assert len(commits) == 1
    assert "chore: initial commit" in commits[0]


def test_recent_commits_empty(tmp_path: Path) -> None:
    repo = tmp_path / "empty_repo"
    repo.mkdir()
    import subprocess

    subprocess.run(["git", "init"], cwd=repo, capture_output=True, check=True)
    commits = get_recent_commits(5, repo)
    assert commits == []


def test_commit(staged_repo: Path) -> None:
    output = commit("feat: add feature module", staged_repo)
    assert "feature" in output
    assert has_staged_changes(staged_repo) is False
    commits = get_recent_commits(5, staged_repo)
    assert any("feat: add feature module" in c for c in commits)
