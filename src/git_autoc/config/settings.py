from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    config_dir: Path
    """Folder where placed settings and prompt templates."""
