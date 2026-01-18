# AAPP-MART  

<p align="center">
<img src="docs/logo/aappmart_logo.png?raw=true" width="250" height="250" alt="aappmart_logo">
</p>

![Build](https://img.shields.io/github/actions/workflow/status/secwexen/aappmart/build.yml?label=Build)
![Lint](https://img.shields.io/github/actions/workflow/status/secwexen/aappmart/lint.yml?label=Lint)
![CodeQL](https://img.shields.io/github/actions/workflow/status/secwexen/aappmart/codeql.yml?label=CodeQL)
![Coverage](https://img.shields.io/codecov/c/github/secwexen/aappmart)
![Contributors](https://img.shields.io/github/contributors/secwexen/aappmart)
![Stars](https://img.shields.io/github/stars/secwexen/aappmart)
![Forks](https://img.shields.io/github/forks/secwexen/aappmart)
![Open Issues](https://img.shields.io/github/issues/secwexen/aappmart)
![Open PRs](https://img.shields.io/github/issues-pr/secwexen/aappmart)
![Release](https://img.shields.io/github/v/release/secwexen/aappmart)
![Python Versions](https://img.shields.io/pypi/pyversions/aappmart)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightblue)
![License](https://img.shields.io/github/license/secwexen/aappmart)
![Repo Size](https://img.shields.io/github/repo-size/secwexen/aappmart)
![Last Commit](https://img.shields.io/github/last-commit/secwexen/aappmart)
[![Website](https://img.shields.io/website?url=https://secwexen.github.io/aappmart/)](https://secwexen.github.io/aappmart/)

*An autonomous intelligence engine that thinks like an attacker to protect defenders.*

### Autonomous Attack Path Prediction & Multi-Agent Red Team Engine

AAPP-MART is an autonomous offensive security engine designed for security teams and researchers.
It predicts attack paths using artificial intelligence and simulates them with a multi-agent red team,
helping organizations identify and mitigate risks before they are exploited.  


for detailed documentation, please visit [Website](https://secwexen.github.io/aappmart/)

---

## Overview

Modern infrastructures are too complex for traditional security testing. AAPP-MART combines predictive AI with autonomous adversarial simulation to continuously evaluate an environment’s real attack surface.

The system operates in two major components:

- **AAPP (AI Attack Path Predictor)**  
  Predicts the most likely attack paths by analyzing services, permissions, vulnerabilities, and configuration weaknesses.

- **MART (Multi-Agent Red Team)**  
  Executes autonomous red team simulations using specialized AI agents that emulate real attacker behavior.

Together, they create a fully automated offensive security engine capable of forecasting and simulating attacks end-to-end.

---

## Key Features

### AI Attack Path Prediction (AAPP)
- Builds attack graphs from system data  
- Identifies multi-step exploit chains  
- Scores risk and exploitability  
- Predicts attacker movement before it happens  

### Multi-Agent Red Team (MART)
- Reconnaissance agent  
- Exploitation agent  
- Privilege escalation agent  
- Lateral movement agent  
- Persistence agent  
- Reporting agent  

Agents collaborate and make decisions autonomously, simulating realistic adversary behavior.

### Autonomous Simulation Brain
- Merges prediction and execution  
- Runs attack scenarios mentally before performing them  
- Generates detailed reports and mitigation recommendations  

---

## Architecture

```
AAPP (Prediction Engine)
    ↓
Predicted Attack Paths
    ↓
MART (Multi-Agent Red Team)
    ↓
Autonomous Simulation
    ↓
Final Report & Defense Recommendations
```

---

## Directory Structure

```
aappmart/
│
├── aapp/                  # Attack Path Predictor
├── mart/                  # Multi-Agent Red Team
├── core/                  # Autonomous simulation brain
├── api/                   # Optional REST API
├── cli/                   # Command-line interface
├── data/                  # Sample data & signatures
├── reports/               # Generated reports
├── docs/                  # Documentation
├── tests/                 # Unit tests
├── scripts/               # Helper scripts
├── requirements.txt
├── setup.py
└── README.md
```

---

## Platform Support

AAPP-MART is a cross-platform Python project and runs on:

- Linux
- macOS
- Windows

No platform-specific dependencies are required.

---

## Installation

```bash
git clone https://github.com/secwexen/aappmart
cd aappmart

# (Optional but recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

> ⚠️ Note: Core implementation is still in progress. Some modules may not be functional yet.

---

## Quick Start

```python
from aappmart.core.orchestrator import AAPP_MART

engine = AAPP_MART(target="192.168.1.10")
engine.run()

report = engine.get_report()
print(report)
```

> ⚠️ Note: Core implementation is still in progress.  
> Some modules may not be fully functional yet.  
> This example is for demonstration purposes and to help you get started.  

---

## Testing

Run unit tests with:

```bash
pytest
```

---

## Use Cases

- Automated red teaming  
- Continuous security validation  
- Attack surface mapping  
- Zero-day exposure modeling  
- SOC augmentation  
- Pre-breach risk forecasting  

---

## Acronym Breakdown

**AAPP** → AI Attack Path Predictor  
**MART** → Multi-Agent Red Team  

**AAPP-MART** = The fusion of prediction and simulation into a single autonomous attack intelligence engine.

---

## License

This project is licensed under the Apache License, Version 2.0.  
See the `LICENSE` file for full details.  

---

## Contributing

Contributions are welcome.  
Please open an issue before submitting major changes or new features.  
See `CONTRIBUTING.md` for detailed contribution guidelines.  

---

## Roadmap

- [ ] Graph-based attack path visualizer
- [ ] Cloud environment support
- [ ] Agent marketplace
- [ ] Reinforcement learning–based decision engine

---

## Development Status

⚠️ Early-stage open source project. Core implementation is still in progress.  
This repository provides the project structure and foundational components of the AAPP-MART engine.  
Additional advanced modules and controlled security-testing features will be added progressively.  

---

## Ethical Use Statement

AAPP-MART is designed to help organizations understand and reduce their attack surface
by simulating adversarial behavior in a controlled and authorized manner.
Its primary goal is to improve defensive posture, not to facilitate real-world attacks.

---

## Disclaimer

AAPP-MART is intended exclusively for ethical, legal, and authorized security research,
penetration testing, and defensive security validation.

The use of this tool against systems, networks, or applications without explicit
authorization from the system owner is strictly prohibited and may be illegal.

The authors and contributors of this project assume no responsibility or liability
for any misuse, damage, or legal consequences resulting from the use of this software.
Users are solely responsible for ensuring compliance with all applicable laws,
regulations, and organizational policies.

---

## Security

For responsible disclosure and reporting security issues, please see `SECURITY.md`.  

---

## Author

**Secwexen**  
GitHub: [secwexen](https://github.com/secwexen)  
