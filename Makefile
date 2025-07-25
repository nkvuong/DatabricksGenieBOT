##@ Utility
.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <target>\033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


.PHONY: uv
uv:  ## Install uv if it's not present.
	@command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh

.PHONY: dev
dev: uv ## Install dev dependencies
	uv sync --dev

.PHONY: lock
lock: uv ## lock dependencies
	uv lock

.PHONY: install
install: uv ## Install dependencies
	uv sync --frozen

.PHONY: lint
lint:  ## Run linters
	uv run ruff check ./src ./tests

.PHONY: test
test: uv ## Run tests
	uv run pytest

.PHONY: coverage
coverage: uv ## Run tests with coverage
	uv run pytest --cov=chatx

.PHONY: fix
fix:  ## Fix lint errors
	uv run ruff check ./src ./tests --fix
	uv run ruff format ./src ./tests

.PHONY: build
build:  ## Build package
	uv build
