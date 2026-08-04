from pathlib import Path

from pydantic import BaseModel

REQUIRED = ("openai_base_url", "openai_model")

CONFIG_DIR = Path.home() / ".config" / "git-autoc"
CONFIG_PATH = CONFIG_DIR / "config.toml"

_STR_KEYS = ("openai_base_url", "openai_model", "openai_api_key")
_INT_KEYS = ("openai_max_tokens",)
_FLOAT_KEYS = ("openai_temperature",)

_COMMENTS: dict[str, str] = {
    "openai_base_url": "Base URL of the OpenAI-compatible API",
    "openai_model": "Model name to use",
    "openai_api_key": "API key (leave empty for local providers)",
    "openai_temperature": "Sampling temperature (0-1, lower is more deterministic)",
    "openai_max_tokens": "Maximum tokens to generate in the response",
}


class ConfigError(RuntimeError):
    pass


class Settings(BaseModel):
    openai_base_url: str = "http://localhost:11434/v1"
    openai_model: str = "model"
    openai_api_key: str = ""
    openai_temperature: float = 0.2
    openai_max_tokens: int = 512


def _toml_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def load_settings() -> Settings:
    if not CONFIG_PATH.exists():
        return Settings()
    try:
        with CONFIG_PATH.open("rb") as f:
            import tomllib

            data = tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError) as e:
        raise ConfigError(f"Failed to read config file {CONFIG_PATH}: {e}") from e
    return Settings(**data)


def validate_settings(settings: Settings) -> None:
    missing = [key for key in REQUIRED if not getattr(settings, key)]
    if missing:
        hints = " ".join(f"`git autoc config set {key}`" for key in missing)
        raise ConfigError(f"Missing required config: {', '.join(missing)}. Run {hints}")


def create_default_config() -> str:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    settings = load_settings()
    lines = ["# git-autoc configuration", ""]
    for key, value in settings.model_dump().items():
        comment = _COMMENTS.get(key, "")
        if isinstance(value, str):
            rendered = _toml_string(value)
        else:
            rendered = str(value)
        lines.append(f"{key} = {rendered}  # {comment}".rstrip())
    CONFIG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(CONFIG_PATH)


def set_config_value(key: str, value: str) -> None:
    if key not in Settings.model_fields:
        raise ConfigError(
            f"Unknown config key '{key}'. Known: {', '.join(Settings.model_fields)}"
        )
    if key in _INT_KEYS:
        try:
            parsed: str | int | float = int(value)
        except ValueError as e:
            raise ConfigError(f"'{key}' expects an integer, got '{value}'") from e
    elif key in _FLOAT_KEYS:
        try:
            parsed = float(value)
        except ValueError as e:
            raise ConfigError(f"'{key}' expects a number, got '{value}'") from e
    else:
        parsed = value
    if not CONFIG_PATH.exists():
        create_default_config()
    lines = CONFIG_PATH.read_text(encoding="utf-8").splitlines()
    rendered = _toml_string(value) if isinstance(parsed, str) else str(parsed)
    comment = _COMMENTS.get(key, "")
    out = []
    replaced = False
    for line in lines:
        if line.startswith(f"{key} =") and not line.lstrip().startswith("#"):
            out.append(f"{key} = {rendered}  # {comment}".rstrip())
            replaced = True
        else:
            out.append(line)
    if not replaced:
        out.append(f"{key} = {rendered}  # {comment}".rstrip())
    CONFIG_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")


settings = load_settings()
