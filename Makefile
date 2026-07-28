.PHONY: all test lint format typecheck security dev clean build docs

# Default: run tests
all: test

# Run unit tests with coverage and JSON report
test: nox -s tests

# Run linting (flake8, ruff)
lint: nox -s lint

# Auto format code (black + isort + ruff format)
format: nox -s format

# Static type checking (mypy)
typecheck: nox -s typecheck

# Security checks (bandit + safety)
security: nox -s security

# Setup development environment and install pre-commit hooks
dev:
	nox -s dev
	poetry run pre-commit install || pip install pre-commit && pre-commit install

# Build distribution packages
build: python -m build

# Build local project documentation
docs: nox -s docs

# Clean pycache, temporary files, build artifacts, and cache directories
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".nox" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +