# AAPP-MART Architecture

AAPP-MART is a modular, extensible, and autonomous security analysis framework.  
It combines AI-driven Attack Path Prediction (AAPP) with a Multi-Agent Red Team (MART) engine.

This document outlines the system architecture, core components, and internal data flow.

## 1. High-Level Overview

AAPP-MART consists of three major subsystems:

1. **AAPP (Attack Path Predictor)**  
   Builds attack graphs, predicts likely attack paths, and prioritizes risks.

2. **MART (Multi-Agent Red Team)**  
   Simulates attacker behavior using autonomous agents.

3. **CORE (Simulation Brain)**  
   Orchestrates AAPP + MART, manages global state, and controls execution.

All components communicate through a shared **Knowledge Graph**.

## 2. Directory Structure

```
aapp-mart
├── src/
│   └── aapp_mart/
│       ├── aapp/                  # Attack Path Predictor
│       ├── agents/                # Autonomous attacker agents
│       ├── api/                   # REST API (optional)
│       ├── cli/                   # Command-line interface
│       ├── common/                # Common, reusable base classes or constants
│       ├── core/                  # Autonomous simulation brain
│       ├── integrations/          # Sample data & signatures
│       ├── mart/                  # Multi-Agent Red Team
│       ├── modules/               # Pluggable engine modules
│       ├── offline/               # Offline mode resources
│       ├── predictors/            # Prediction logic & models
│       ├── reports/               # Generated reports
│       ├── risk/                  # Risk engine and CVSS mapping
│       ├── rl/                    # Reinforcement learning agents & environment
│       ├── utils/                 # Pluggable engine modules
│       └── main.py                # AAPP-MART entry point
│ 
├── assets/
├── configs/
├── dashboard/
├── deployment/
├── docs/
├── examples/
├── helm/
├── internal_api/
├── kubernetes
├── ml_training/
├── observability
├── scripts/
├── tests/
├── CHANGELOG.md
├── CITATION.cff
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── DISCLAIMER.md
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── RELEASE_NOTES.md
├── SECURITY.md
├── SECURITY_SCANNER.md
├── bandit.yaml
├── docker-compose.observability.yaml
├── pyproject.toml
├── requirements-dev.txt
├── requirements.txt
└── trivyignore
```

## 3. Component Breakdown

### 3.1 AAPP — Attack Path Predictor

Responsible for:

- Parsing target data  
- Building attack graphs  
- Predicting attack paths  
- Scoring risks  

Key modules:

- `analyzer.py`
- `graph_builder.py`
- `predictor.py`
- `scoring.py`
- `models/`

### 3.2 MART — Multi-Agent Red Team

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

Key modules:

- `orchestrator.py`
- `simulation_engine.py`
- `knowledge_graph.py`

## 4. Knowledge Graph

Stores:

- Hosts  
- Services  
- Vulnerabilities  
- Credentials  
- Attack paths  
- Agent findings  

Acts as the shared memory for all agents.

## 5. Data Flow

```
Input → AAPP → Knowledge Graph → MART → Reports
```

## 6. Extensibility

AAPP-MART supports:

- New agents  
- New ML models  
- New scoring algorithms  
- New simulation modes  

## 7. Summary

AAPP-MART integrates predictive attack modeling with autonomous red-team simulation.  
Its architecture is modular, scalable, and designed for advanced security research.
