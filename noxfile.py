import nox

PYTHON_VERSIONS = ["3.11"]

@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    """Run unit tests with coverage."""
    session.install("-r", "requirements.txt")
    session.install("-r", "dev-requirements.txt")
    session.install("pytest", "pytest-cov")
    session.run("pytest", "--cov=.", "--cov-report=term-missing")

@nox.session
def lint(session):
    """Run linting (flake8)."""
    session.install("-r", "dev-requirements.txt")
    session.run("flake8", "src", "tests")

@nox.session
def format(session):
    """Auto format code (black + isort)."""
    session.install("-r", "dev-requirements.txt")
    session.run("black", ".")
    session.run("isort", ".")

@nox.session
def typecheck(session):
    """Run static type checking with mypy."""
    session.install("-r", "dev-requirements.txt")
    session.install("mypy")
    session.run("mypy", "src")

@nox.session
def security(session):
    """Run security checks (bandit + safety)."""
    session.install("-r", "dev-requirements.txt")
    session.install("bandit", "safety")
    session.run("bandit", "-r", "src")
    session.run("safety", "check")

@nox.session
def dev(session):
    """Setup development environment."""
    session.install("-r", "requirements.txt")
    session.install("-r", "dev-requirements.txt")
    session.install(
        "pytest", "black", "isort", "flake8", "mypy", "bandit"
    )
