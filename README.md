# AAPP-MART

<p align="center">
<img src="assets/images/aapp-mart-logo.png" width="350" alt="AAPP-MART AI-Autonomous Attack Path Prediction and Multi‑Agent Red Team Simulation Engine Logo" loading="lazy" decoding="async">
</p>

**Predict. Simulate. Secure.**  
An AI‑Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine designed for enterprise‑grade security assessment.  

**Official Website:** [https://secwexen.github.io/aapp-mart/](https://secwexen.github.io/aapp-mart/)

⭐ If you find this project valuable, consider starring the repository.

[![Build](https://github.com/secwexen/aapp-mart/actions/workflows/ci.yml/badge.svg?branch=main&event=pull_request)](https://github.com/secwexen/aapp-mart/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/secwexen/aapp-mart/branch/main/graph/badge.svg?branch=main&event=pull_request)](https://codecov.io/gh/secwexen/aapp-mart)
[![Release](https://img.shields.io/github/v/release/secwexen/aapp-mart)](https://github.com/secwexen/aapp-mart/releases)
[![License](https://img.shields.io/github/license/secwexen/aapp-mart)](https://github.com/secwexen/aapp-mart/blob/main/LICENSE)

## About

**AAPP‑MART** (AI‑Autonomous Attack Path Prediction & Multi‑Agent Red Team Simulation Engine) is an open‑source Python security engine designed for offensive security research, adversarial modeling, and automated risk assessment. It combines AI‑powered attack‑path prediction with autonomous multi‑agent red‑team simulation to model how real attackers navigate an environment and to reveal actionable, data‑driven security insights.

Unlike traditional static vulnerability scanners or manual penetration testing, AAPP‑MART uses predictive analytics, graph‑based threat modeling, and autonomous adversarial behavior to deliver continuous and realistic security evaluation. Its architecture helps defenders anticipate attack strategies, validate defensive controls, and understand real‑world risk through repeatable, scalable, and intelligence‑driven simulations. 

The system generates structured attack-path reports, MITRE ATT&CK-mapped insights, and risk scoring outputs to support SOC operations, detection engineering, and continuous security improvement.

## Overview

Modern infrastructures are too dynamic and interconnected for traditional security testing to keep pace. 
Static scanners and predefined BAS playbooks often fail to capture how real attackers move across complex environments. 

AAPP‑MART addresses this gap by combining predictive AI, AI-driven threat modeling, cyber attack surface prediction, 
and autonomous adversarial simulation to evaluate an environment’s real exposure. The engine models attacker behavior, 
forecasts potential attack paths, and simulates multi-agent adversarial activity to provide proactive, 
intelligence-driven insights into organizational security posture.

## How AAPP-MART Works

1. **AAPP** (AI-Autonomous Attack Path Prediction)  
   Evaluates assets, configurations, permissions, and vulnerabilities to predict probable attacker paths.

   **AI Engine:**
   - Decision Logic: Rule-based / ML / Hybrid (per module).  
   - Learning: Offline or deterministic scoring  
   - Decision Factors: Exploitability, exposure, privilege, asset criticality

2. **MART** (Multi-Agent Red Team Simulation Engine)  
   Autonomous agents simulate realistic adversary actions:  
   Reconnaissance, Exploitation, Lateral Movement, Privilege Escalation, Persistence, Reporting 

3. **CORE Orchestration Engine**  
   Coordinates AAPP & MART, maintains a global knowledge graph, executes simulations, and produces structured risk reports.

**Example Attack Flow:** 
```bash
[User Credential] → [Phishing/Exploit] → [Initial Access] → [Lateral Movement] → [Privilege Escalation] → [Critical Asset Compromise]
```

## Architecture Diagram

AAPP-MART is an AI-Autonomous cybersecurity simulation engine designed for predictive AI-Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine experimentation.

The system models infrastructure assets, vulnerabilities, and relationships as an attack graph that serves as the analytical foundation for the prediction engine and autonomous agent system. These components simulate adversarial behavior and forecast potential attack paths across complex environments.

## Features

- AI-Autonomous Attack Path Prediction
- Multi-Agent Red Team Simulation Engine
- Graph-based threat modeling and attack graph analysis
- MITRE ATT&CK aligned adversary behavior modeling
- Risk-based security posture analysis
- ML-assisted vulnerability prioritization
- Scalable adversarial simulation architecture
- Extensible modular plugin system
- Python-based open-source cybersecurity Engine

## Conceptual Usage Example (Planned API)

This example reflects the intended public API design:

```python
import os
from aapp_mart.core.orchestrator import AAPP_MART

# Initialize the engine with a target IP or hostname
engine = AAPP_MART(target="192.168.1.10")

# Run simulation
engine.run()

# Retrieve the generated attack-path report
report = engine.get_report()

# Print a concise summary of the predicted attack paths
report.export(format="json", path="./logs/attack-path/attack_report.json")
```

> Core orchestration modules are currently under development.  

See [API Reference](docs/reference/api_reference.md) and [System Architecture](docs/architecture/architecture.md) for interface details and system structure.  

## Demo

Experience how **AAPP-MART simulates real-world cyber attacks and predicts attack paths using multi-agent red team simulation engine**.

This interactive demo includes:
- Shows predicted attack paths 
- Simulates red-team agent behavior 
- Generates risk scores and MITRE ATT&CK technique mappings 

### Run the Demo (Google Colab)

**Launch the interactive demo here:**
[Attack Path Demo Notebook on Google Colab](https://colab.research.google.com/github/secwexen/aapp-mart/blob/main/demo/aapp_mart_attack_path_demo.ipynb)

### Demo Console Output

```
Environment is ready for AAPP-MART demo.
Simulating attack path prediction for target: 192.168.1.10
Report exported in json format to ./logs/attack-path/attack_report.json
```

### Explanation of the Output

- The first line indicates the environment is set up.
- The second line indicates that attack path prediction is being “simulated” for the target IP address (`192.168.1.10`).
- The third line states that a report was exported in JSON format to `./logs/attack-path/attack_report.json`.

> [!NOTE]
> No actual file is created or report is generated unless that directory and export logic exist. The output is simply printed to the console as a simulation.

## Legal & Authorized Use

AAPP-MART is intended solely for authorized security assessment, defensive threat modeling, 
and controlled adversary simulation within environments where explicit permission has been granted.

The system is designed for non-destructive analysis and does not support uncontrolled exploitation. 
Users are responsible for ensuring lawful and policy-compliant usage.

## Why AAPP-MART?

AAPP-MART stands out from traditional security tools in its approach:

- **Traditional scanners** → static, reactive, often limited to known vulnerabilities.
- **BAS (Breach & Attack Simulation) tools** → rely on predefined playbooks and limited scenarios.
- **AAPP-MART** → predictive, autonomous, and adaptive: forecasts attack paths and executes intelligent multi-agent simulations.

By combining **AI-Autonomous attack path prediction** with **Multi-Red Team Simulation Engine**, AAPP-MART provides organizations with a forward-looking security posture, not just reactive alerts.

## Why This Project Exists

AAPP-MART was created to help security teams anticipate and simulate modern cyber-attacks before damage occurs.  
Unlike traditional tools that detect incidents after they happen, it predicts attacker behavior and models potential attack paths proactively.

## Installation

AAPP‑MART is currently under active development.

### Supported Operating Systems

- Windows 10 / 11  
- Linux (Ubuntu 22.04+ / Debian 11+ / other Debian-based distributions)  
- macOS (Intel & Apple Silicon)

### Python Requirements

- Python **3.11+**  
- pip 23+  
- Virtual environment recommended

## Quick Start

```bash
# Clone repository
git clone https://github.com/secwexen/aapp-mart.git
cd aapp-mart

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r dev-requirements.txt
```

For full details, refer to the [Quick Start](docs/guides/quickstart.md) file.

## Target Users

- CISOs, InfoSec managers, and executive stakeholders seeking actionable security intelligence  
- Security, engineering, and risk teams aiming to proactively assess and improve cyber resilience  
- Internal/External red, blue, and purple teams requiring realistic, repeatable adversary emulation  
- Organizations subject to regulatory or compliance mandates (MITRE ATT&CK, NIST, CIS, PCI DSS, ISO 27001, etc.)

## Docs & Resources

Detailed guides and references are also available in the repository:

- [Wiki — Full Documentation](https://github.com/secwexen/aapp-mart/wiki)
- [Repository Structure & System Components](docs/architecture/architecture.md)
- [API Reference](docs/reference/api_reference.md)
- [Risk Model](docs/ai/risk-model.md)
- [Deployment Guide](docs/guides/deployment.md)
- [Full Installation Guide](docs/getting-started/installation.md)
- [Quick Start](docs/getting-started/quickstart.md)
- [Examples](docs/examples.md)
- [Roadmap & Milestones](ROADMAP.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [Security Policy](SECURITY.md)

## License

Copyright © 2026 secwexen.

This project is licensed under the Apache License, Version 2.0.  
See the [LICENSE](LICENSE) file for full details.  

## Contributing

Contributions are welcome!

### Contributing Workflow (Summary)

- Fork the repository and create a feature or fix branch (e.g. `feature/your-feature` or `fix/bug-name`).
- Make your changes and add relevant tests.
- Ensure all tests pass (`pytest`) and code style checks (e.g. `make lint`).
- Open a pull request referencing related issues/discussion when possible.
- All PRs must pass CI checks before merging.

Please open an issue before submitting major changes or new features.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## Roadmap

The development of **AAPP-MART** follows a structured roadmap focused on improving attack path prediction, Multi-Red Team Simulation Engine, and security research capabilities.

Planned improvements include:

- advanced attack graph generation
- improved AI-based attack path prediction
- expanded MART offensive agents
- enhanced risk scoring and reporting
- improved visualization and dashboards
- plugin ecosystem for custom modules and agents
- distributed simulation support

For the full roadmap and upcoming features, see [Roadmap.md](ROADMAP.md).

The roadmap evolves over time based on community feedback, research outcomes, and contributor proposals. Contributions and suggestions are welcome.

## Development Status

AAPP-MART active development open source project. Core implementation is still in progress.  

Advanced prediction models, autonomous agent behaviors, and controlled simulation capabilities are being implemented progressively.

## Community & Support

- Check out [Issues](https://github.com/secwexen/aapp-mart/issues) for tasks and ideas.  
- Join [Discussions](https://github.com/secwexen/aapp-mart/discussions) to share feedback and proposals.
- **If you find this project valuable, consider starring the repository.**  
- Contribute code, documentation, or testing — see [CONTRIBUTING.md](CONTRIBUTING.md) for details.  

## Security

If you discover a security vulnerability, please follow our responsible disclosure process.

[Read SECURITY.md](SECURITY.md) for instructions on reporting issues securely. 
