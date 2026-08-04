import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=repo,
        capture_output=True,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=repo,
        capture_output=True,
        check=True,
    )
    init_file = repo / "init.txt"
    init_file.write_text("initial")
    subprocess.run(
        ["git", "add", "init.txt"], cwd=repo, capture_output=True, check=True
    )
    subprocess.run(
        ["git", "commit", "-m", "chore: initial commit"],
        cwd=repo,
        capture_output=True,
        check=True,
    )
    return repo


@pytest.fixture
def staged_repo(git_repo: Path) -> Path:
    new_file = git_repo / "feature.py"
    new_file.write_text("def foo():\n    return 42\n")
    subprocess.run(
        ["git", "add", "feature.py"], cwd=git_repo, capture_output=True, check=True
    )
    return git_repo


@pytest.fixture
def unstaged_repo(git_repo: Path) -> Path:
    new_file = git_repo / "new.txt"
    new_file.write_text("not staged\n")
    return git_repo
