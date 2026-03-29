# Installation Guide

This guide provides step-by-step instructions to set up and run the AAPP-MART project on your local machine.

### Supported Operating Systems

- Windows 10 / 11  
- Linux (Ubuntu 22.04+ / Debian 11+ / other Debian-based distributions)  
- macOS (Intel & Apple Silicon)

### Python Requirements

- Python **3.11+**  
- pip 23+  
- Virtual environment recommended

## Quick Start

```bash
# Clone repo
git clone https://github.com/secwexen/aapp-mart.git
cd aapp-mart

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r dev-requirements.txt
```

### **Verify Installation (Optional)**:

Run the test suite to ensure everything is functioning as expected:
```bash
pytest  # Run tests and confirm correct setup
```

## Troubleshooting

- If `pip install` fails, ensure pip is updated:
  ```bash
  pip install --upgrade pip
  ```

- Check the Python version to ensure compatibility:
  ```bash
  python --version
  ```

- For additional guidance or error resolution, refer to the [Troubleshooting Guide](docs/guides/troubleshooting.md).
