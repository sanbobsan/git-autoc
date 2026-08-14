# git-autoc

AI-powered git commit message generator. Reads your staged changes and writes a conventional commit message using any OpenAI-compatible API.

## Features

- Generates **Conventional Commits** from your staged diff
- Uses your **recent commit history** for style-consistent output
- **Interactive confirmation** (`y` / `e` / `N`) before committing
- **Dry-run** mode with no side effects
- Three **body styles**: long, bullet list, paragraph
- Works with any **OpenAI-compatible API** (Ollama, LM Studio, OpenAI, …)
- Configuration managed **from the CLI** — no `.env`

## Installation

Requires Python 3.13+.

### Run without installing

Run the latest version from PyPI without installing anything:

```bash
uvx git-autoc --help
```

### Install as a command

Install it once with `uv tool install`:

```bash
uv tool install git-autoc
git-autoc --help
```

This puts two commands on your PATH:

- `git-autoc` — a native git subcommand, so `git autoc` just works in any repository
- `autoc` — a short standalone alias

To remove it later:

```bash
uv tool uninstall git-autoc
```

## Usage

Both installation modes work the same. This guide uses `git autoc`; replace it with `uvx git-autoc` or `autoc` as you prefer.

Stage the changes you want to commit, then run:

```bash
git autoc
```

The tool generates a commit message, shows it, and asks how to proceed:

- `y` — commit with the generated message
- `e` — open the editor to adjust the message before committing
- `N` (default) — abort, keep changes staged

If nothing is staged but there are unstaged changes, you are asked whether to stage everything first. If the repository is clean, the tool exits.

To generate without committing (or to preview the message first):

```bash
git autoc --dry-run
```

### Options

| Option | Alias | Description |
|---|---|---|
| `--dry-run` | `-n` | Generate a message without committing |
| `--long` | `-l` | Allow an optional body paragraph or bullet list |
| `--list` | | Always add a bullet-list body |
| `--desc` | | Always add a paragraph body |

`--long`, `--list`, and `--desc` are mutually exclusive.

## Body styles

| Style | Flag | Behavior |
|---|---|---|
| Default | | One-line message, no body |
| Long | `--long` | Body added only if the change is worth explaining |
| List | `--list` | Body always present, as a bullet list |
| Description | `--desc` | Body always present, as a single paragraph |

## Configuration

Configuration lives in `~/.config/git-autoc/config.toml`.

Show the current configuration (creates a default file on first run):

```bash
git autoc config
```

Set a value interactively:

```bash
git autoc config set openai_model
```

Remove the config file and directory:

```bash
git autoc config clear
```

### Settings

| Key | Default | Description |
|---|---|---|
| `openai_base_url` | `http://localhost:11434/v1` | Base URL of the OpenAI-compatible API |
| `openai_model` | `model` | Model name to use |
| `openai_api_key` | *(empty)* | API key; leave empty for local providers |
| `openai_temperature` | `0.2` | Sampling temperature (0–1, lower is more deterministic) |
| `openai_max_tokens` | `512` | Maximum tokens in the generated response |

`openai_base_url` and `openai_model` are required and must be non-empty; the tool refuses to run otherwise.

## Development

```bash
make run     # run the CLI
make format  # format code (ruff)
make check   # type check (ty) + lint + format check
make test    # run tests (pytest)
```

### Project layout

```
src/git_autoc/
├── main.py           # CLI (typer), wires all layers
├── core/config.py    # settings, TOML loading, config management
├── git/utils.py      # git operations (diff, log, stage, commit)
└── llm/              # prompt building, provider, commit styles
```

### Stack

- **CLI:** typer + rich
- **Config:** pydantic + tomllib
- **AI client:** openai (OpenAI-compatible API)
- **Quality:** ruff, ty, pytest
