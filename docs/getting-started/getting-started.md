# Getting Started

This guide will help you quickly set up and start using the AAPP-MART system for authorized security assessment and analysis.

## 1. Clone the Repository

Clone the repository and move into the project directory:

```bash
# Clone repository
git clone https://github.com/secwexen/aapp-mart.git
cd aapp-mart
```

## 2. Review the Repository Structure

The main project components are organized as follows:

```text
docs/                 # Project documentation
tests/                # Automated tests
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

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Install the project development dependencies:

```bash
pip install -r requirements-dev.txt
```

## 5. Run the Test Suite

Run the automated tests before making changes:

```python
pytest -m pytest -v
```