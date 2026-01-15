from setuptools import setup, find_packages

setup(
    name="aappmart",
    version="0.1.0",
    description="Autonomous Attack Path Prediction & Multi-Agent Red Team Engine",
    author="secwexen",
    packages=find_packages(),
    install_requires=[
        "networkx",
        "numpy",
        "pandas",
        "scikit-learn",
        "fastapi",
        "uvicorn",
        "rich",
        "pyyaml"
    ],
    python_requires=">=3.10",
)
