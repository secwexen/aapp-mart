# Getting Started

This guide will help you quickly set up and start using the AAPP-MART for authorized security assessment and analysis.

## 1. Clone the Repository

Clone the repository and move into the project directory:

```bash
git clone https://github.com/secwexen/aapp-mart.git
cd aapp-mart
```

## 2. Review the Repository Structure

The main project components are organized as follows:

```text
├── docs/                 # Project documentation
├── src/aapp_mart/        # Application source code
├── tests/                # Automated tests
├── Makefile              # Development and build commands
└── pyproject.toml        # Project and tool configuration
```

## 3. Install Python

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

## 4. Install Dependencies

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

## 5. Run the Test Suite

Run the automated tests before making changes:

```python
pytest -m pytest -v
```

Alternatively, use the Makefile target:

```bash
make test
```

The test command uses the project's configured pytest options, including coverage reporting.

## 6. Run Code Quality Checks

Run linting and formatting checks:

```bash
make lint
```

This checks the code using the tools configured in the project.

To apply formatting and automatically fix supported import-order issues:

```bash
make format
```

## 7. Build the Package

Build the distribution packages:

```bash
make build
```

The generated distribution files are placed in the `dist/` directory.
