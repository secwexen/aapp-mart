# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-01-16

### Added
- Initial project skeleton and core directory structure
- Quick Start example demonstrating basic usage
- Installation instructions and dependency setup
- Testing framework setup using pytest
- Ethical Use guidelines and legal disclaimer

### Notes
- This is an early-stage, pre-release version.
- Core attack simulation and multi-agent logic are still under active development.
- Breaking changes may occur in future `0.x` releases.

## [0.2.0] - 2026-02-03

### Added
- Major updates in repo `aapp-mart`
- Major updates in `src/aapp_mart/`
- New modules under `src/aapp_mart/modules` (automation, memory, network, system)
- New agents and behaviors under `src/aapp_mart/mart`
- ML training dataset and features in `ml_training/`

### Fixed
- Potential fix for GitHub Actions workflow permission alerts (#7)

⚠️ Core simulation engine and attack orchestration are still under active development. This is a **pre-release**.

## [0.3.0] - 2026-02-05

### Added
- Core Simulation Engine files completed.
- Updated ML training files and models.
- Bug fixes and minor enhancements across modules.
- CLI/API usage improvements and documentation updates.

⚠️ Note: While the core features are now stable, some advanced modules and experimental agents are still under development. This release is intended for testing, early adoption, and contribution purposes.

# **[0.4.0] – 2026-02-27**

### **Added**
- New functional modules under `src/aapp_mart/modules/`:
  - automation, memory, network, offensive, system  
- Expanded agent framework with new offensive, forensic, network, and system agents  
- Updated behavior mappings and multi‑step attack behavior pipelines  
- Observability stack:
  - centralized logging, Promtail integration  
  - Prometheus metrics exporter  
  - OpenTelemetry tracing + Jaeger integration  
  - Grafana dashboards (agent activity, system health, platform overview)  
- Reinforcement Learning components:
  - RL agent, environment, memory, policy, trainer  
- New API endpoints and expanded CLI commands (simulate, scan, report)  
- Helm chart and updated Kubernetes manifests  
- Expanded documentation (architecture, features, API, CLI, deployment, threat model, prediction engine, examples)  
- New API, integration, end‑to‑end, stability, and performance tests  

### **Changed**
- Improved attack graph and knowledge graph engine  
- Updated prediction engine, ML models, and model registry  
- Enhanced dashboard backend (timeline, attack graph, risk heatmap)  
- Improved Dockerfiles, Nginx configuration, and deployment pipeline  
- Updated environment configuration templates (dev, staging, prod)  

### **Fixed**
- Multiple GitHub Actions workflow permission issues  
- Minor bugs across modules and agents  

### **Notes**
- This version is a **pre‑release**.  
- Some advanced modules, RL policies, and attack graph rules remain under active development.

### **Full Changelog**
https://github.com/secwexen/aapp-mart/compare/v0.3.0...v0.4.0
