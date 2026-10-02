install:
	@echo "--- 🚀 Installing the package ---"
	uv sync

test:
	uv run pytest

lint:
	@echo "--- 🧹 Running linters ---"
	uv run ruff format .
	uv run ruff check . --fix
