# AAPP-MART

<p align="center">
<img src="assets/images/aapp-mart-logo.png" width="450" alt="AAPP-MART Logo" loading="lazy" decoding="async">
</p>

[![Build](https://github.com/secwexen/aapp-mart/actions/workflows/ci.yml/badge.svg)](https://github.com/secwexen/aapp-mart/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/secwexen/aapp-mart?include_prereleases)](https://github.com/secwexen/aapp-mart/releases)
[![License](https://img.shields.io/github/license/secwexen/aapp-mart)](https://github.com/secwexen/aapp-mart/blob/main/LICENSE)

⭐ If you find this project valuable, consider starring the repository.

## About

AAPP‑MART (AI‑Powered Autonomous Attack Path Prediction & Multi‑Agent Red Team Simulation Engine) is a cybersecurity engine for **adversary emulation**, **security validation**, **threat modeling**, and **risk assessment**.

Unlike traditional static manual penetration testing, AAPP‑MART uses predictive analytics, graph‑based threat modeling, and autonomous adversarial behavior to deliver continuous and realistic security evaluation. Its architecture helps defenders anticipate attack strategies, execute defensive controls validation, and enhance cyber resilience through repeatable, scalable, and intelligence‑driven simulations.

AAPP-MART is designed as an extensible cybersecurity engine rather than a traditional vulnerability scanner or a collection of predefined attack playbooks, providing a foundation for proactive security validation, red teaming, purple teaming, security research, and enterprise security operations.

## Why AAPP-MART?

AAPP-MART combines **AI-powered attack path prediction**, **multi-agent red team simulation**, **attack graph analysis**, and **risk-based security assessment** in a single cybersecurity engine. Instead of treating vulnerabilities and security findings as isolated events, AAPP-MART analyzes how weaknesses, assets, identities, network relationships, and adversarial techniques can combine to form realistic attack paths.

Its **AAPP (AI-Powered Autonomous Attack Path Prediction)** capability identifies and prioritizes potential attack paths using predictive models, graph-based analysis, security-state information, and deterministic security rules. **MART (Multi-Agent Red Team Simulation)** then provides a controlled environment for modeling adversarial behavior across reconnaissance, initial access, privilege escalation, lateral movement, persistence, and other MITRE ATT&CK-aligned activities.

AAPP-MART provides structured, repeatable, and actionable security intelligence that helps security teams understand not only where vulnerabilities exist, but how those vulnerabilities could contribute to a broader attack scenario.

## Use Cases

- AI-Powered Autonomous Attack Path Prediction (AAPP)  
- Multi-Agent Red Team Simulation (MART)  
- Attack Surface & Lateral Movement Modeling  
- MITRE ATT&CK Aligned Threat Simulation  
- Vulnerability Prioritization & Risk Scoring  
- Continuous Security Assessment  
- Attack Simulation Research

## How it Works

### 1. AI-Powered Autonomous Attack Path Prediction (AAPP)

Evaluates assets, configurations, permissions, and vulnerabilities to predict probable attacker paths.

### 2. Multi-Agent Red Team Simulation (MART)

Autonomous agents simulate realistic adversary actions:

- Reconnaissance  
- Exploitation  
- Lateral Movement  
- Privilege Escalation  
- Persistence  
- Reporting

### 3. Core Orchestration (ENGINE)

Coordinates AAPP & MART, maintains a global knowledge graph, executes simulations, and produces structured risk reports.

## Architecture

The system is architected around three primary subsystems:

- AI-Powered Autonomous Attack Path Prediction (AAPP)  
- Multi-Agent Red Team Simulation (MART)  
- Core Orchestration (ENGINE)

These subsystems operate in a tightly integrated manner through a shared attack graph (knowledge graph), enabling coordinated attack modeling, adversarial simulation, and unified risk analysis across the engine.

## Legal & Authorized Use Only

AAPP-MART is intended solely for offensive security, adversary emulation, security validation, threat modeling, and risk assessment within environments where explicit permission has been granted.

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

- AI-Powered Autonomous Attack Path Prediction (AAPP)  
- Multi-Agent Red Team Simulation (MART)  
- Core Security Engine & Orchestration  
- Graph-Based Attack Path Modeling  
- MITRE ATT&CK-Aligned Adversary Behavior  
- Risk-Based Security Posture Analysis  
- ML-Assisted Vulnerability Prioritization

For full details, refer to the [Features](docs/product/features.md) file.

## Demo

This section demonstrates a runnable attack-path simulation for the AAPP-MART cybersecurity engine.

### Usage

```bash
python aapp_mart.py --target 10.10.20.15
```

### Output

```text
=== AAPP-MART — AI-Powered Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine ===

[*] Simulation Workflow Started
[*] Initial Entry Point: 10.10.20.15 (WORKSTATION-01, Linux) 

[+] [Agent-Recon       ] Reconnaissance       | MITRE: T1595 | Severity: LOW      | Status: SUCCESS | Active scanning detected on (10.10.20.15)
[+] [Agent-Access      ] Initial Access       | MITRE: T1078 | Severity: HIGH     | Status: SUCCESS | Valid account abuse
[+] [Agent-Exploitation] Privilege Escalation | MITRE: T1068 | CVE: CVE-2024-1086 | Severity: CRITICAL | Status: SUCCESS | Kernel privilege escalation simulated
[+] [Agent-Pivot       ] Lateral Movement     | MITRE: T1021 | Severity: HIGH     | Status: SUCCESS | Remote service pivoting to (10.10.20.45)
[+] [Agent-Collection  ] Collection           | MITRE: T1005 | Severity: CRITICAL | Status: SUCCESS | Backup data discovery and collection on (10.10.20.25)

[✓] Simulation Completed Successfully

=== COMPREHENSIVE RISK SUMMARY ===

[*] Target IP (Initial Entry Point) : 10.10.20.15 (WORKSTATION-01)
[*] Risk Score                      : 8.32/10 (HIGH)
[*] Summary                         : DC (10.10.20.45) breached via Workstation (10.10.20.15) kernel privilege escalation using CVE-2024-1086. Backup Server (10.10.20.25) compromise.
[*] Duration                        : 1.00s
[*] Simulated Step Count            : 5 Stages
[*] Affected Assets                 : 4 Systems (3 Compromised, 1 Isolated, 0 Blocked)
[*] Started At                      : 2026-01-01T01:01:01.123456+00:00
[*] Generated At                    : 2026-01-01T01:01:01.123456+00:00

--- Affected Critical Assets ---

[!] WORKSTATION-01       | IP: 10.10.20.15 | Type: Endpoint      | Severity: HIGH     | Status: Compromised | Detail: Initial Vector
[!] FILE-SERVER-01       | IP: 10.10.20.2  | Type: Storage       | Severity: HIGH     | Status: Isolated    | Detail: Domain Admin Access
[!] DOMAIN-CONTROLLER-01 | IP: 10.10.20.45 | Type: Identity/AD   | Severity: CRITICAL | Status: Compromised | Detail: Data Exfiltrated
[!] BACKUP-SERVER-01     | IP: 10.10.20.25 | Type: Backup Server | Severity: HIGH     | Status: Compromised | Detail: Backup Access

=== REPORT EXPORT FORMAT ===

[1] JSON Report
[2] CSV Report
[3] JSON + CSV Report

Select Report Format [1-3]: 3

[+] JSON Report Exported: logs/attack-path/attack_path_10_10_20_15_20260101_010101.json
[+] CSV Report Exported: logs/attack-path/attack_path_10_10_20_15_20260101_010101.csv
```

> [!NOTE]
> This IP/hostname is an example target used for demonstration purposes only.

## Installation

### Supported Operating Systems

- Linux — Recommended for development, testing, automation, and deployment  
- Windows — Supported for development and testing with Visual Studio Code and WSL2  
- macOS — Supported for local development and testing

### Requirements

- Python 3.11+
- Git
- pip
- Make
- pytest

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
pip install -r requirements-dev.txt
```

For full details, refer to the [Quick Start](docs/getting-started/quickstart.md) file.

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

- Fork the repository and create a feature or fix branch (e.g. `feature/your-feature`, `fix/bug-name`, `docs/update-readme`, `chore/dependency-update`).
- Make your changes and add relevant tests.
- Use clear commit messages (e.g. Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`).
- Ensure all tests pass (`pytest`) and code style checks (e.g. `make lint`).
- Open a pull request referencing related issues when possible.
- All PRs must pass CI checks before merging.

Please open an issue before submitting major changes or new features.

See [CONTRIBUTING](CONTRIBUTING.md) for detailed contribution guidelines.

## Roadmap

Planned improvements include:

- Improved AI-Powered Attack Path Prediction
- Path-aware risk scoring based on simulated attack chains
- Optional visualization layer for simulation outputs
- Plugin ecosystem for custom modules and agents
- Distributed simulation support

For the full roadmap and upcoming features, see [Roadmap](ROADMAP.md).

## Security

If you discover a security vulnerability, please follow our responsible disclosure process.

See [SECURITY](SECURITY.md) for instructions on reporting issues securely.
