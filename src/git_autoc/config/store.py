from platformdirs import PlatformDirs

from git_autoc.config.settings import Settings


def get_settings() -> Settings:
    dirs = PlatformDirs("git_autoc")

    return Settings(config_dir=dirs.user_config_path)
