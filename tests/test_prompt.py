from autocommit.llm.prompt import build_messages


def test_build_messages_structure() -> None:
    diff = "diff --git a/test.txt b/test.txt\n+hello"
    commits = ["feat: previous commit"]
    messages = build_messages(diff, commits)

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"


def test_build_messages_system_prompt() -> None:
    diff = ""
    messages = build_messages(diff, [])
    system = messages[0]["content"]
    assert isinstance(system, str)
    assert "conventional commit" in system.lower()
    assert "type(scope)" in system
    assert "feat" in system
    assert "fix" in system


def test_build_messages_user_prompt_contains_diff() -> None:
    diff = "+new code here"
    commits = ["fix: bug fix"]
    messages = build_messages(diff, commits)
    user = messages[1]["content"]
    assert isinstance(user, str)
    assert diff in user


def test_build_messages_user_prompt_contains_commits() -> None:
    diff = ""
    commits = ["feat: feature one", "fix: bug fix"]
    messages = build_messages(diff, commits)
    user = messages[1]["content"]
    assert isinstance(user, str)
    for c in commits:
        assert c in user


def test_build_messages_empty_commits() -> None:
    diff = ""
    messages = build_messages(diff, [])
    user = messages[1]["content"]
    assert isinstance(user, str)
    assert "no recent commits" in user.lower()
