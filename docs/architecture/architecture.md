# Architecture

This document outlines the system architecture, core components, and internal data flow.

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
│   ├── GLOSSARY.md
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
│   ├── configuration
│   │   └── configuration.md
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
│   │   ├── troubleshooting.md
│   │   └── usage.md
│   ├── legal
│   │   ├── ethics.md
│   │   ├── licensing.md
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
├── pyproject.toml
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
│       │   ├── __init__.py
│       │   ├── analyzer.py
│       │   ├── feature_pipeline.py
│       │   ├── models.py
│       │   ├── prediction.py
│       │   ├── predictor.py
│       │   └── scoring.py
│       ├── agents
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── discovery.py
│       │   ├── lateral_movement.py
│       │   ├── privilege_escalation.py
│       │   ├── recon.py
│       │   └── validation.py
│       ├── api
│       │   ├── __init__.py
│       │   ├── app.py
│       │   ├── routes
│       │   │   ├── __init__.py
│       │   │   ├── attack_graph.py
│       │   │   ├── prediction.py
│       │   │   ├── reports.py
│       │   │   ├── risk.py
│       │   │   └── simulation.py
│       │   └── schemas.py
│       ├── attack_graph
│       │   ├── __init__.py
│       │   ├── builder.py
│       │   ├── edge.py
│       │   ├── graph.py
│       │   ├── node.py
│       │   └── path_finder.py
│       ├── audit
│       │   ├── __init__.py
│       │   ├── events.py
│       │   ├── logger.py
│       │   └── models.py
│       ├── cli
│       │   ├── __init__.py
│       │   ├── commands
│       │   │   ├── __init__.py
│       │   │   ├── graph.py
│       │   │   ├── predict.py
│       │   │   ├── report.py
│       │   │   ├── risk.py
│       │   │   └── simulate.py
│       │   └── main.py
│       ├── cve
│       │   ├── __init__.py
│       │   ├── analyzer.py
│       │   ├── cache.py
│       │   ├── fetcher.py
│       │   └── models.py
│       ├── engine
│       │   ├── __init__.py
│       │   ├── contracts.py
│       │   ├── exceptions.py
│       │   ├── pipeline.py
│       │   ├── state_machine.py
│       │   └── utils.py
│       ├── events
│       │   ├── __init__.py
│       │   ├── event.py
│       │   ├── event_types.py
│       │   ├── publisher.py
│       │   └── subscriber.py
│       ├── mart
│       │   ├── __init__.py
│       │   ├── behavior.py
│       │   ├── coordinator.py
│       │   ├── state.py
│       │   └── strategy.py
│       ├── mitre
│       │   ├── __init__.py
│       │   ├── attack_matrix.py
│       │   ├── mapper.py
│       │   ├── models.py
│       │   ├── tactics.py
│       │   └── techniques.py
│       ├── model
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── loader.py
│       │   ├── manager.py
│       │   ├── metadata.py
│       │   └── registry.py
│       ├── observability
│       │   ├── __init__.py
│       │   ├── health.py
│       │   ├── logging.py
│       │   └── metrics.py
│       ├── plugins
│       │   ├── __init__.py
│       │   ├── exceptions.py
│       │   ├── interfaces.py
│       │   ├── loader.py
│       │   └── metadata.py
│       ├── policy
│       │   ├── __init__.py
│       │   ├── evaluator.py
│       │   ├── loader.py
│       │   ├── models.py
│       │   └── rules.py
│       ├── reports
│       │   ├── __init__.py
│       │   ├── csv_report.py
│       │   ├── generator.py
│       │   ├── json_report.py
│       │   └── models.py
│       ├── risk
│       │   ├── __init__.py
│       │   ├── calculator.py
│       │   ├── factors.py
│       │   ├── models.py
│       │   └── scorer.py
│       ├── runtime
│       │   ├── __init__.py
│       │   ├── context.py
│       │   ├── execution.py
│       │   └── execution_result.py
│       ├── shared
│       │   ├── __init__.py
│       │   ├── constants.py
│       │   ├── utils.py
│       │   └── validators.py
│       ├── simulation
│       │   ├── __init__.py
│       │   ├── result.py
│       │   ├── scenario.py
│       │   ├── simulator.py
│       │   ├── state.py
│       │   └── step.py
│       ├── storage
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── filesystem.py
│       │   └── sqlite.py
│       ├── threat_intel
│       │   ├── __init__.py
│       │   ├── client.py
│       │   ├── correlation.py
│       │   ├── feeds.py
│       │   ├── indicators.py
│       │   └── models.py
│       └── workflows
│           ├── __init__.py
│           ├── base.py
│           ├── prediction.py
│           ├── risk.py
│           └── simulation.py
└── tests
    ├── aapp
    │   └── test_aapp.py
    ├── agents
    │   └── test_agents.py
    ├── api
    │   └── test_api.py
    ├── attack_graph
    │   └── test_attack_graph.py
    ├── audit
    │   └── test_audit.py
    ├── conftest.py
    ├── cve
    │   └── test_cve.py
    ├── demo
    │   └── test_aapp_mart.py
    ├── engine
    │   └── test_engine.py
    ├── mart
    │   └── test_mart.py
    ├── mitre
    │   └── test_mitre.py
    ├── model
    │   └── test_model.py
    ├── observability
    │   └── test_observability.py
    ├── plugins
    │   └── test_plugins.py
    ├── policy
    │   └── test_policy.py
    ├── reports
    │   └── test_reports.py
    ├── risk
    │   └── test_risk.py
    ├── simulation
    │   └── test_simulation.py
    ├── storage
    │   └── test_storage.py
    ├── threat_intel
    │   └── test_threat_intel.py
    └── workflows
        └── test_workflows.py
```

## Overview

AAPP-MART consists of three major subsystems:

### 1. AI-Powered Autonomous Attack Path Prediction (AAPP)

- Builds attack graphs, predicts likely attack paths, and prioritizes risks.

### 2. Multi-Agent Red Team Simulation (MART)

- Simulates attacker behavior using autonomous agents.

### 3. Core Orchestration (ENGINE)

- Orchestrates AAPP + MART, manages global state, and controls execution.

## Component Breakdown

### AI-Powered Autonomous Attack Path Prediction (AAPP)

Builds attack graphs, predicts likely attack paths, and prioritizes risks:

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
