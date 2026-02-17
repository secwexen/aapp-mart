# CONCEPTS.md

## Overview

This document introduces the key concepts and terminology behind **AAPP-MART** – the Autonomous Attack Path Prediction & Multi-Agent Red Team simulation engine. Understanding these concepts is essential for using, extending, or reviewing the system effectively.

---

## Core Concepts

### 1. Attack Graph

An **Attack Graph** is a directed graph (G = (V, E)) where:

- **Vertices (V)** represent assets or security-relevant states (hosts, users, privileges, network services).
- **Edges (E)** represent feasible transitions an attacker could exploit (vulnerability exploitation, privilege escalation, lateral movement).

Edges are annotated with **likelihood** and **exploitability weights** to support predictive scoring.

---

### 2. AAPP (AI Attack Path Predictor)

**AAPP** analyzes the target environment to predict the most probable attack paths. It uses:

- Graph-based analysis
- Rule-based, ML, or hybrid AI decision logic
- Factors such as exploitability, exposure, and asset criticality

AAPP outputs **risk-scored attack paths** for simulation or reporting.

---

### 3. MART (Multi-Agent Red Team)

**MART** is the autonomous red team engine that simulates adversary behavior using specialized agents:

- **Reconnaissance Agent** – gathers environmental information
- **Exploitation Agent** – attempts logical exploit chains
- **Privilege Escalation Agent** – escalates permissions when possible
- **Lateral Movement Agent** – moves across network boundaries
- **Persistence Agent** – simulates maintaining access
- **Reporting Agent** – logs and summarizes actions

Agents collaborate and make decisions independently, creating realistic attack simulations.

---

### 4. Simulation Modes

- **Prediction-Only Mode** – builds attack graphs and forecasts paths without executing actions. Safe for continuous monitoring.
- **Simulation Mode** – runs controlled, non-destructive simulations to evaluate defenses. Intended for lab environments.

---

### 5. Risk Scoring

Risk is calculated as:

$$
Risk = Likelihood \times Impact
$$

Where:

- **Likelihood** – probability of a given path succeeding
- **Impact** – potential effect on assets or operations

Additional modifiers include **asset criticality weighting**, **CVSS integration**, and **confidence scores**.

---

### 6. Operational Safeguards

AAPP-MART is designed for safe, authorized usage:

- No destructive payloads
- No uncontrolled exploitation
- Scope is explicitly defined
- Detailed logging and deterministic execution for auditability

---

### 7. MITRE ATT&CK Alignment

AAPP-MART maps predicted paths and agent behaviors to **MITRE ATT&CK tactics and techniques** for standardized reporting and defensible results.

---

### 8. Deployment Patterns

- **Standalone CLI** – local execution and automation
- **REST API (planned)** – programmatic integration
- **Air-Gapped / Offline Mode** – isolated environments
- **Containerization (planned)** – Docker-based deployments

---

## References

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [CVSS v3.1 Specification](https://www.first.org/cvss/specification-document)
- [AAPP-MART Architecture & Documentation](architecture.md)
