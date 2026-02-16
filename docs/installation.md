# Installation

AAPP‑MART is currently under active development.  
This guide explains how to set up the framework for local development, testing, and future production use.

---

## Requirements

Before installing AAPP‑MART, ensure your environment meets the following requirements:

- Python 3.10 or higher  
- pip (Python package manager)  
- Git (for cloning the repository)  
- Recommended: virtual environment (venv, conda, or similar)

---

## 1. Clone the Repository

Use Git to clone the AAPP‑MART repository:

```bash
git clone https://github.com/secwexen/aapp-mart.git
cd aapp-mart
```

---

## 2. Create a Virtual Environment (Recommended)

Creating a virtual environment keeps dependencies isolated.

### Using `venv`:

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### Using Conda:

```bash
conda create -n aapp-mart python=3.10
conda activate aapp-mart
```

---

## 3. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

If you are developing the framework, install it in editable mode:

```bash
pip install -e .
```

This allows you to modify the source code without reinstalling.

---

## 4. Running the Framework

Once installed, you can test the framework using the example scripts:

```bash
python examples/basic_usage.py
```

Or run the CLI:

```bash
python -m aappmart.cli.aappmart_cli
```

---

## 5. Running Tests

AAPP‑MART includes a full test suite under the `tests/` directory.

Run all tests with:

```bash
pytest
```

If `pytest` is not installed:

```bash
pip install pytest
```

---

## Development Mode

If you plan to contribute or extend the framework:

1. Keep your virtual environment active  
2. Install dev dependencies (optional):

```bash
pip install -r requirements-dev.txt
```

3. Follow the project structure under `src/aapp_mart/`

---

## Future Installation (PyPI)

Once the first stable release is published, AAPP‑MART will be installable via PyPI:

```bash
pip install aapp-mart
```

This section will be updated when the package becomes publicly available.

---

## Troubleshooting

Common issues:

### **ModuleNotFoundError**
Ensure you installed the project in editable mode:

```bash
pip install -e .
```

### **Python version mismatch**
Verify your Python version:

```bash
python --version
```

### **Virtual environment not activated**
Activate your environment again:

```bash
source venv/bin/activate
```

---

AAPP‑MART is evolving rapidly.  
Installation steps will be updated as new components, APIs, and modules are introduced.
