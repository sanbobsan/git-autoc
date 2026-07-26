
run:
	uv run -m autocommit

format:
	uv run ruff check --select I --fix src/
	uv run ruff check --fix src/
	uv run ruff format src/

test:
	uv run pytest -v

check:
	uv run ty check src/
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/
