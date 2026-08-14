# Contributing

## Setup

Requirements: Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Commands

| Command | What it does |
|---|---|
| `make run` | Run the CLI |
| `make format` | Fix import order (ruff), then lint-fix and format |
| `make check` | Type check (`ty`) + lint (ruff) + format check |
| `make test` | Run the test suite (pytest) |

Run `make check` and `make test` before submitting changes; new code should include tests.

## Project layout

```
src/git_autoc/
├── main.py           # CLI (typer), wires all layers
├── core/config.py    # settings, TOML loading, config management
├── git/utils.py      # git operations (diff, log, stage, commit)
└── llm/              # prompt building, provider, commit styles
```
