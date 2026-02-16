# AAPP-MART  

<p align="center">
<img src="assets/images/aapp-mart-logo.png" width="250" alt="aapp-mart-logo">
</p>

![Build](https://img.shields.io/github/actions/workflow/status/secwexen/aapp-mart/ci.yml?branch=main&label=Build)
![CodeQL](https://img.shields.io/github/actions/workflow/status/secwexen/aapp-mart/codeql.yml?branch=main&label=CodeQL)
![Python Versions](https://img.shields.io/pypi/pyversions/aapp-mart)
![License](https://img.shields.io/github/license/secwexen/aapp-mart)
[![Website](https://img.shields.io/website?url=https://secwexen.github.io/aapp-mart/)](https://secwexen.github.io/aapp-mart/)
![Status](https://img.shields.io/badge/status-actively%20developed-brightgreen)

## Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine

AAPP-MART is an autonomous attack simulation and prediction engine for defensive security validation, designed for security teams and researchers.
It predicts attack paths using artificial intelligence and simulates them with a multi-agent red team,
helping organizations identify and mitigate risks before they are exploited.  
  
for detailed documentation, please visit [AAPP-MART Website](https://secwexen.github.io/aapp-mart/)

---

## Executive Summary

AAPP-MART is a deterministic attack path modeling and controlled adversary simulation engine 
designed for authorized defensive security validation.

The system combines:
- Graph-based attack path prediction
- Controlled multi-agent adversary simulation
- Risk-scored analytical reporting

It does not perform destructive exploitation.

---

## Legal & Authorized Use

AAPP-MART is intended solely for authorized security assessment, defensive threat modeling, 
and controlled adversary simulation within environments where explicit permission has been granted.

The system is designed for non-destructive analysis and does not support uncontrolled exploitation. 
Users are responsible for ensuring lawful and policy-compliant usage.

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

## Attack Graph Model

AAPP-MART models the target environment as a directed attack graph:

G = (V, E)

Where:

- **V (Vertices)** represent assets or security-relevant states

- Host systems
- Network services
- Identity objects (users, roles, tokens)
- Privilege states

- **E (Edges)** represent feasible adversarial transitions between states

- Exploit of a vulnerability
- Credential abuse
- Misconfiguration leverage
- Privilege escalation step
- Lateral movement action

Each edge ( e \in E ) is associated with:

- **Likelihood score (Lₑ)**
- **Exploitability weight (Wₑ)**
- Optional contextual modifiers (exposure, privilege level, asset criticality)

### Path Scoring

For an attack path ( P = {e_1, e_2, ..., e_n} ):

[
PathScore(P) = \prod_{i=1}^{n} L_{e_i} \times C_{context}
]

Where:

- ( L_{e_i} ) = likelihood of each transition
- ( C_{context} ) = contextual weighting factor (asset exposure, privilege amplification, etc.)

The engine ranks predicted attack paths based on aggregated likelihood and impact weighting.

The model is deterministic with respect to input data and configuration parameters.

---

## Risk Scoring Model

AAPP-MART calculates risk using a structured composite model:

[
Risk = Likelihood \times Impact
]

### 1. Likelihood

Derived from:

- Vulnerability exploitability
- Exposure level
- Privilege requirements
- Chaining feasibility within the attack graph

### 2. Impact

Weighted using:

- Asset criticality
- Privilege escalation level
- Lateral movement amplification
- Business sensitivity (if provided)

### 3. Asset Criticality Weighting

Each asset may be assigned a criticality factor:

[
AdjustedRisk = Risk \times AssetWeight
]

### 4. CVSS Integration 

If vulnerability scan data is provided, scores may incorporate metrics aligned with
FIRST and the
Common Vulnerability Scoring System framework.

CVSS values are treated as input modifiers rather than sole risk determinants.

### 5. Confidence Score

Each reported risk includes a confidence indicator based on:

- Completeness of input data
- Assumption density
- Model coverage of the simulated path

---

## Security Boundaries & Operational Safeguards

AAPP-MART is designed as a controlled simulation system. The following safeguards define its operational boundary:

- **Non-destructive simulation enforcement**
- No payload execution
- No arbitrary command execution on targets
- No uncontrolled exploitation logic
- No automated scanning beyond defined scope

### Scope Restriction

Targets must be explicitly defined.
The engine does not autonomously expand scope.

### Operational Controls

- Structured logging of all simulation steps
- Deterministic execution boundaries
- Configurable simulation mode (prediction-only vs simulation)

These constraints ensure the system remains a defensive validation platform rather than an exploitation tool.

---

## Explainability & Audit Trail

AAPP-MART is designed to produce traceable and explainable outputs.

### Agent Decision Trace

Each simulated action includes:

- Triggering condition
- Supporting evidence
- Graph transition reference
- Risk contribution

### Attack Path Reasoning Log

For each predicted path:

- Ordered transition list
- Cumulative score calculation
- Context modifiers applied

### Deterministic Replay

Given identical input data and configuration:

- The prediction engine produces consistent results
- Simulation flows can be replayed for validation

### Structured Output

Reports can be exported in structured formats (e.g., JSON) to support:

- SIEM ingestion
- SOC workflows
- External audit review

---

## Deployment Model

AAPP-MART supports the following deployment patterns:

### Standalone CLI

- Local execution
- Scriptable automation
- CI/CD integration

### REST API Mode (Planned)

- Programmatic integration
- External orchestration support

### Offline / Air-Gapped Operation

- No external service dependency required
- Suitable for isolated environments

### Containerization (Planned)

- Docker-based deployment
- Isolated execution boundary

### System Requirements

- Python 3.11
- Standard system memory sufficient for graph size
- No platform-specific dependencies

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
│       └── main.py                # AAPPMART entry point
│ 
├── assets/
├── docs/
├── examples/
├── internal_api/
├── ml_training/
├── tests/
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

## Known Limitations

AAPP-MART is subject to the following constraints:

- Does not exploit zero-day vulnerabilities
- Does not execute destructive payloads
- Does not replace full manual penetration testing
- Depends on accuracy and completeness of input data
- Attack path prediction is model-driven and not a guarantee of real-world exploit success
- Large-scale environments may require tuning for performance

The system is intended for structured defensive analysis, not offensive weaponization.

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

## Documentation

Detailed guides and references are also available in the repository:

- [About AAPP-MART](ABOUT.md)
- [Full installation guide](docs/installation.md)
- [Module development](docs/modules.md)
- [Prediction engine details](docs/prediction_engine.md)
- [Examples and quick starts](examples/)
- [Roadmap & Milestones](docs/roadmap.md)
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
**Phase 2 – Core Implementation**  
**Phase 3 – Ecosystem & Advanced Features**  

---

## Development Status

Actively Developed open source project. Core implementation is still in progress.   

AAPP-MART is currently under active development.
This repository provides the foundational architecture, core interfaces,
and initial logic of the AAPP-MART engine.

Advanced prediction models, autonomous agent behaviors,
and controlled simulation capabilities are being implemented progressively.

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
