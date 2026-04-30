# Architecture

AAPP-MART is a modular, extensible, and autonomous security analysis framework.  
It combines AI-Autonomous Attack Path Prediction (AAPP) with a Multi-Agent Red Team Simulation Engine (MART).

This document outlines the system architecture, core components, and internal data flow.

## 1. High-Level Overview

AAPP-MART consists of three major subsystems:

1. **AAPP (AI-Autonomous Attack Path Prediction)**  
   Builds attack graphs, predicts likely attack paths, and prioritizes risks.

2. **MART (Multi-Agent Red Team Simulation Engine)**  
   Simulates attacker behavior using autonomous agents.

3. **CORE (Simulation Brain)**  
   Orchestrates AAPP + MART, manages global state, and controls execution.

All components communicate through a shared **Knowledge Graph**.

## 2. Directory Structure

```
aapp-mart
├── assets/
├── configs/
├── docs/
├── examples/
├── helm/
├── observability/
├── scripts/
├── src/
│   └── aapp_mart/
│       ├── agents/  
│       ├── cli/  
│       ├── domain/                
│       ├── common/  
│       ├── integrations/  
│       ├── mart/  
│       ├── modules/  
│       ├── offline/  
│       ├── rl/  
│       ├── utils/  
│       └── main.py  
├── tests/
├── CHANGELOG.md
├── CITATION.cff
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── DISCLAIMER.md
├── GOVERNANCE.md
├── LICENSE
├── LICENSE‑3RD‑PARTY.md
├── MAINTAINERS
├── NOTICE
├── README.md
├── SECURITY.md
├── SUPPORT.md
├── dev-requirements.txt
├── requirements.txt
└── trivyignore
```

## 3. Component Breakdown

### 3.1 AAPP — AI-Autonomous Attack Path Prediction

Responsible for:

- Parsing target data  
- Building attack graphs  
- Predicting attack paths  
- Scoring risks  

### 3.2 MART — Multi-Agent Red Team Simulation Engine

Simulates attacker behavior using specialized agents:

- Reconnaissance  
- Exploitation  
- Privilege escalation  
- Lateral movement  
- Persistence  
- Reporting  

All agents inherit from `agent_base.py` and share memory via the Knowledge Graph.

### 3.3 CORE — Simulation Brain

Coordinates the entire system:

- Runs AAPP  
- Initializes MART agents  
- Executes simulation loops  
- Maintains global state  
- Generates final reports