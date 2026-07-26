from openai.types.chat import ChatCompletionMessageParam

SYSTEM_PROMPT = """You are a git commit message generator. Generate conventional commit messages based on the provided diff.

Format: type(scope): description

Types: feat, fix, chore, docs, refactor, test, style, perf, ci, build
- feat: a new feature
- fix: a bug fix
- chore: maintenance, dependencies, config
- docs: documentation only
- refactor: code change that neither fixes a bug nor adds a feature
- test: adding or updating tests
- style: formatting, linting, whitespace
- perf: performance improvement
- ci: CI/CD changes
- build: build system or external dependency changes

Rules:
- First line max 80 characters
- Use imperative mood in the description
- Scope is optional, use lowercase
- If a longer body is needed, add a blank line after the subject
- Bullet points in body use - or *
- Answer ONLY with the commit message, no extra text"""


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
