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


def has_unstaged_changes(cwd: Path | None = None) -> bool:
    diff = subprocess.run(
        ["git", "diff", "--quiet"],
        cwd=cwd,
        capture_output=True,
        check=False,
    )
    if diff.returncode != 0:
        return True
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    return any(line.startswith("??") for line in status.stdout.splitlines())


def stage_all(cwd: Path | None = None) -> None:
    result = subprocess.run(
        ["git", "add", "-A"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    result.check_returncode()


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


def get_staged_files(cwd: Path | None = None) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [f for f in result.stdout.splitlines() if f]


def get_recent_commits(n: int = 5, cwd: Path | None = None) -> list[str]:
    result = subprocess.run(
        ["git", "log", f"-{n}", "--oneline"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
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


def commit_edit(message: str, cwd: Path | None = None) -> bool:
    try:
        proc = subprocess.run(
            ["git", "commit", "-e", "-m", message],
            cwd=cwd,
            check=False,
        )
        return proc.returncode == 0
    except KeyboardInterrupt:
        return False
