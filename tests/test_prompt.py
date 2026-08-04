from git_autoc.llm.prompt import build_messages
from git_autoc.llm.style import BodyStyle, CommitStyle


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


def test_style_none_forbids_body() -> None:
    diff = ""
    messages = build_messages(diff, [], style=CommitStyle(body=BodyStyle.NONE))
    system = messages[0]["content"]
    assert "No body" in system
    assert "bullet list" in system


def test_style_long_allows_body() -> None:
    diff = ""
    messages = build_messages(diff, [], style=CommitStyle(body=BodyStyle.LONG))
    system = messages[0]["content"]
    assert "Body is optional" in system


def test_style_list_forces_bullets() -> None:
    diff = ""
    messages = build_messages(diff, [], style=CommitStyle(body=BodyStyle.LIST))
    system = messages[0]["content"]
    assert "bullet list" in system
    assert "Always add a body" in system


def test_style_desc_forces_paragraph() -> None:
    diff = ""
    messages = build_messages(diff, [], style=CommitStyle(body=BodyStyle.DESC))
    system = messages[0]["content"]
    assert "single paragraph" in system


def test_style_max_chars_respected() -> None:
    diff = ""
    messages = build_messages(
        diff, [], style=CommitStyle(body=BodyStyle.NONE, max_chars=100)
    )
    system = messages[0]["content"]
    assert "100 chars" in system
    assert "No body" in system


def test_default_style_is_none() -> None:
    diff = ""
    messages = build_messages(diff, [])
    system = messages[0]["content"]
    assert "No body" in system
    assert "bullet list" in system
