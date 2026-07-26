import subprocess
from pathlib import Path


def has_staged_changes(cwd: Path | None = None) -> bool:
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=cwd,
        capture_output=True,
        check=False,
    )
    return result.returncode != 0


def get_staged_diff(cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", "diff", "--cached"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    result.check_returncode()
    return result.stdout


def get_recent_commits(n: int = 5, cwd: Path | None = None) -> list[str]:
    result = subprocess.run(
        ["git", "log", f"-{n}", "--oneline"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    result.check_returncode()
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def commit(message: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", "commit", "-m", message],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    result.check_returncode()
    return result.stdout
