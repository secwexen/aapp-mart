from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
requirements_path = this_directory / "requirements.txt"

with open(requirements_path, "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="aapp-mart",
    author="Secwexen",
    description="Autonomous Offensive Security Engine — AI-driven attack path prediction & multi-agent red team simulation",
    long_description=(this_directory / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/secwexen/aapp-mart",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires='>=3.10',
    install_requires=requirements,
    include_package_data=True,  
    package_data={
        "aapp_mart": [
            "data/models/*",
            "data/samples/*",
            "cli/data/attack_signatures.json",
            "cli/data/sample_targets/*",
            "mart/behaviors/*.py",
            "reports/templates/*"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security :: Penetration Testing",
    ],
    entry_points={
        "console_scripts": [
            "aapp-mart= aapp_mart.cli.aappmart_cli:main",  
        ],
    },
)
