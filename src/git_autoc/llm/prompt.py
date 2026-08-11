from openai.types.chat import ChatCompletionMessageParam

from git_autoc.llm.style import BodyStyle, CommitStyle

_BASE = """You are an expert developer generating conventional git commit messages from staged diffs.
Output ONLY the commit message. No explanations, no prefixes, no backticks, no markdown.
Always respond with a commit message, even for trivial changes. Never return an empty response.

FORMAT: type(scope): short description

RULES:
1. Imperative mood: use "add", "fix", "update", "remove", "refactor". Never use "added", "adds", "fixed", etc.
2. Scope: derive it from the primary changed component (e.g., module, folder, or file name). Keep it lowercase and short. Omit scope if changes are global.
3. Be concise and describe exactly what changed. Do not just list changed files.
4. Lists: If you generate a bullet list in the body, start each item with a lowercase letter and use imperative mood.

TYPES:
- feat:     new feature or enhancement
- fix:      bug fix
- refactor: code restructuring (no behavior changes). NOT for configs.
- docs:     documentation, README, or docstrings ONLY. (Comments/prompts = refactor/chore)
- test:     adding or modifying tests ONLY.
- chore:    deps, configs, build system, minor routine tasks.
- style:    formatting, linting, whitespace ONLY (no code logic changes).
- perf:     performance improvement
- ci:       CI/CD pipeline changes
- build:    build system changes (npm, poetry, docker)"""

_BODY_RULES: dict[BodyStyle, str] = {
    BodyStyle.NONE: "One line. Max {max_chars} chars. Lowercase for scope and description.\nNo body, no bullet list, no extra text.",
    BodyStyle.LONG: "Body is optional. If the change is worth explaining, add a blank line after the title, then a short paragraph or bullet list. Let the change itself decide the format.\nFirst line max {max_chars} chars.",
    BodyStyle.LIST: "Always add a body with a bullet list. Title first (max {max_chars} chars), blank line, then the bullet list.",
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
