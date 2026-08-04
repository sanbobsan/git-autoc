from pathlib import Path

import pytest

from autocommit.core import config as config_module
from autocommit.core.config import (
    ConfigError,
    Settings,
    create_default_config,
    load_settings,
    set_config_value,
    validate_settings,
)


@pytest.fixture
def isolated_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "config.toml"
    monkeypatch.setattr(config_module, "CONFIG_PATH", path)
    monkeypatch.setattr(config_module, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(config_module, "settings", load_settings())
    return path


def test_defaults_when_no_file(isolated_config: Path) -> None:
    settings = load_settings()
    assert settings.openai_base_url == "http://localhost:11434/v1"
    assert settings.openai_model == "model"
    assert settings.openai_temperature == 0.2
    assert settings.openai_max_tokens == 512


def test_create_default_config_writes_file(isolated_config: Path) -> None:
    path = create_default_config()
    assert Path(path) == isolated_config
    assert isolated_config.exists()
    content = isolated_config.read_text(encoding="utf-8")
    assert "openai_base_url" in content
    assert "openai_model" in content


def test_load_settings_from_file(isolated_config: Path) -> None:
    isolated_config.write_text(
        'openai_base_url = "http://example.com"\n'
        'openai_model = "gpt-test"\n'
        "openai_temperature = 0.7\n",
        encoding="utf-8",
    )
    settings = load_settings()
    assert settings.openai_base_url == "http://example.com"
    assert settings.openai_model == "gpt-test"
    assert settings.openai_temperature == 0.7
    assert settings.openai_max_tokens == 512


def test_load_settings_broken_file_raises(isolated_config: Path) -> None:
    isolated_config.write_text("openai_base_url = [unclosed\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_settings()


def test_validate_settings_ok() -> None:
    validate_settings(
        Settings(openai_base_url="http://x", openai_model="m", openai_api_key="k")
    )


def test_validate_settings_missing_required() -> None:
    with pytest.raises(ConfigError, match="openai_base_url"):
        validate_settings(Settings(openai_base_url=""))


def test_validate_settings_api_key_not_required() -> None:
    validate_settings(
        Settings(openai_base_url="http://x", openai_model="m", openai_api_key="")
    )


def test_set_config_value_string(isolated_config: Path) -> None:
    create_default_config()
    set_config_value("openai_model", "gpt-test")
    settings = load_settings()
    assert settings.openai_model == "gpt-test"
    content = isolated_config.read_text(encoding="utf-8")
    assert 'openai_model = "gpt-test"' in content


def test_set_config_value_int(isolated_config: Path) -> None:
    create_default_config()
    set_config_value("openai_max_tokens", "2048")
    assert load_settings().openai_max_tokens == 2048


def test_set_config_value_float(isolated_config: Path) -> None:
    create_default_config()
    set_config_value("openai_temperature", "0.5")
    assert load_settings().openai_temperature == 0.5


def test_set_config_value_bad_int(isolated_config: Path) -> None:
    create_default_config()
    with pytest.raises(ConfigError):
        set_config_value("openai_max_tokens", "abc")


def test_set_config_value_unknown_key(isolated_config: Path) -> None:
    create_default_config()
    with pytest.raises(ConfigError):
        set_config_value("openai_nope", "x")


def test_set_config_value_creates_file(isolated_config: Path) -> None:
    set_config_value("openai_model", "gpt-test")
    assert isolated_config.exists()
    assert load_settings().openai_model == "gpt-test"
