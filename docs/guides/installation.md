# Installation

This guide explains how to set up the framework for local development, testing, and future production use.

## Requirements

Before installing AAPP‑MART, ensure your environment meets the following requirements:

- Python **3.11**

## 1. Clone the Repository

Use Git to clone the AAPP‑MART repository:

```bash
git clone https://github.com/secwexen/aapp-mart.git
cd aapp-mart
```

## 2. Create a Virtual Environment (Recommended)

Creating a virtual environment keeps dependencies isolated.

### Using `venv`:

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

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