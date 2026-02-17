# AAPP & MART Detailed Overview

---

## AAPP (AI Attack Path Predictor)

AAPP predicts attack paths by evaluating:

- Services, configurations, and permissions
- Known vulnerabilities and exploitability
- Privilege escalation possibilities
- Asset criticality and exposure

### AI Engine

- **Decision Logic:** Rule-based / ML / Hybrid (per module).  
- **Learning:** Offline or deterministic scoring  
- **Decision Factors:** Exploitability, exposure, privilege, asset criticality

## MART (Multi-Agent Red Team)

MART simulates realistic adversary behaviors:

- Reconnaissance agent  
- Exploitation agent  
- Privilege escalation agent  
- Lateral movement agent  
- Persistence agent  
- Reporting agent

Agents collaborate autonomously to execute predicted attack paths safely, without destructive payloads.

## CORE — Simulation Brain

CORE is the central orchestration engine that coordinates the entire system:

- Initializes and runs **AAPP** to generate attack paths
- Starts **MART** agents and manages their interactions
- Executes deterministic simulation loops
- Maintains the **Knowledge Graph** as global state
- Generates final analytical reports
- Ensures reproducibility and traceable execution

---

## Integration

- AAPP generates attack paths → MART simulates them in controlled environments
- Produces human-readable and structured reports (JSON, PDF, etc.)
- Aligns with MITRE ATT&CK framework for standardized mapping
