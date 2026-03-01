# Project Modules Overview

This document describes the main modules of the repository and their responsibilities.

## Core Analytics & Graph

- **networkx** → Graph-based algorithms and network analysis.
- **numpy / pandas** → Numerical computing and data manipulation.
- **scikit-learn / joblib** → Machine learning models and persistence.
- **graphviz** → Graph visualization.

## API Layer

- **FastAPI** → RESTful API framework.
- **Uvicorn** → ASGI server for running FastAPI.
- **AnyIO / Sniffio** → Async I/O support.

## Data Validation & Configuration

- **Pydantic** → Data validation and schema management.
- **PyYAML** → Configuration file parsing.
- **Orjson** → High-performance JSON serialization.

## Networking

- **HTTPX / Requests** → HTTP client libraries for external API calls.

## CLI / UX / Visualization

- **Rich / TQDM** → CLI enhancements and progress bars.
- **Matplotlib / Seaborn** → Data visualization.
- **Pillow** → Image processing.

## Development & Tooling

- **Pytest / Coverage / Asyncio** → Testing framework.
- **Pylint / Flake8 / Black / Isort / Autoflake** → Code quality and formatting.
- **Build** → Package building.
- **Loguru** → Advanced logging.
