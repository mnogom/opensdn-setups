install-uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh
	
install-deps:
	./deps/install-api-client.sh

install-req:
	uv sync --dev

install: install-uv install-req install-deps

lint:
	uv run isort ./*.py ./src
	uv run ruff format
