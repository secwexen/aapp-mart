.PHONY: install install-dev test lint format build clean run

install:
    pip install -r requirements.txt

install-dev:
    pip install -r requirements.txt
    pip install -r requirements-dev.txt

test:
    pytest --cov=. --maxfail=1 -q

lint:
    pylint $(git ls-files '*.py')

format:
    black .
    isort .
    autoflake --remove-unused-variables --in-place --recursive .

build:
    python -m build

clean:
    rm -rf build dist *.egg-info
    find . -type d -name "__pycache__" -exec rm -rf {} +

run:
    python -m aappmart
