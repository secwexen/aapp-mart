# Quickstart

This quickstart file helps you run your first AAPP-MART request in under 5 minutes.

## 1. Clone & Setup

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

### 2. Run the API

Start the local API server:

```bash
uvicorn aapp_mart.api.app:app --app-dir src --host 127.0.0.1 --port 8000
```

The API will be available at:

- **Health Check:** `http://127.0.0.1:8000/health`
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`
- **OpenAPI Schema:** `http://127.0.0.1:8000/openapi.json`

The API binds to `127.0.0.1` by default and is accessible only from the local machine.

### 2. Run Tests

```python
# Run the full pytest suite
python -m pytest -v
```
