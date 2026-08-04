import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from autocommit.core import config as config_module
from autocommit.git.utils import (
    commit,
    commit_edit,
    get_recent_commits,
    get_staged_diff,
    get_staged_files,
    has_staged_changes,
)
from autocommit.llm.prompt import build_messages
from autocommit.llm.provider import generate
from autocommit.llm.style import BodyStyle, CommitStyle

console = Console()
app = typer.Typer(add_completion=False)
config_app = typer.Typer(help="Manage autocommit configuration")
app.add_typer(config_app, name="config")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
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
    if ctx.invoked_subcommand is not None:
        return

    flags = sum([long, list_mode, desc])
    if flags > 1:
        console.print("Use only one of --long, --list, --desc", style="red")
        raise typer.Exit()

    if not has_staged_changes():
        console.print("No staged changes found", style="yellow")
        raise typer.Exit()

    try:
        config_module.validate_settings(config_module.settings)
    except config_module.ConfigError as e:
        console.print(e, style="red")
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

    if dry_run:
        return

    try:
        action = Prompt.ask("Commit?", choices=["y", "N", "e"], default="N")
    except KeyboardInterrupt:
        console.print("\nAborted", style="yellow")
        raise typer.Exit()

    if action == "y":
        output = commit(result)
        console.print(output.strip(), style="bold green")
    elif action == "e":
        if commit_edit(result):
            console.print("Committed", style="bold green")
        else:
            console.print("Commit aborted", style="yellow")


@config_app.callback(invoke_without_command=True)
def config_cmd(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is not None:
        return
    if not config_module.CONFIG_PATH.exists():
        config_module.create_default_config()
    content = config_module.CONFIG_PATH.read_text(encoding="utf-8")
    console.print(Panel(content, title=str(config_module.CONFIG_PATH)))


@config_app.command()
def set(key: str) -> None:
    """Set a config value (you will be prompted for the value)"""
    current = config_module.settings.model_dump().get(key, "")
    value = Prompt.ask(f"Enter value for {key}", default=str(current))
    try:
        config_module.set_config_value(key, value)
    except config_module.ConfigError as e:
        console.print(e, style="red")
        raise typer.Exit()
    config_module.settings = config_module.load_settings()
    console.print("Config updated", style="green")
