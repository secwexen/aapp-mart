# AAPP-MART Examples

This document provides installation instructions, environment setup, and example usage for AAPP-MART.

---

## Installation

```bash
# 1. Clone repository
git clone https://github.com/secwexen/aapp-mart.git
cd aapp-mart

# 2. (Optional but recommended) Create a virtual environment 
# Linux / macOS
python3 -m venv venv  
source venv/bin/activate  

# Windows (PowerShell)
python -m venv venv  
venv\Scripts\activate  

# 3. Install dependencies
pip install -r requirements.txt
```

> Note: Some modules may be under active development. Functionality may be limited.

---

## Environment Configuration

AAPP-MART uses environment variables for configuration.
For local development, copy the example file and adjust values as needed:

```bash
cp .env.example .env
```

> Never commit your real `.env` file, as it may contain sensitive or environment‑specific information.

---

## Quick Start Example

```python
from aapp_mart.core.orchestrator import AAPP_MART

engine = AAPP_MART(target="192.168.1.10")
engine.run()
report = engine.get_report()
print(report)
```

> Note: Example is for demonstration purposes. Some features may not yet be fully implemented.

---

## CLI / API Usage Examples

### Run an attack simulation

```bash
aapp-mart run --target 192.168.1.10
```

### Generate a prediction-only report

```bash
aapp-mart predict --input data/target_profile.json --output report.txt
```

### List available modules

```bash
aapp-mart modules list
```

> See the [CLI documentation](docs/cli.md) for all available commands and advanced options.
