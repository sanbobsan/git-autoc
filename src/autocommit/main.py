import typer
from rich.console import Console
from rich.panel import Panel

from autocommit.git.utils import (
    commit,
    get_recent_commits,
    get_staged_diff,
    get_staged_files,
    has_staged_changes,
)
from autocommit.llm.prompt import build_messages
from autocommit.llm.provider import generate
from autocommit.llm.style import BodyStyle, CommitStyle

console = Console()
app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    dry_run: bool = typer.Option(
        False, "--dry-run", "-n", help="Generate without committing"
    ),
    long: bool = typer.Option(
        False, "--long", "-l", help="Generate with optional body"
    ),
    list_mode: bool = typer.Option(
        False, "--list", help="Generate with bullet list body"
    ),
    desc: bool = typer.Option(False, "--desc", help="Generate with paragraph body"),
) -> None:
    flags = sum([long, list_mode, desc])
    if flags > 1:
        console.print("Use only one of --long, --list, --desc", style="red")
        raise typer.Exit()

    if not has_staged_changes():
        console.print("No staged changes found", style="yellow")
        raise typer.Exit()

    if long:
        body = BodyStyle.LONG
    elif list_mode:
        body = BodyStyle.LIST
    elif desc:
        body = BodyStyle.DESC
    else:
        body = BodyStyle.NONE

    style = CommitStyle(body=body)

    diff = get_staged_diff()
    commits = get_recent_commits(5)
    files = get_staged_files()
    messages = build_messages(diff, commits, files, style)

    with console.status("Generating commit message..."):
        try:
            result = generate(messages)
        except RuntimeError as e:
            console.print(e, style="red")
            raise typer.Exit()

    console.print(Panel(result, title="Generated Commit Message"))

    if not dry_run and typer.confirm("Commit?"):
        output = commit(result)
        console.print(f"Created commit: {output.strip()}", style="bold green")
