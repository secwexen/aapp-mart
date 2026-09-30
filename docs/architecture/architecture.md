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
aapp-mart
├── ACKNOWLEDGEMENTS.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── DISCLAIMER.md
├── Dockerfile
├── GOVERNANCE.md
├── LICENSE
├── LICENSE‑3RD‑PARTY.md
├── MAINTAINERS
├── MANIFEST.in
├── Makefile
├── NOTICE
├── README.md
├── ROADMAP.md
├── SBOM.md
├── SECURITY.md
├── SUPPORT.md
├── assets
│   └── images
│       └── aapp-mart-logo.png
├── data
│   └── samples
│       ├── example_input.json
│       └── example_output.json
├── demo
│   └── aapp_mart.py
├── deployment
│   ├── README.md
│   ├── helm
│   │   └── aapp-mart
│   │       ├── Chart.yaml
│   │       └── README.md
│   └── observability
│       └── README.md
├── docs
│   ├── FAQ.md
│   ├── README.md
│   ├── ai
│   │   ├── ai-powered-autonomous-attack-path-prediction.md
│   │   ├── models.md
│   │   ├── predictors.md
│   │   └── risk-model.md
│   ├── architecture
│   │   ├── architecture.md
│   │   ├── components.md
│   │   ├── design.md
│   │   ├── modules.md
│   │   └── threat-model.md
│   ├── concepts
│   │   ├── agents.md
│   │   └── concepts.md
│   ├── contributing
│   │   └── commit-convention.md
│   ├── executive
│   │   ├── executive-summary.md
│   │   ├── positioning.md
│   │   └── vision.md
│   ├── getting-started
│   │   ├── getting-started.md
│   │   ├── installation.md
│   │   └── quickstart.md
│   ├── guides
│   │   ├── cli.md
│   │   ├── deployment.md
│   │   ├── development.md
│   │   ├── testing.md
│   │   ├── troubleshooting.md
│   │   └── usage.md
│   ├── legal
│   │   ├── ethics.md
│   │   ├── privacy-policy.md
│   │   └── terms-of-service.md
│   ├── product
│   │   ├── differentiators.md
│   │   ├── examples.md
│   │   ├── features.md
│   │   ├── overview.md
│   │   └── what-is-aapp-mart.md
│   ├── reference
│   │   ├── api-reference.md
│   │   ├── licensing.md
│   │   └── references.md
│   ├── research
│   │   ├── benchmark.md
│   │   └── research.md
│   └── testing
│       └── testing.md
├── examples
│   ├── basic_simulation.py
│   ├── custom_agent_example.py
│   ├── integration_example.py
│   └── reports
│       └── risk_summary.json
├── models
│   └── README.md
├── observability
│   └── metrics
│       └── metrics.md
├── scripts
│   ├── ci
│   │   ├── lint.sh
│   │   └── test.sh
│   └── dev
│       ├── build_docs.sh
│       ├── format_code.sh
│       └── run_local.py
├── src
│   └── aapp_mart
│       ├── __init__.py
│       ├── __main__.py
│       ├── aapp
│       │   ├── analyzer.py
│       │   ├── feature_pipeline.py
│       │   └── scoring.py
│       ├── attack_graph
│       │   ├── builder.py
│       │   ├── graph.py
│       │   └── path_finder.py
│       ├── cli
│       │   ├── __init__.py
│       │   ├── commands
│       │   │   ├── predict.py
│       │   │   ├── report.py
│       │   │   └── simulate.py
│       │   └── main.py
│       ├── cve
│       │   ├── __init__.py
│       │   ├── cache.py
│       │   ├── fetcher.py
│       │   └── models.py
│       ├── domain
│       │   └── risk
│       │       └── cvss_calculator.py
│       ├── engine
│       │   ├── contracts.py
│       │   ├── exceptions.py
│       │   ├── pipeline.py
│       │   ├── state_machine.py
│       │   └── utils.py
│       ├── events
│       │   ├── event.py
│       │   ├── event_types.py
│       │   ├── publisher.py
│       │   └── subscriber.py
│       ├── plugins
│       │   ├── exceptions.py
│       │   ├── interfaces.py
│       │   ├── loader.py
│       │   └── metadata.py
│       ├── runtime
│       │   ├── context.py
│       │   ├── execution.py
│       │   └── execution_result.py
│       ├── shared
│       │   ├── constants.py
│       │   ├── utils.py
│       │   └── validators.py
│       └── storage
│           ├── __init__.py
│           ├── base.py
│           ├── filesystem.py
│           └── sqlite.py
└── tests
    ├── conftest.py
    ├── test_aapp.py
    ├── test_agents.py
    └── test_attack_graph.py
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
