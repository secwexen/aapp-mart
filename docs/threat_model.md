# Threat Model & Scope

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

# Input & Output Contract

## Inputs
AAPP-MART consumes structured security-relevant data, such as:

- Target identifiers (IP address, hostname, environment label)
- Asset and service metadata
- Optional vulnerability scan results
- Optional configuration and permission data

## Outputs
The engine produces analytical security artifacts, including:

- Predicted attack paths
- Simulated adversary decision flows
- Risk-scored findings
- Human-readable reports with mitigation guidance

---

# Modes of Operation

AAPP-MART operates in controlled modes designed for authorized security assessment and defensive validation.

## Prediction-Only Mode

- No active interaction with the target
- Builds attack graphs and forecasts attacker movement
- Safe for continuous assessment and design-time analysis

## Simulation Mode

- Executes non-destructive, controlled attack simulations
- Focuses on logic flow rather than payload execution
- Designed for lab environments and authorized testing only

Destructive actions and uncontrolled exploitation are intentionally excluded.

---

# MITRE ATT&CK Alignment

AAPP-MART aligns its prediction and simulation logic with the MITRE ATT&CK framework to ensure standardized, explainable, and defensible security findings.

Agent behaviors and predicted attack paths are mapped to high-level ATT&CK tactics and techniques, including but not limited to:

- **Reconnaissance (TA0043)**
  - Example: T1595 – Active Scanning
- **Initial Access (TA0001)**
  - Example: T1190 – Exploit Public-Facing Application
- **Credential Access (TA0006)**
  - Example: T1003 – OS Credential Dumping
- **Privilege Escalation (TA0004)**
  - Example: T1068 – Exploitation for Privilege Escalation
- **Lateral Movement (TA0008)**
  - Example: T1021 – Remote Services
- **Persistence (TA0003)**
  - Example: T1547 – Boot or Logon Autostart Execution

This mapping is used for risk scoring, reporting, and defensive recommendations.
