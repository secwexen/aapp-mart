# Modules and Dependencies

This document describes the main third-party libraries used by AAPP-MART and their intended roles within the project.

## Core Analytics and Graph Processing

- **NetworkX** – Graph representation, traversal, and graph analysis.
- **NumPy / SciPy** – Numerical computing and scientific calculations.
- **Pandas** – Data manipulation and analysis.
- **Scikit-learn** – Machine learning utilities and predictive modeling.
- **Joblib** – Serialization and persistence of supported Python objects and models.
- **PyTorch / Transformers** – Machine learning and deep learning capabilities.
- **Graphviz** – Graph rendering and visualization support.

## API and Application Server

- **FastAPI** – Framework for building APIs.
- **Uvicorn** – ASGI server for running the API.
- **Gunicorn** – Application server used for supported deployment configurations.
- **AnyIO / Sniffio** – Asynchronous I/O support and asynchronous environment detection.

## Data Validation and Configuration

- **Pydantic** – Data validation and schema definition.
- **PyYAML** – YAML configuration parsing.
- **Python-dotenv** – Loading configuration values from environment files.
- **Orjson** – High-performance JSON serialization and deserialization.

## Networking and External Data Sources

- **HTTPX / Requests** – HTTP clients for communicating with external services and public data sources.

These libraries can support public vulnerability data retrieval and threat intelligence workflows where the corresponding functionality is implemented.

## CLI and Visualization

- **Rich** – Enhanced terminal output and formatting.
- **TQDM** – Progress indicators for supported operations.
- **Matplotlib / Seaborn** – Data visualization and plotting.
- **Pillow** – Image processing.

## Security and Cryptography

- **Cryptography** – Cryptographic primitives and security-related utilities.
- **PyOpenSSL** – OpenSSL-based cryptographic and TLS functionality.

## Testing

- **Pytest** – Automated testing framework.
- **Pytest-asyncio** – Support for testing asynchronous code.
- **Pytest-cov** – Test coverage reporting.
- **Pytest-xdist** – Parallel test execution.

## Development and Code Quality

- **Ruff** – Linting, import sorting, and supported static security checks.
- **Black** – Code formatting.
- **Mypy** – Static type checking.
- **Pre-commit** – Git hooks for running configured checks before commits.
- **Build** – Building Python distribution packages.
- **Loguru** – Logging utilities.

## Dependency Management

Project dependencies are declared in `pyproject.toml`.

Runtime dependencies are listed under `[project.dependencies]`, while development and testing tools are listed under `[project.optional-dependencies].dev`.

The presence of a dependency does not necessarily mean that every capability it supports has been implemented or integrated into AAPP-MART.

Documentation should be updated as dependencies and implemented functionality evolve.
