from __future__ import annotations

import re
from dataclasses import dataclass

BLOCK_RE = re.compile(r"\{(\w+)(?::(\w+))?\}")

TemplateStr = str


@dataclass(frozen=True)
class Block:
    name: str
    param: str | None = None


class Template:
    def __init__(self, raw_template: TemplateStr):
        self.raw_template: TemplateStr = raw_template
        self.complete_template: str | None = None

    def get_blocks(self) -> list[Block]:
        """Extract all blocks {name:param} from the template string."""
        return [
            Block(name, param or None)
            for name, param in BLOCK_RE.findall(self.raw_template)
        ]

    def render(self, values: dict[Block, str]) -> str:
        """Substitute block values into the template."""

        def replace_match(match: re.Match[str]) -> str:
            name = match.group(1)
            param = match.group(2) or None

            block = Block(name, param)
            if block in values:
                return values[block]

            return match.group(0)

        self.complete_template = BLOCK_RE.sub(replace_match, self.raw_template)
        return self.complete_template
