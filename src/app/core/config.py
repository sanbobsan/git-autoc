from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # required
    openai_base_url: str
    openai_model: str
    openai_api_key: str
    # not required
    openai_temperature: float = 0.2
    openai_max_tokens: int = 512

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
