# AAPP-MART  

<p align="center">
<img src="assets/images/aapp-mart-logo.png" width="250" alt="aapp-mart-logo">
</p>

![Build](https://img.shields.io/github/actions/workflow/status/secwexen/aapp-mart/ci.yml?branch=main&label=Build)
![CodeQL](https://img.shields.io/github/actions/workflow/status/secwexen/aapp-mart/codeql.yml?branch=main&label=CodeQL)
![Python Versions](https://img.shields.io/pypi/pyversions/aapp-mart)
![License](https://img.shields.io/github/license/secwexen/aapp-mart)
[![Website](https://img.shields.io/website?url=https://secwexen.github.io/aapp-mart/)](https://secwexen.github.io/aapp-mart/)
![Status](https://img.shields.io/badge/status-early--stage-brightgreen)

## Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine

**AAPP‑MART (Autonomous Attack Path Prediction & Multi‑Agent Red Team)** is an open‑source Python engine for offensive security research and automated risk assessment. It combines AI‑driven attack‑path prediction with autonomous adversarial simulation to model how attackers move through an environment and to surface actionable security insights.

Unlike traditional static vulnerability scanning, AAPP‑MART blends predictive analytics with multi‑agent red‑team behavior to provide continuous security evaluation. Its architecture helps defenders anticipate attack strategies, validate controls, and understand real‑world risk through repeatable and data‑driven simulations.  
  
For full documentation and guides, visit the official [AAPP-MART Website](https://secwexen.github.io/aapp-mart/).

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

## Conceptual Usage Example

The following illustrates the intended Python API design once the core engine is fully implemented:

```python
from aapp_mart.core.orchestrator import AAPP_MART

engine = AAPP_MART(target="192.168.1.10")
engine.run()
report = engine.get_report()
print(report)
```

> This example reflects the intended public API design.  
> Core orchestration modules are currently under development.  
> See [API Reference](docs/api_reference.md) and [Architecture](docs/architecture.md) for interface details and system structure.  

---

## Legal & Authorized Use

AAPP-MART is intended solely for authorized security assessment, defensive threat modeling, 
and controlled adversary simulation within environments where explicit permission has been granted.

The system is designed for non-destructive analysis and does not support uncontrolled exploitation. 
Users are responsible for ensuring lawful and policy-compliant usage.

---

## Market Positioning & Research Foundations

AAPP-MART sits at the intersection of **academic attack graph modeling**, **BAS tooling**, and **AI-assisted adversary simulation**, combining **deterministic graph-based prediction** with **controlled autonomous simulation**.

It continuously models, predicts, and simulates attacker behavior, providing **forward-looking defensive validation**.

Built on research-grade principles:

- **Attack Graph Theory** – Models assets, privileges, and attacker transitions
- **Risk Modeling** – Likelihood × Impact framework
- **Deterministic Simulation** – Predictable multi-agent behavior
- **Graph Traversal** – DFS, Best-First, or A* exploration

Threat modeling ensures clarity and reproducibility:

- **STRIDE** – Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Privilege Escalation
- **Adversary Capability Model** – Attacker skills, access scope, potential actions
- **Formal Risk Notation** – Transparent likelihood, impact, and path scoring

**Conclusion:** AAPP-MART is a defensible, explainable, and academically credible simulation engine, elevating it from a standard tool to a research-grade security platform.

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

### **AAPP (AI Attack Path Predictor)**  
Predicts the most likely attack paths by analyzing services, permissions, vulnerabilities, and configuration weaknesses.

#### **AI Engine**
Clarifying AAPP-MART’s AI approach:

- **Decision Logic** – Rule-based / ML / Hybrid (per module).  
- **Learning** – Offline training or deterministic scoring.  
- **Decision Factors** – Exploitability, exposure, privileges, asset criticality.

Explicit AI definition ensures credibility, reproducibility, and clarity for users and reviewers.

### **MART (Multi-Agent Red Team)**  
Executes autonomous red team simulations using specialized AI agents that emulate real attacker behavior.

Together, they create a fully automated offensive security engine capable of forecasting and simulating attacks end-to-end.

### **CORE Orchestration Engine**
The CORE Orchestration Engine is the central coordination layer of AAPP‑MART. It manages multi‑agent behavior, controls the execution flow of attack simulations, and ensures consistent interaction between all system modules.

---

## Docs & Resources

Detailed guides and references are also available in the repository:

- [Threat Model](docs/threat_model.md)
- [Risk Model](docs/risk_model.md)
- [Deployment Guide](docs/deployment.md)
- [Full Installation Guide](docs/installation.md)
- [Module Development](docs/modules.md)
- [Prediction Engine Details](docs/prediction_engine.md)
- [Examples & Quick Starts](docs/examples.md)
- [Roadmap & Milestones](docs/roadmap.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [Security Policy](SECURITY.md)

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

Early-stage open source project. Core implementation is still in progress.   

AAPP-MART is currently under active development.
This repository provides the foundational architecture, core interfaces,
and initial logic of the AAPP-MART engine.

Advanced prediction models, autonomous agent behaviors,
and controlled simulation capabilities are being implemented progressively.

---

## Support & Community

⭐ Found AAPP-MART useful? Give us a star and support the project!  
💬 Join discussions, report issues, or contribute your ideas!  

For support, questions, or feature requests, please open an issue:
[Open an issue on GitHub](https://github.com/secwexen/aapp-mart/issues)

For ideas and general discussions, use GitHub Discussions.

---

## Security

If you discover a security vulnerability, please follow our responsible disclosure process.

[Read SECURITY.md](SECURITY.md) for instructions on reporting issues securely. 

---

## Author

**Secwexen** – Project Lead & Maintainer   
**GitHub:** [github.com/secwexen](https://github.com/secwexen)  
