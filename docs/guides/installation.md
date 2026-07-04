# Installation

This guide explains how to set up the framework for local development, testing, and future production use.

## Requirements

Before installing AAPP‑MART, ensure your environment meets the following requirements:

- Python 3.11+
- Go 1.21+
- C++17+
- Node.js 18+ (frontend / visualization layer)
- Docker
- Kubernetes (for deployment)
- YAML / JSON-based configuration ecosystem

## 1. Clone the Repository

Use Git to clone the AAPP‑MART repository:

```bash
# Clone repository
git clone https://github.com/secwexen/aapp-mart.git
cd aapp-mart
```

## 2. Create a Virtual Environment (Recommended)

Creating a virtual environment keeps dependencies isolated.

### Using `venv`:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

## 3. Install Dependencies

Install all required Python packages:

```bash
# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements-dev.txt
```
