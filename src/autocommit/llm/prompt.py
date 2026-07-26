from openai.types.chat import ChatCompletionMessageParam

from autocommit.llm.style import BodyStyle, CommitStyle

_BASE = """You generate conventional git commit messages from diffs.

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

Write like a human describing the change. Be concise.

Always respond with a commit message, even for trivial changes.
Never return an empty response. Describe exactly what changed.

Answer ONLY the commit message. No backticks, no markdown."""

_BODY_RULES: dict[BodyStyle, str] = {
    BodyStyle.NONE: "One line. Max {max_chars} chars. Lowercase for scope and description.\nNo body, no bullet list, no extra text.",
    BodyStyle.LONG: "Body is optional. If the change is worth explaining, add a blank line after the title, then a short paragraph or bullet list. Let the change itself decide the format.\nFirst line max {max_chars} chars.",
    BodyStyle.LIST: "Always add a body with bullet list. Title first (max {max_chars} chars), blank line, then bullet list.\nStart each bullet with lowercase, use imperative mood.",
    BodyStyle.DESC: "Always add a body as a single paragraph. Title first (max {max_chars} chars), blank line, then a few sentences describing the change concisely.",
}


def _build_system_prompt(style: CommitStyle) -> str:
    rule = _BODY_RULES[style.body].format(max_chars=style.max_chars)
    return f"{_BASE}\n\n{rule}"


def build_messages(
    diff: str,
    recent_commits: list[str],
    changed_files: list[str] | None = None,
    style: CommitStyle | None = None,
) -> list[ChatCompletionMessageParam]:
    style = style or CommitStyle()
    context = "\n".join(recent_commits) if recent_commits else "(no recent commits)"

    parts = [f"Recent commits for context:\n{context}"]
    if changed_files:
        parts.append("Changed files:\n" + "\n".join(f"  {f}" for f in changed_files))
    parts.append(f"Staged diff:\n```diff\n{diff}\n```")
    user_prompt = "\n\n".join(parts)

    return [
        {"role": "system", "content": _build_system_prompt(style)},
        {"role": "user", "content": user_prompt},
    ]
