# Getting Started

This guide will help you quickly set up and start using the AAPP-MART system for authorized security assessment and analysis.

## 1. Clone the Repository

Use Git to clone the AAPP‑MART repository:

```bash
# Clone repository
git clone https://github.com/secwexen/aapp-mart.git
cd aapp-mart
```

## 2. Create a Virtual Environment (Recommended)

Creating a virtual environment keeps dependencies isolated.

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate     # Linux/Mac
.\.venv\Scripts\Activate.ps1  # Windows
```

## 3. Install Dependencies

Install all required Python packages:

```bash
# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements-dev.txt
```