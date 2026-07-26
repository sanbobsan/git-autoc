# Project: auto-commit

CLI-утилита для автоматической генерации и создания git-коммитов через AI.

---

## Tech Stack

| | |
|---|---|
| Language | Python 3.13+ |
| Package manager | `uv` (uv_build) |
| Config | `pydantic-settings` — `.env` + env vars |
| AI client | `openai` (OpenAI-compatible API) |
| Linter | `ruff` (imports, all rules, formatter) |
| Type checker | `ty` |
| Project layout | `src/` layout (`src/app/`) |

---

## Project Structure

```
src/app/
├── __init__.py          # empty
├── __main__.py          # from app.main import main; main()
├── main.py              # CLI entry point
├── core/
│   ├── __init__.py      # empty
│   └── config.py        # pydantic-settings Settings
├── git/
│   ├── __init__.py
│   └── utils.py         # git diff, log, commit helpers
├── llm/
│   ├── __init__.py
│   ├── client.py        # openai client factory
│   └── prompt.py        # prompt building
└── commit/
    ├── __init__.py
    └── generator.py     # high-level commit generation logic
```

---

## Make Commands

```makefile
run        uv run -m app
format     ruff check --select I --fix src/ && ruff check --fix src/ && ruff format src/
check      ty check src/ && ruff check src/ && ruff format --check src/
```

Always run `make check` before finishing a task.

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

- `Settings` class uses `SettingsConfigDict(env_file=".env")`.
- Module-level singleton: `settings = Settings()`.
- Required fields have no default; optional fields have defaults.

### Error handling

- Let exceptions propagate at the top level (CLI handles them).
- Use early returns / guard clauses instead of deep nesting.

---

## Config Conventions

Settings are defined in `src/app/core/config.py` using `pydantic.BaseSettings`.

```python
class Settings(BaseSettings):
    openai_base_url: str        # required
    openai_model: str           # required
    openai_api_key: str         # required
    openai_temperature: float = 0.2
    openai_max_tokens: int = 512

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
```

Env vars override `.env`, which is in `.gitignore`. Template at `.env.example`.

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
4. `commit/` — high-level orchestration
5. `main.py` — CLI, wires everything together

Each layer imports only from layers above it (core → git → llm → commit → main).
