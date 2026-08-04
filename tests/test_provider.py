import httpx
import pytest
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
)

from git_autoc.llm import provider
from git_autoc.llm.provider import generate


class FakeMessage:
    def __init__(self, content: str) -> None:
        self.content = content


class FakeChoice:
    def __init__(self, content: str) -> None:
        self.message = FakeMessage(content)


class FakeResponse:
    def __init__(self, content: str) -> None:
        self.choices = [FakeChoice(content)]


class FakeCompletions:
    def __init__(self, results: list) -> None:
        self.results = results
        self.index = 0

    def create(self, **kwargs):
        result = self.results[self.index]
        self.index += 1
        if isinstance(result, Exception):
            raise result
        return result


class FakeChat:
    def __init__(self, completions: FakeCompletions) -> None:
        self.completions = completions


class FakeClient:
    def __init__(self, completions: FakeCompletions) -> None:
        self.chat = FakeChat(completions)


def patch_client(monkeypatch: pytest.MonkeyPatch, completions: FakeCompletions) -> None:
    monkeypatch.setattr(provider, "OpenAI", lambda **kwargs: FakeClient(completions))


def make_error(error_type: type, status_code: int = 500) -> Exception:
    request = httpx.Request("POST", "http://localhost:11434/v1")
    if error_type in (APIConnectionError, APITimeoutError):
        return error_type(request=request)
    response = httpx.Response(status_code, request=request)
    return error_type("error", response=response, body=None)


def test_generate_returns_content(monkeypatch: pytest.MonkeyPatch) -> None:
    completions = FakeCompletions([FakeResponse("feat: add feature")])
    patch_client(monkeypatch, completions)
    assert generate([]) == "feat: add feature"


def test_generate_retries_on_empty_then_succeeds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    completions = FakeCompletions([FakeResponse(""), FakeResponse("feat: add feature")])
    patch_client(monkeypatch, completions)
    assert generate([]) == "feat: add feature"


def test_generate_empty_after_two_attempts(monkeypatch: pytest.MonkeyPatch) -> None:
    completions = FakeCompletions([FakeResponse(""), FakeResponse("")])
    patch_client(monkeypatch, completions)
    with pytest.raises(RuntimeError, match="Empty response"):
        generate([])


def test_generate_connection_error(monkeypatch: pytest.MonkeyPatch) -> None:
    completions = FakeCompletions([make_error(APIConnectionError)])
    patch_client(monkeypatch, completions)
    with pytest.raises(RuntimeError, match="Could not reach the API"):
        generate([])


def test_generate_timeout_error(monkeypatch: pytest.MonkeyPatch) -> None:
    completions = FakeCompletions([make_error(APITimeoutError)])
    patch_client(monkeypatch, completions)
    with pytest.raises(RuntimeError, match="Could not reach the API"):
        generate([])


def test_generate_model_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    completions = FakeCompletions([make_error(NotFoundError, 404)])
    patch_client(monkeypatch, completions)
    with pytest.raises(RuntimeError, match="not found"):
        generate([])


def test_generate_auth_error(monkeypatch: pytest.MonkeyPatch) -> None:
    completions = FakeCompletions([make_error(AuthenticationError, 401)])
    patch_client(monkeypatch, completions)
    with pytest.raises(RuntimeError, match="API key"):
        generate([])


def test_generate_rate_limit_error(monkeypatch: pytest.MonkeyPatch) -> None:
    completions = FakeCompletions([make_error(RateLimitError, 429)])
    patch_client(monkeypatch, completions)
    with pytest.raises(RuntimeError, match="rate limiting"):
        generate([])


def test_generate_generic_status_error(monkeypatch: pytest.MonkeyPatch) -> None:
    completions = FakeCompletions([make_error(APIStatusError, 503)])
    patch_client(monkeypatch, completions)
    with pytest.raises(RuntimeError, match="status 503"):
        generate([])
