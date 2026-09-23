.PHONY: all test lint format typecheck security dev clean build docs

# Default: run tests
all: test

# Run unit tests with coverage
test:
	nox -s tests

# Run linting
lint:
	nox -s lint

# Auto-format code
format:
	nox -s format

# Static type checking
typecheck:
	nox -s typecheck

# Security checks
security:
	nox -s security

# Setup development environment and install pre-commit hooks
dev:
	nox -s dev
	pre-commit install

# Build distribution packages
build:
	python -m build

# Build local project documentation
docs:
	nox -s docs

# Clean caches and build artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".nox" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
