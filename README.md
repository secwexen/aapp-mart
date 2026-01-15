# AAPP-MART  

<p align="center"><img src="docs/logo/aappmart_logo.png" width="300" alt="AAPP-MART Logo"></p>

![Build Status](https://img.shields.io/github/actions/workflow/status/secwexen/secwexen-aappmart/build.yml?label=Build)
![Lint](https://img.shields.io/github/actions/workflow/status/secwexen/secwexen-aappmart/lint.yml?label=Lint)
![Python Lint](https://img.shields.io/github/actions/workflow/status/secwexen/secwexen-aappmart/pylint.yml?label=PyLint)
![CodeQL](https://img.shields.io/github/actions/workflow/status/secwexen/secwexen-aappmart/codeql.yml?label=CodeQL)
![Release](https://img.shields.io/github/v/release/secwexen/secwexen-aappmart)
![License](https://img.shields.io/github/license/secwexen/secwexen-aappmart)
![Python Versions](https://img.shields.io/pypi/pyversions/secwexen-aappmart)
![Coverage](https://img.shields.io/codecov/c/github/secwexen/secwexen-aappmart)
[![Website](https://img.shields.io/website?url=https://aappmart.github.io)](https://aappmart.github.io/)

### Autonomous Attack Path Prediction & Multi-Agent Red Team Engine

AAPP-MART is an autonomous offensive security engine that predicts attack paths using artificial intelligence and simulates them with a multi-agent red team. By identifying risks before they occur, it forms the world’s first fully automated attack simulation brain.

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

## Installation

```bash
git clone https://github.com/yourusername/aappmart
cd aappmart
pip install -r requirements.txt
```

---

## Quick Start

```python
from aappmart.core.orchestrator import AAPP_MART

engine = AAPP_MART(target="192.168.1.10")
engine.run()

report = engine.get_report()
print(report)
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

Apache-2.0 license.

---

## Contributing

Contributions are welcome.  
Please open an issue before submitting major changes.

---

## Roadmap

- [ ] Graph-based attack path visualizer
- [ ] Cloud environment support
- [ ] Agent marketplace
- [ ] Reinforcement learning–based decision engine

---

## Development Status

This repository contains the project structure and foundational components of the AAPP-MART engine.  
Core offensive logic and advanced modules may be added progressively.
