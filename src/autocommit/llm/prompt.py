from openai.types.chat import ChatCompletionMessageParam

SYSTEM_PROMPT = """You generate conventional git commit messages from diffs.

Format: type(scope): short description

Types:
- feat    new feature or enhancement
- fix     bug fix
- refactor  code or config change (neither feature nor fix)
- docs    ONLY README, docs/, docstrings
- test    test files only
- chore   deps, CI, build system, configs
- style   formatting, linting, whitespace only
- perf    performance improvement
- ci      CI/CD only
- build   build system only

- Changing comments, prompt text, or config → refactor, NOT docs
- Changing tests → test, NOT refactor

Always use imperative mood: add, fix, update, remove, refactor.
Never: added, adds, adding, fixes, fixed, removes.

One line. Max 72 chars. Lowercase for scope and description.
No body, no bullet list, no extra text.

Write like a human describing the change. Be concise.

Answer ONLY the commit message. No backticks, no markdown."""


def build_messages(
    diff: str, recent_commits: list[str]
) -> list[ChatCompletionMessageParam]:
    context = "\n".join(recent_commits) if recent_commits else "(no recent commits)"

    user_prompt = f"""Recent commits for context:
{context}

Staged diff:
```diff
{diff}
```"""

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
