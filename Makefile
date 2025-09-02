.PHONY: 
	lint 
	build

lint:
	uv run ruff check --fix
	uv run ruff format
	uv run ty check

build:
	uv build