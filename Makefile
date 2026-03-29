# Makefile for AAPP-MART
.PHONY: all test lint format typecheck security dev clean

# Default: run tests
all: test

# Run unit tests with coverage
test:
	nox -s tests

# Run linting (flake8)
lint:
	nox -s lint

# Auto format code (black + isort)
format:
	nox -s format

# Static type checking (mypy)
typecheck:
	nox -s typecheck

# Security checks (bandit + safety)
security:
	nox -s security

# Setup development environment
dev:
	nox -s dev

# Clean pycache and temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".nox" -exec rm -rf {} +
