# Frequently Asked Questions

This document provides answers to the most frequently asked questions about **AAPP-MART**.

## 1. What is AAPP-MART?

**AAPP-MART** (AI-Powered Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine).

It uses AI-assisted prediction and multi-agent simulation to help security teams identify potential attack paths, assess risks, and prioritize defensive improvements before exploitation occurs.

## 2. How does AAPP-MART differ from traditional penetration testing?

Traditional penetration testing is typically **manual, time-bound, and human-driven**, meaning results depend heavily on tester experience and scope limitations.

AAPP-MART complements traditional security assessments through:

- AI-assisted attack-path prediction
- Graph-based attack-path analysis
- Multi-agent adversary simulation
- Repeatable and structured security evaluation

It models attacker behavior dynamically across an environment using predictive attack-path analysis rather than executing a fixed test plan.

## 3. Is AAPP-MART an offensive hacking tool?

No. AAPP-MART is designed for authorized security simulation and defensive research only. It does not function as an uncontrolled exploitation framework.

Its purpose is to:

- Simulate attacker behavior in controlled environments
- Identify potential attack paths before real attackers do
- Improve defensive posture and detection engineering

It should only be used in environments where explicit permission has been granted.

## 4. What problems does AAPP-MART solve?

AAPP-MART addresses limitations in traditional security approaches by providing:

- Better visibility into multi-step attack chains
- Prioritization of high-risk attack paths
- Repeatable simulation of modeled adversarial behavior
- Context-aware risk modeling instead of isolated vulnerability reporting

## 5. Does AAPP-MART replace human red teams?

No. AAPP-MART is designed to **augment, not replace**, human expertise.

It helps security teams:

- Automate repetitive analysis
- Explore more attack scenarios than manually feasible
- Identify non-obvious attack chains

Human analysts remain essential for interpretation, validation, and strategic decision-making.

## 6. What outputs does AAPP-MART provide?

AAPP-MART provides structured security analysis results to help users understand potential attack paths and associated risks.

Depending on the capabilities enabled in the installed version, outputs may include:

- Predicted attack paths and attack graph analysis
- Risk scores and security findings
- MITRE ATT&CK tactic and technique mappings
- Multi-agent simulation results
- JSON and CSV reports

These outputs help security researchers and red, blue, and purple teams analyze potential attack scenarios, prioritize risks, and evaluate defensive controls in authorized environments.

## 7. How can I get started with AAPP-MART?

Clone the repository, set up a Python virtual environment, and install the project dependencies according to the installation guide.

For the initial setup:

1. Clone the AAPP-MART repository.
2. Create and activate a Python virtual environment.
3. Install AAPP-MART using the documented installation instructions.
4. Follow the [Quick Start](getting-started/quickstart.md) guide to explore the available capabilities.

Refer to the [Installation Guide](getting-started/installation.md) for detailed setup instructions and the [Usage Guide](guides/usage.md) for supported workflows.

## 8. What data does AAPP-MART use for security analysis?

AAPP-MART analyzes available environment and security information to model potential attack paths, evaluate risks, and support adversary simulation.

Depending on the analysis and configured capabilities, inputs may include:

- Asset and environment information
- Network and service relationships
- Vulnerability and CVE data
- Attack graph and security configuration data
- MITRE ATT&CK tactics and techniques
- Threat intelligence indicators

The quality and completeness of the input data influence the relevance of predictions and risk assessments. Users should validate important findings against their actual environment and use the system only within explicitly authorized assessment scopes.
