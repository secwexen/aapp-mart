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
![Status](https://img.shields.io/badge/status-early--stage-orange)

*An autonomous intelligence engine that thinks like an attacker to protect defenders.*

For a high-level explanation of the project’s purpose and positioning,
see [ABOUT.md](ABOUT.md).

### Autonomous Attack Path Prediction & Multi-Agent Red Team Engine

AAPP-MART is an autonomous offensive security engine designed for security teams and researchers.
It predicts attack paths using artificial intelligence and simulates them with a multi-agent red team,
helping organizations identify and mitigate risks before they are exploited.  


for detailed documentation, please visit [Website](https://secwexen.github.io/aappmart/)

---

## Overview

Modern infrastructures are too complex for traditional security testing. AAPP-MART combines predictive AI with autonomous adversarial simulation to continuously evaluate an environment’s real attack surface.

### Why AAPP-MART?

AAPP-MART stands out from traditional offensive security tools in its approach:

- **Traditional scanners** → static, reactive, often limited to known vulnerabilities.
- **BAS (Breach & Attack Simulation) tools** → rely on predefined playbooks and limited scenarios.
- **AAPP-MART** → predictive, autonomous, and adaptive: forecasts attack paths and executes intelligent multi-agent simulations.

By combining **AI-driven attack path prediction** with **autonomous red team simulations**, AAPP-MART provides organizations with a forward-looking security posture, not just reactive alerts.

---

## System Components

The system operates in two major components:

- **AAPP (AI Attack Path Predictor)**  
  Predicts the most likely attack paths by analyzing services, permissions, vulnerabilities, and configuration weaknesses.

- **MART (Multi-Agent Red Team)**  
  Executes autonomous red team simulations using specialized AI agents that emulate real attacker behavior.

Together, they create a fully automated offensive security engine capable of forecasting and simulating attacks end-to-end.

---

## Threat Model & Scope

AAPP-MART simulates attacker behavior at the following layers:
- Network-level (services, ports, exposure)
- Identity & permission abuse
- Known vulnerability chaining
- Misconfiguration exploitation

Out of scope:
- Zero-click mass exploitation
- Malware delivery to uncontrolled targets
- Destructive payload execution

These boundaries are enforced by design and configuration defaults to ensure safe, authorized, and ethical use.

---

## Input & Output Contract

### Inputs
AAPP-MART consumes structured security-relevant data, such as:
- Target identifiers (IP address, hostname, environment label)
- Asset and service metadata
- Optional vulnerability scan results
- Optional configuration and permission data

### Outputs
The engine produces analytical security artifacts, including:
- Predicted attack paths
- Simulated adversary decision flows
- Risk-scored findings
- Human-readable reports with mitigation guidance

---

## Modes of Operation

AAPP-MART operates in controlled modes designed for authorized security assessment
and defensive validation.

### Prediction-Only Mode
- No active interaction with the target
- Builds attack graphs and forecasts attacker movement
- Safe for continuous assessment and design-time analysis

### Simulation Mode
- Executes non-destructive, controlled attack simulations
- Focuses on logic flow rather than payload execution
- Designed for lab environments and authorized testing only

Destructive actions and uncontrolled exploitation are intentionally excluded.

---

## MITRE ATT&CK Alignment

AAPP-MART aligns its prediction and simulation logic with the MITRE ATT&CK framework
to ensure standardized, explainable, and defensible security findings.

Agent behaviors and predicted attack paths are mapped to high-level ATT&CK tactics
and techniques, including but not limited to:

- Reconnaissance → TA0043
- Initial Access → TA0001
- Credential Access → TA0006
- Privilege Escalation → TA0004
- Lateral Movement → TA0008
- Persistence → TA0003

This mapping is used for risk scoring, reporting, and defensive recommendations.

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

The following directory layout shows the planned structure of the project.   
Some modules are under active development and may not yet be fully implemented.  

```
.
├── .github/
├── src/
│   └── aappmart/
│       ├── aapp/                  # Attack Path Predictor
│       ├── agents/                # Autonomous attacker agents
│       ├── api/                   # Optional REST API
│       ├── cli/                   # Command-line interface
│       ├── core/                  # Autonomous simulation brain
│       ├── data/                  # Sample data & signatures
│       ├── mart/                  # Multi-Agent Red Team
│       ├── modules/               # Pluggable engine modules
│       ├── predictors/            # Prediction logic & models
│       ├── reports/               # Generated reports
│       ├── main.py                # AAPPMART entry point
│       └── __init__.py            # AAPPMART package initializer
│
├── docs/
├── examples/
├── internal_api/
├── scripts/
├── tests/
├── .gitignore
├── .pre-commit-config.yaml
├── ABOUT.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── DISCLAIMER.md
├── LICENSE
├── Makefile
├── README.md
├── SECURITY.md
├── main.py
├── pyproject.toml
├── requirements-dev.txt
├── requirements.txt
└── setup.py
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
# 1. Clone repository
git clone https://github.com/secwexen/aappmart.git
cd aappmart

# 2. (Optional but recommended) Create a virtual environment 
# Linux / macOS
python3 -m venv venv  
source venv/bin/activate  

# Windows (PowerShell)
python -m venv venv  
venv\Scripts\activate  

# 3. Install dependencies
pip install -r requirements.txt
```

> ⚠️ Note: Some modules may be under active development. Functionality may be limited.

---

## Quick Start

```python
from aappmart.core.orchestrator import AAPP_MART

engine = AAPP_MART(target="192.168.1.10")
engine.run()

report = engine.get_report()
print(report)
```

> ⚠️ Note: Example is for demonstration purposes. Some features may not yet be fully implemented. 

---

## Testing

To run the unit tests:

1. Ensure you are in the project root directory:

```bash
cd aappmart
```

2. (Optional) Activate your virtual environment:

```bash
# Linux / macOS
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\activate
```

3. Run all tests with `pytest`:

```bash
pytest
```

> ⚠️ Note: Some modules are under active development. Certain tests may be skipped or marked as expected failures until those features are fully implemented.

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
See the [LICENSE](LICENSE) file for full details.  

---

## Contributing

Contributions are welcome.  
Please open an issue before submitting major changes or new features.  
See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.  

---

## Roadmap

AAPP-MART development is structured into strategic phases:

**Phase 1 – Research & Architecture**
- Core AI prediction engine (AAPP) design
- Multi-agent simulation framework (MART) prototyping
- Initial attack graph models and risk scoring

**Phase 2 – Core Implementation**
- Integration of prediction and simulation engines
- Autonomous agent behaviors for reconnaissance, exploitation, and lateral movement
- MITRE ATT&CK alignment and reporting pipeline

**Phase 3 – Ecosystem & Advanced Features**
- Graph-based visualization and dashboards
- Cloud and hybrid environment support
- Agent marketplace and reinforcement learning–based decision engine
- Continuous security validation and SOC augmentation

---

## Development Status

⚠️ Early-stage open source project. Core implementation is still in progress.   

AAPP-MART is currently under active development.
This repository provides the foundational architecture, core interfaces,
and initial logic of the AAPP-MART engine.

Advanced prediction models, autonomous agent behaviors,
and controlled simulation capabilities are being implemented progressively.

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

## Support & Contact

For support, questions, or feature requests, please open an issue on GitHub:
[GitHub Issues](https://github.com/secwexen/aappmart/issues)

You may also use GitHub Discussions for ideas and general discussions.  

---

## Security

For responsible disclosure and reporting security issues, please see [SECURITY.md](SECURITY.md).  

---

## Author

**Secwexen** – Project Author & Maintainer  
**Role:** Project Manager | Lead Developer   
**GitHub:** [github.com/secwexen](https://github.com/secwexen)  
