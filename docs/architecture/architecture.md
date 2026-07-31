# Architecture

This document outlines the system architecture, core components, and internal data flow.

## High-Level Overview

AAPP-MART consists of three major subsystems:

1. AI-Powered Autonomous Attack Path Prediction (AAPP)  
   Builds attack graphs, predicts likely attack paths, and prioritizes risks.

2. Multi-Agent Red Team Simulation (MART)  
   Simulates attacker behavior using autonomous agents.

3. Core Orchestration (ENGINE)  
   Orchestrates AAPP + MART, manages global state, and controls execution.

All components communicate through a shared Knowledge Graph.

## Project Structure

```text
aapp-mart/
│   ACKNOWLEDGEMENTS.md
│   bandit.yaml
│   CHANGELOG.md
│   CITATION.cff
│   CODE_OF_CONDUCT.md
│   CONTRIBUTING.md
│   requirements-dev.txt
│   DISCLAIMER.md
│   Dockerfile
│   docker-compose.yml
│   GOVERNANCE.md
│   LICENSE
│   LICENSE‑3RD‑PARTY.md
│   MAINTAINERS
│   Makefile
│   MANIFEST.in
│   mypy.ini
│   NOTICE
│   noxfile.py
│   pyproject.toml
│   pytest.ini
│   README.md
│   requirements.txt
│   ROADMAP.md
│   SBOM.md
│   SECURITY.md
│   SUPPORT.md
│           
├─── assets/
│   └─── images/
│           
├─── configs/
│           
├─── data/
│   └─── sample_targets/
│           
├─── demo/
│       
├─── docs/
│   ├─── ai/
│   ├─── architecture/
│   ├─── concepts/
│   ├─── contributing/
│   ├─── executive/
│   ├─── guides/
│   ├─── legal/
│   ├─── product/
│   ├─── reference/
│   ├─── research/
│   └─── start-here/
│           
├─── examples/
│   └─── scripts/
│           
├─── helm/
│   └─── aapp-mart/
│       └─── templates/
│               
├─── observability/
│   ├─── grafana_dashboards/     
│   ├─── logging/     
│   └─── metrics/
│           
├─── scripts/
│   ├─── ci/    
│   ├─── dev/     
│   └───ops/
│           
├─── src/
│   └─── aapp_mart/
│       │   
│       ├─── api/
│       │   ├─── docs/
│       │   ├─── endpoints/
│       │   └─── schemas/
│       │           
│       ├─── attack_graph/
│       │       
│       ├─── cli/
│       │   │   
│       │   ├─── commands/
│       │   ├─── data/
│       │   │   └─── sample_targets/
│       │   └─── examples/
│       │       
│       ├─── cve/
│       │       
│       ├─── domain/
│       │   ├─── agents/
│       │   │   └─── custom/
│       │   │           
│       │   ├─── predictors/
│       │   │       
│       │   ├─── reports/
│       │   │   ├─── exporters/
│       │   │   └─── templates/
│       │   │       └─── attack/
│       │   │               
│       │   └─── risk/
│       │           
│       ├─── integrations/
│       │   └─── siem/
│       │           
│       ├─── mart/
│       │   └─── offensive/
│       │           
│       ├─── modules/
│       │   ├─── automation/
│       │   ├─── memory/
│       │   ├─── network/
│       │   ├─── offensive/
│       │   └─── system/
│       │           
│       ├─── network/
│       ├─── offline/
│       ├─── rl/
│       └─── utils/
│       
└─── tests/
    └─── api/
```

## Component Breakdown

### AI-Powered Autonomous Attack Path Prediction (AAPP)

Responsible for:

- Parsing target data  
- Building attack graphs  
- Predicting attack paths  
- Scoring risks  

### Multi-Agent Red Team Simulation (MART)

Simulates attacker behavior using specialized agents:

- Reconnaissance  
- Exploitation  
- Privilege escalation  
- Lateral movement  
- Persistence  
- Reporting

### Core Orchestration (ENGINE)

Coordinates the entire system:

- Runs AAPP  
- Initializes MART agents  
- Executes simulation loops  
- Maintains global state  
- Generates final reports