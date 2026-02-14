# AAPP-MART  

<p align="center">
<img src="assets/images/aapp-mart-logo.png" width="250" alt="aapp-mart-logo">
</p>

![Build](https://img.shields.io/github/actions/workflow/status/secwexen/aapp-mart/ci.yml?branch=main&label=Build)
![PyLint](https://img.shields.io/github/actions/workflow/status/secwexen/aapp-mart/pylint.yml?branch=main&label=PyLint)
![CodeQL](https://img.shields.io/github/actions/workflow/status/secwexen/aapp-mart/codeql.yml?branch=main&label=CodeQL)
![Dependencies](https://img.shields.io/github/actions/workflow/status/secwexen/aapp-mart/dependency-review.yml?branch=main&label=Dependencies)
![Python Versions](https://img.shields.io/pypi/pyversions/aapp-mart)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgray)
![License](https://img.shields.io/github/license/secwexen/aapp-mart)
![Downloads](https://img.shields.io/pypi/dm/aapp-mart?label=Downloads)
![Repo Size](https://img.shields.io/github/repo-size/secwexen/aapp-mart)
[![Website](https://img.shields.io/website?url=https://secwexen.github.io/aapp-mart/)](https://secwexen.github.io/aapp-mart/)
![Status](https://img.shields.io/badge/status-early--stage-orange)

## Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine

AAPP-MART is an autonomous attack simulation and prediction engine for defensive security validation, designed for security teams and researchers.
It predicts attack paths using artificial intelligence and simulates them with a multi-agent red team,
helping organizations identify and mitigate risks before they are exploited.  
  
for detailed documentation, please visit [AAPP-MART Website](https://secwexen.github.io/aapp-mart/)

---

## Intended Use & Ethics Statement

AAPP-MART is designed exclusively for authorized security testing, defensive threat modeling, and red team simulations with explicit permission.  
It is intended to help organizations understand and reduce their attack surface by simulating adversarial behavior in a controlled and authorized manner.  

The project is not intended for unauthorized access, real-world exploitation, or destructive attack activities.  
Users are responsible for complying with all applicable laws, regulations, and organizational policies.  
Its primary goal is to improve defensive posture, not to facilitate real-world attacks.

---

## Who Should Use AAPP-MART?

- Security Operations Centers (SOC)
- Red & Blue Teams
- Security Architects
- Threat Modeling Teams
- Academic & Security Researchers

---

## What AAPP-MART Is NOT

- Not an exploitation framework
- Not a malware delivery system
- Not a zero-day weaponization tool
- Not designed for uncontrolled or destructive attacks

---

## Overview

Modern infrastructures are too complex for traditional security testing. AAPP-MART combines predictive AI with autonomous adversarial simulation to continuously evaluate an environment’s real attack surface.

### Why AAPP-MART?

AAPP-MART stands out from traditional security tools in its approach:

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

```
aapp-mart
├── src/
│   └── aapp_mart/
│       ├── aapp/                  # Attack Path Predictor
│       ├── agents/                # Autonomous attacker agents
│       ├── api/                   # Optional REST API
│       ├── common/                # Common, reusable base classes or constants
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
├── ml_training/
├── scripts/
├── tests/
├── ABOUT.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── DISCLAIMER.md
├── LICENSE
├── Makefile
├── README.md
├── SECURITY.md
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

## Platform & Safety Notes

- AAPP-MART is intended to run in **controlled and authorized environments only**.
- Some simulation techniques may model sensitive attacker behaviors; **use exclusively in isolated lab or test environments**.
- The engine avoids destructive actions by design, but **misconfiguration or improper use may still pose risks**.
- Users are responsible for ensuring compliance with **organizational policies, legal requirements, and ethical guidelines**.
- Do not deploy AAPP-MART against production systems without **explicit authorization and appropriate safeguards**.

---

## Installation

```bash
# 1. Clone repository
git clone https://github.com/secwexen/aapp-mart.git
cd aapp-mart

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

> Note: Some modules may be under active development. Functionality may be limited.

---

## Environment Configuration

AAPP-MART uses environment variables for configuration.
For local development, copy the example file and adjust values as needed:

```bash
cp .env.example .env
```

> Never commit your real .env file, as it may contain sensitive or environment‑specific information.

---

## Example Quick Start

```python
from aapp_mart.core.orchestrator import AAPP_MART

engine = AAPP_MART(target="192.168.1.10")
engine.run()
report = engine.get_report()
print(report)
```

> Note: Example is for demonstration purposes. Some features may not yet be fully implemented. 

---

## Example Output

```bash
=== Attack Path Prediction Report ===
Target: 192.168.1.10

[+] Predicted Attack Paths:
  1. Internal Reconnaissance → Credential Access → Lateral Movement → Privilege Escalation
  2. Initial Access → Exploit Service Vulnerability → Persistence

[+] Risk Score: 8.5 / 10

[+] Recommendations:
- Patch service X and limit privileged account exposure.
- Disable unused open ports.
==========================================
```

> Output is illustrative—actual results depend on your environment and enabled modules.  
> Risk scores and attack paths are heuristic and for demonstration only.  

---

## CLI/API Usage Example

Run an attack simulation:
```bash
aapp-mart run --target 192.168.1.10
```

Generate a prediction-only report:
```bash
aapp-mart predict --input data/target_profile.json --output report.txt
```

List available modules:
```bash
aapp-mart modules list
```

See the CLI documentation for available commands and advanced options: [CLI documentation](docs/cli.md)

---

## Testing

To maintain code quality and reliability, please use the following checks before submitting code or pull requests.

1. Run all unit tests
Make sure your code passes all tests.
```bash
pytest
```

2. Check test coverage
Verify that your changes are covered by tests (coverage.py needs to be installed).
```bash
coverage run -m pytest
coverage report
```

3. Check code style and linting
Ensure your code meets the project's style and static analysis requirements.
```bash
make lint         # If you have a Makefile with lint target
# or, run pylint directly:
pylint src/aapp_mart
```

> Note: Some modules are under active development. Certain tests may be skipped or marked as expected failures until those features are fully implemented.

---

## Use Cases

- Automated red teaming  
- Continuous security validation  
- Attack surface mapping  
- Zero-day exposure modeling  
- SOC augmentation  
- Pre-breach risk forecasting  

---

## Acronym

- **AAPP** — AI Attack Path Predictor (*ey-ey pee-pee*)  
- **MART** — Multi-Agent Red Team (*maart*)  

**AAPP-MART** — The fusion of AI-driven attack path prediction and autonomous multi-agent simulation into a unified attack intelligence engine.

---

## Documentation

Detailed guides and references are also available in the repository:

- [About AAPP-MART](ABOUT.md)
- [Full installation guide](docs/installation.md)
- [Module development](docs/modules.md)
- [Prediction engine details](docs/prediction_engine.md)
- [Examples and quick starts](examples/)
- [Contributing guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [Security policy](SECURITY.md)

---

## License

This project is licensed under the Apache License, Version 2.0.  
See the [LICENSE](LICENSE) file for full details.  

---

## Contributing

### Contributing Workflow (Summary)

- Fork the repository and create a feature or fix branch (e.g. `feature/your-feature`).
- Make your changes and add relevant tests.
- Ensure all tests pass (`pytest`) and code style checks (e.g. `make lint`).
- Open a pull request referencing related issues/discussion when possible.
- All PRs must pass CI checks before merging.

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

Early-stage open source project. Core implementation is still in progress.   

AAPP-MART is currently under active development.
This repository provides the foundational architecture, core interfaces,
and initial logic of the AAPP-MART engine.

Advanced prediction models, autonomous agent behaviors,
and controlled simulation capabilities are being implemented progressively.

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

## Support & Community

If you find this project useful, consider giving it a ⭐ on GitHub.
Contributions, issues, and pull requests are welcome.

For support, questions, or feature requests, please open an issue:
👉 [Open an issue on GitHub](https://github.com/secwexen/aapp-mart/issues)

For ideas and general discussions, use GitHub Discussions.

---

## Security

If you discover a security vulnerability, please follow our responsible disclosure process.

[Read SECURITY.md](SECURITY.md) for instructions on reporting issues securely. 

---

## Author

**Secwexen** – Project Lead & Maintainer   
**GitHub:** [github.com/secwexen](https://github.com/secwexen)  
