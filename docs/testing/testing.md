# Testing

This document describes how to run tests for AAPP-MART and verify the behavior of its core components.

## Testing Requirements

Before running the test suite, install the project and development

### Install Dependencies

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

## Run Tests

Run the complete test suite:

```python
python -m pytest -v
```
