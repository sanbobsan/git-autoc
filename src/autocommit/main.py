import typer
from rich.console import Console
from rich.panel import Panel

from autocommit.git.utils import (
    commit,
    get_recent_commits,
    get_staged_diff,
    has_staged_changes,
)
from autocommit.llm.prompt import build_messages
from autocommit.llm.provider import generate

console = Console()
app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    dry_run: bool = typer.Option(
        False, "--dry-run", "-n", help="Generate without committing"
    ),
) -> None:
    if not has_staged_changes():
        console.print("No staged changes found", style="yellow")
        raise typer.Exit()

    diff = get_staged_diff()
    commits = get_recent_commits(5)
    messages = build_messages(diff, commits)

    with console.status("Generating commit message..."):
        result = generate(messages)

    console.print(Panel(result, title="Generated Commit Message"))

    if not dry_run and typer.confirm("Commit?"):
        output = commit(result)
        console.print(f"Created commit: {output.strip()}", style="bold green")
