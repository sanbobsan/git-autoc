
run:
	uv run -m git_autoc

format:
	uv run ruff check --select I --fix src/ tests/
	uv run ruff check --fix src/ tests/
	uv run ruff format src/ tests/

test:
	uv run pytest -v

check:
	uv run ty check src/
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/

install:
	uv sync
