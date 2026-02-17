# Risk Scoring Model

AAPP-MART calculates risk using a structured composite model:

$$
Risk = Likelihood \times Impact
$$

This document describes how risk is derived, weighted, and reported.

---

## 1. Likelihood

Likelihood represents the probability of a given attack path being successful.  
It is derived from:

- Vulnerability exploitability
- Exposure level
- Privilege requirements
- Chaining feasibility within the attack graph

---

## 2. Impact

Impact quantifies the potential effect of a successful attack.  
It is weighted using:

- Asset criticality
- Privilege escalation level
- Lateral movement amplification
- Business sensitivity (if provided)

---

## 3. Asset Criticality Weighting

Each asset may be assigned a criticality factor to adjust the risk:

$$
AdjustedRisk = Risk \times AssetWeight
$$

This allows the model to prioritize more critical assets in scoring and reporting.

---

## 4. CVSS Integration

If vulnerability scan data is provided, the system can incorporate **CVSS (Common Vulnerability Scoring System)** metrics aligned with FIRST standards.  

- CVSS values act as input modifiers, not sole determinants.
- This integration enhances risk scoring accuracy while maintaining deterministic control.

---

## 5. Confidence Score

Each reported risk includes a confidence indicator based on:

- Completeness of input data
- Assumption density
- Coverage of the simulated path in the attack graph

This ensures transparency and supports reproducibility of the results.

---

## 6. Security Boundaries & Operational Safeguards

AAPP-MART is designed as a controlled simulation engine. Safeguards include:

- **Non-destructive simulation enforcement**
- No payload execution
- No arbitrary command execution on targets
- No uncontrolled exploitation logic
- No automated scanning beyond defined scope

### 6.1 Scope Restriction

- Targets must be explicitly defined.
- The engine does not autonomously expand scope.

### 6.2 Operational Controls

- Structured logging of all simulation steps
- Deterministic execution boundaries
- Configurable simulation modes (Prediction-Only vs Simulation)

These constraints ensure that AAPP-MART remains a defensive validation platform rather than an offensive exploitation tool.

---

## References

- [CVSS v3.1 Specification](https://www.first.org/cvss/specification-document)
- [AAPP-MART Attack Graph & Risk Modeling Overview](docs/architecture.md)
