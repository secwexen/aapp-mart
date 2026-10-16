# Quickstart

This quickstart file helps you run your first AAPP-MART request in under 5 minutes.

## Clone & Setup

```bash
# Clone repository
git clone https://github.com/secwexen/aapp-mart.git
cd aapp-mart

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate     # Linux/Mac
.\.venv\Scripts\Activate.ps1  # Windows

# Install AAPP-MART
python -m pip install .

# Install the development dependencies
python -m pip install -e ".[dev]"
```

### 2. Run Tests

```python
# Run the full pytest suite
python -m pytest -v
```
