.PHONY: install test lint format build clean

install:
    pip install -r requirements.txt

test:
    pytest -q

lint:
    pylint aappmart || true

format:
    black aappmart

build:
    python -m build

clean:
    rm -rf build dist *.egg-info
