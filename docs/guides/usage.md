# Usage Guide

This guide explains the intended usage workflow for AAPP-MART, including input preparation, attack-path analysis, simulation, and result handling.

The system is designed for authorized security assessments, controlled testing environments, cybersecurity research, and defensive security validation.

## Prerequisites

Before using AAPP-MART, verify that the environment meets the project's requirements.

### Requirements

- Python 3.13+
- pip for Python dependency installation
- Make for repository automation and common development tasks
- Git for repository management
- Pytest for automated testing and validation

### Optional Components

- Docker: Used for containerized labs, and testing.

Linux is recommended for development and deployment. Windows environments can use Visual Studio Code and WSL2, while macOS is supported for local development and testing.

For additional details, consult the [Installation Guide](docs/getting-started/installation.md).

## Install Python

The project requires Python 3.13 or later.

Check the installed version:

```python
python --version
```

or:

```python
python3 --version
```

Install Python 3.13+ if the required version is not available.

## Install Dependencies

Create a virtual environment:

```python
python -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install AAPP-MART:

```bash
python -m pip install .
```

Install the development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Run the Test Suite

Run the automated tests before making changes:

```python
pytest -m pytest -v
```

Alternatively, use the Makefile target:

```bash
make test
```

The test command uses the project's configured pytest options, including coverage reporting.
