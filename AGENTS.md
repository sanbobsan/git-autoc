# Project: auto-commit

CLI-утилита для автоматической генерации и создания git-коммитов через AI.

---

## Tech Stack

| | |
|---|---|
| Language | Python 3.13+ |
| Package manager | `uv` (uv_build) |
| Config | `pydantic` + `tomllib` — `~/.config/autocommit/config.toml` |
| AI client | `openai` (OpenAI-compatible API) |
| UI | `rich` (Panel, Console, spinner) |
| Linter | `ruff` (imports, all rules, formatter) |
| Type checker | `ty` |
| Project layout | `src/` layout (`src/app/`) |

---

## Project Structure

```
src/app/
├── __init__.py          # empty
├── __main__.py          # from app.main import main; main()
├── main.py              # CLI: argparse, wires all layers
├── core/
│   ├── __init__.py      # empty
│   └── config.py        # pydantic-settings Settings
├── git/
│   ├── __init__.py
│   └── utils.py         # diff, log, stage, commit helpers
└── llm/
    ├── __init__.py
    ├── provider.py      # generate(messages) -> str via openai
    ├── prompt.py        # build system + user messages from git context
    └── style.py         # BodyStyle enum, CommitStyle dataclass
```

---

## Make Commands

```makefile
run        uv run -m autocommit
format     ruff check --select I --fix src/ && ruff check --fix src/ && ruff format src/
test       uv run pytest -v
check      ty check src/ && ruff check src/ tests/ && ruff format --check src/ tests/
```

Always run `make check` and `make test` before finishing a task. New code must include tests.

---

## Coding Conventions

### General

- No comments in code unless the logic is non-trivial. Let the code speak.
- No emojis in code or commit messages.
- Newline at end of every file.
- No trailing whitespace.
- No executable permissions on `.py` files.

### Imports

- Style: Ruff with `--select I` (isort). Ruff will fix ordering automatically via `make format`.
- Imports grouped: stdlib → third-party → local.
- Always absolute imports: `from app.core.config import settings`.

### Types

- Full type annotations on all functions and dataclass/Pydantic fields.
- Use `ty` for type checking (`make check` runs it).
- Prefer `| None` over `Optional[]`.

### Naming

- `snake_case` for functions, variables, modules.
- `PascalCase` for classes.
- `UPPER_CASE` for constants.
- Single underscore prefix `_` for private helpers.

### Pydantic

- `Settings` class uses `pydantic.BaseModel` (no `.env`).
- Module-level singleton: `settings = load_settings()`.
- All fields have defaults.

### Error handling

- Let exceptions propagate at the top level (CLI handles them).
- Use early returns / guard clauses instead of deep nesting.

---

## Config Conventions

Settings are defined in `src/autocommit/core/config.py` using `pydantic.BaseModel` and loaded from `~/.config/autocommit/config.toml` (read-only via `tomllib`).

```python
class Settings(BaseModel):
    openai_base_url: str = "http://localhost:11434/v1"
    openai_model: str = "model"
    openai_api_key: str = ""
    openai_temperature: float = 0.2
    openai_max_tokens: int = 512
```

- Managed via `git autoc config` (create/show) and `git autoc config set <key>` (interactive).
- `load_settings()` loads the TOML file; `validate_settings()` enforces `REQUIRED` non-empty fields at generate time.
- No `.env` support. `.env.example` kept only as reference.

---

## Git Workflow

- Branch: `main` (linear history).
- Commits follow **Conventional Commits**:
  ```
  type(scope): short description

  Longer body with bullet points if needed.
  ```
  Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `style`, `perf`, `ci`, `build`.
- No merge commits — use rebase.
- Never commit unless explicitly asked.

---

## Architecture

Layered design:
1. `core/config.py` — configuration
2. `git/` — interface to git operations
3. `llm/` — AI provider + prompt construction
4. `main.py` — CLI (Typer), UI (Rich), wires everything together

Each layer imports only from layers above it (core → git → llm → main).
