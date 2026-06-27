# AAPP-MART

<p align="center">
<img src="assets/images/aapp-mart-logo.png" width="400" alt="AAPP-MART Logo" loading="lazy" decoding="async">
</p>

[![Build](https://github.com/secwexen/aapp-mart/actions/workflows/ci.yml/badge.svg)](https://github.com/secwexen/aapp-mart/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/secwexen/aapp-mart/branch/main/graph/badge.svg)](https://codecov.io/gh/secwexen/aapp-mart)
[![Release](https://img.shields.io/github/v/release/secwexen/aapp-mart)](https://github.com/secwexen/aapp-mart/releases)
[![License](https://img.shields.io/github/license/secwexen/aapp-mart)](https://github.com/secwexen/aapp-mart/blob/main/LICENSE)

⭐ If you find this project valuable, consider starring the repository.

## About

**AAPP‑MART** (AI‑Autonomous Attack Path Prediction & Multi‑Agent Red Team Simulation Engine) is an open‑source cybersecurity engine for **offensive security research**, **adversarial modeling**, and **automated risk assessment**. It combines **AI‑powered attack‑path prediction** with **autonomous multi‑agent red‑team simulation** to model how real attackers navigate an environment and to reveal actionable, data‑driven security insights.

Unlike traditional static vulnerability scanners or manual penetration testing, AAPP‑MART uses predictive analytics, graph‑based threat modeling, and autonomous adversarial behavior to deliver continuous and realistic security evaluation. Its architecture helps defenders anticipate attack strategies, validate defensive controls, and understand real‑world risk through repeatable, scalable, and intelligence‑driven simulations. 

The system generates structured **attack-path reports**, **MITRE ATT&CK-mapped insights**, and **risk scoring outputs** to support SOC operations, detection engineering, and continuous security improvement.

## Why AAPP-MART?

AAPP-MART stands out from traditional security tools in its approach:

- **Traditional scanners** → static, reactive, often limited to known vulnerabilities.
- **BAS (Breach & Attack Simulation) tools** → rely on predefined playbooks and limited scenarios.
- **AAPP-MART** → predictive, autonomous, and adaptive: forecasts attack paths and executes intelligent multi-agent simulations.

By combining **AI-Autonomous Attack Path Prediction** with **Multi-Agent Red Team Simulation Engine**, AAPP-MART provides organizations with a forward-looking security posture, not just reactive alerts.

## Use Cases

AAPP-MART enables advanced, intelligence-driven security operations through the following core use cases:

- **Predictive Attack Path Analysis**
- **Autonomous Red Team Simulation**
- **Attack Surface & Lateral Movement Modeling**
- **MITRE ATT&CK–Aligned Threat Simulation**
- **Vulnerability Prioritization & Risk Scoring**

## How it Works

### 1. AAPP (AI-Autonomous Attack Path Prediction)

Evaluates assets, configurations, permissions, and vulnerabilities to predict probable attacker paths.

### 2. MART (Multi-Agent Red Team Simulation Engine)

Autonomous agents simulate realistic adversary actions:

- Reconnaissance  
- Exploitation  
- Lateral Movement  
- Privilege Escalation  
- Persistence  
- Reporting

### 3. Orchestration Engine

Coordinates AAPP & MART, maintains a global knowledge graph, executes simulations, and produces structured risk reports.

## Architecture

The system is architected around three primary subsystems:

- **AI-Attack Path Prediction Engine (AAPP)**
- **Multi-Agent Red Team Simulation Engine (MART)**
- **Core Orchestration Layer**

These subsystems operate in a tightly integrated manner through a shared attack graph (knowledge graph), enabling coordinated attack modeling, adversarial simulation, and unified risk analysis across the platform.

## Legal & Authorized Use Only

AAPP-MART is intended solely for authorized security assessment, defensive threat modeling, 
and controlled adversary simulation within environments where explicit permission has been granted.

The system is designed for non-destructive analysis and does not support uncontrolled exploitation. 
Users are fully responsible for ensuring compliance with all applicable laws, regulations, and organizational policies when operating this system.

Unauthorized use of this system is strictly prohibited and may violate applicable laws and regulations.

## Legal Disclaimer

The developers and contributors of this project assume no responsibility or liability for misuse, damage, or legal consequences arising from the use of this software.

This software is provided “as is” without warranty of any kind, express or implied.

## Who is this for

- CISOs, InfoSec managers, and executive stakeholders seeking actionable security intelligence  
- Security, engineering, and risk teams aiming to proactively assess and improve cyber resilience  
- Internal/External red, blue, and purple teams requiring realistic, repeatable adversary emulation  
- Organizations subject to regulatory or compliance mandates (MITRE ATT&CK, NIST, CIS, PCI DSS, ISO 27001, etc.)

## Features

- **AI-Autonomous Attack Path Prediction**
- **Multi-Agent Red Team Simulation Engine**
- Graph-based threat modeling and attack graph analysis
- **MITRE ATT&CK aligned adversary behavior modeling**
- Risk-based security posture analysis
- ML-assisted vulnerability prioritization

## Demo

Run the autonomous attack-path simulation locally:

```bash
python demo/advanced_attack_simulation_demo.py
```

### Demo Output

```text
=== AAPP-MART Autonomous Simulation ===

[*] Target acquired: 10.10.20.15
[+] Reconnaissance       | MITRE: T1595 | Severity: LOW      | Active scanning detected
[+] Phishing             | MITRE: T1566 | Severity: MEDIUM   | Credential harvesting attempt
[+] Initial Access       | MITRE: T1078 | Severity: HIGH     | Valid account abuse
[+] Lateral Movement     | MITRE: T1021 | Severity: HIGH     | Remote service pivoting
[+] Privilege Escalation | MITRE: T1068 | Severity: CRITICAL | Kernel privilege escalation simulated
[✓] Simulation completed successfully

=== Risk Summary ===

Target              : 10.10.20.15
Risk Score          : 8.9/10
Duration            : 11.2s
Compromised Assets  : 3
Generated At        : 2026-01-01 09:58:45

Critical Assets:
- FILE-SERVER-01
- DOMAIN-CONTROLLER
- HR-DB

[+] Report exported → aapp-mart/logs/attack-path/attack_report_10.10.20.15.json
```

See the [Attack Simulation Report - 10.10.20.15](demo/attack_report_10.10.20.15.json) file.

> [!NOTE]
> This IP/hostname is an example target. You will write the actual target IP/hostname yourself in the main project.

## Installation

### Supported Operating Systems

- Linux (primary, production & deployment recommended)  
- Windows (WSL2 + Docker required for full compatibility)  
- macOS (Docker or native development supported)

### Requirements

- Python 3.11+
- Go 1.21+
- C++17+
- Node.js 18+ (frontend / visualization layer)
- Docker
- Kubernetes (for deployment)
- YAML / JSON-based configuration ecosystem

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

## Documentation

- [Quick Start](docs/getting-started/quickstart.md)  
- [Installation Guide](docs/getting-started/installation.md)  
- [API Reference](docs/reference/api-reference.md)  
- [Deployment Guide](docs/guides/deployment.md)  
- [Security Policy](SECURITY.md)

## License

Copyright © 2026 secwexen.

This project is licensed under the Apache-2.0 License.  
See the [LICENSE](LICENSE) file for full details.

## Contributing

Contributions and suggestions are welcome!

### Contributing Workflow (Summary)

- Fork the repository and create a feature or fix branch (e.g. `feature/your-feature`, `fix/bug-name`, `docs/update-readme`, `chore/dependency-update`).
- Make your changes and add relevant tests.
- Use clear commit messages (e.g. Conventional Commits: feat:, fix:, docs:, refactor:).
- Ensure all tests pass (`pytest`) and code style checks (e.g. `make lint`).
- Open a pull request referencing related issues/discussion when possible.
- All PRs must pass CI checks before merging.

Please open an issue before submitting major changes or new features.

See [CONTRIBUTING](CONTRIBUTING.md) for detailed contribution guidelines.

## Roadmap

The development of **AAPP-MART** follows a structured roadmap focused on improving attack path prediction, Multi-Red Team Simulation Engine, and security research capabilities.

Planned improvements include:

- improved AI-based attack path prediction
- expanded MART offensive agents
- path-aware risk scoring based on simulated attack chains
- optional visualization layer for simulation outputs
- plugin ecosystem for custom modules and agents
- distributed simulation support

For the full roadmap and upcoming features, see [Roadmap](ROADMAP.md).

## Development Status

Active development. Core modules are under implementation.

## Security

If you discover a security vulnerability, please follow our responsible disclosure process.

See [SECURITY](SECURITY.md) for instructions on reporting issues securely.
