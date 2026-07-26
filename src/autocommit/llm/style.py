from dataclasses import dataclass
from enum import Enum


class BodyStyle(str, Enum):
    NONE = "none"
    LONG = "long"
    LIST = "list"
    DESC = "desc"


@dataclass
class CommitStyle:
    body: BodyStyle = BodyStyle.NONE
    max_chars: int = 80
