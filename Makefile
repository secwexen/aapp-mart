.PHONY: all check test lint format typecheck security dev clean build docs

# Default target
all: check

# Run all quality checks
check: lint typecheck security test

# Run tests with coverage
test:
	python -m pytest --cov=aapp_mart --cov-report=term-missing

# Run linting and check formatting
lint:
	python -m ruff check src/aapp_mart tests scripts demo
	python -m black --check src/aapp_mart tests scripts demo

# Auto-fix import ordering and format code
format:
	python -m ruff check --select I --fix src/aapp_mart tests scripts demo
	python -m black src/aapp_mart tests scripts demo

# Static type checking
typecheck:
	python -m mypy src/aapp_mart

# Security-focused static analysis
security:
	python -m ruff check --select S src/aapp_mart tests

# Install development dependencies and Git hooks
dev:
	python -m pip install -e ".[dev]"
	pre-commit install

# Build distribution packages
build:
	python -m build

# Build local project documentation
docs:
	bash scripts/dev/build_docs.sh

# Clean caches, coverage reports, and build artifacts
clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -prune -exec rm -rf {} +
	find . -type d -name "htmlcov" -prune -exec rm -rf {} +
	find . -type d -name "dist" -prune -exec rm -rf {} +
	find . -type d -name "build" -prune -exec rm -rf {} +
	find . -type d -name "*.egg-info" -prune -exec rm -rf {} +
	rm -f .coverage coverage.xml
