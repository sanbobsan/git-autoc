import typer

from autocommit.git.utils import (
    commit,
    get_recent_commits,
    get_staged_diff,
    has_staged_changes,
)
from autocommit.llm.prompt import build_messages
from autocommit.llm.provider import generate

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    dry_run: bool = typer.Option(
        False, "--dry-run", "-n", help="Generate without committing"
    ),
) -> None:
    if not has_staged_changes():
        typer.echo("No staged changes found")
        raise typer.Exit()

    diff = get_staged_diff()
    commits = get_recent_commits(5)
    messages = build_messages(diff, commits)
    result = generate(messages)

    typer.echo(result)

    if not dry_run and typer.confirm("Commit?"):
        output = commit(result)
        typer.echo(output)
