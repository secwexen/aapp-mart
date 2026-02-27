# **v0.4.0 – Platform Expansion, Observability Integration, and System Enhancements**

This release delivers a significant expansion of AAPP‑MART’s core capabilities, introducing new functional modules, enhanced agent behaviors, an end‑to‑end observability layer, and substantial improvements across the simulation, prediction, and deployment pipelines. v0.4.0 builds on the stabilization work completed in v0.3.0 and marks a major step toward a fully modular, scalable, and production‑aligned multi‑agent security simulation platform.

## **1. Platform Expansion**

### **New Functional Modules**
AAPP‑MART now includes an extended set of operational modules under `src/aapp_mart/modules/`, enabling broader attack surface coverage and deeper system interaction:

- **Automation Module** — Task orchestration and automated workflow execution.
- **Memory Module** — Memory parsing and in‑depth forensic extraction.
- **Network Module** — Network scanning, port enumeration, and service discovery.
- **Offensive Module** — Credential testing, exploit execution, and cloud attack tooling.
- **System Module** — System information gathering and privilege evaluation.

These modules significantly expand the platform’s operational depth and agent capabilities.

## **2. Agent Framework Enhancements**

### **New and Updated Agents**
The agent ecosystem has been extended with additional offensive, forensic, and system‑level agents:

- Reconnaissance, exploitation, lateral movement, persistence, privilege escalation, and reporting agents.
- Forensic, network, and system agents for deeper environment interaction.
- Updated agent registry and behavior mapping (`behavior_to_technique.json`).

### **Behavioral Improvements**
- Expanded MITRE ATT&CK technique mappings.
- New behavior pipelines for multi‑step attack execution.
- Improved agent coordination and decision logic.

## **3. Attack Graph & Knowledge Graph Improvements**

Enhancements to the attack graph and knowledge graph subsystems include:

- Updated graph builder and rule engine (`graph_builder.py`, `technique_graph_rules.json`).
- Improved node/edge modeling for complex attack paths.
- Extended knowledge graph integration for contextual reasoning.

These updates strengthen the platform’s ability to model realistic adversarial movement.

## **4. Prediction, ML, and Reinforcement Learning Updates**

### **Prediction Engine**
- New hybrid, rule‑based, and ML‑based predictors.
- Updated model registry and validation pipeline.
- Expanded explainability features for model transparency.

### **Reinforcement Learning**
- RL agent, environment, memory, policy, and trainer modules added.
- Initial RL configurations and training workflows included.

These additions lay the foundation for adaptive, learning‑based attack path prediction.

## **5. Observability Layer (New)**

A comprehensive observability stack has been introduced to support monitoring, debugging, and operational insight.

### **Logging**
- Centralized logging configuration (`logging.yaml`)
- Promtail integration for log forwarding.

### **Metrics**
- Prometheus exporter for simulation and agent metrics.
- Prometheus configuration files included.

### **Tracing**
- OpenTelemetry configuration for distributed tracing.
- Jaeger integration for trace visualization.

### **Dashboards**
- Grafana dashboards for:
  - Agent activity
  - System health
  - Platform overview

This observability layer provides full visibility into system behavior and performance.

## **6. API, CLI, and Interface Enhancements**

### **API**
- Expanded endpoints for agents, prediction, and reporting.
- Updated OpenAPI/Swagger documentation.
- Improved request/response schemas.

### **CLI**
- New commands for simulation, scanning, and reporting.
- Enhanced CLI UX and error handling.

### **Dashboard**
- Backend updates for visualization components (timeline, attack graph, risk heatmap).

## **7. Deployment & Infrastructure Improvements**

### **Kubernetes & Helm**
- Helm chart added for streamlined deployment.
- Kubernetes manifests for service, ingress, and deployment.

### **Docker & Nginx**
- Updated Dockerfiles for backend and frontend.
- Production‑ready Nginx configuration.

### **Environment Configurations**
- Development, staging, and production environment templates.

These updates improve portability, scalability, and operational readiness.

## **8. Documentation Expansion**

The documentation set has been significantly expanded and reorganized:

- Architecture overview  
- Feature documentation  
- API reference  
- CLI guide  
- Deployment guide  
- Ethical use guidelines  
- Threat model  
- Prediction engine documentation  
- Examples and tutorials  

This provides a more complete, structured, and professional onboarding experience for users and contributors.

## **9. Testing & Quality Improvements**

- New API, integration, and end‑to‑end tests.
- Predictor stability tests.
- Offline mode validation.
- Performance testing via Locust and JMeter.

Test coverage and reliability have improved across the platform.

## **Status Note**

v0.4.0 remains a **pre‑release**. While the platform has expanded significantly and core components are stable, several advanced modules, RL policies, and attack graph rules are still under active development. This release is intended for early adopters, contributors, and research environments.

## What's Changed

* Potential fix for code scanning alert no. 8: Workflow does not contain permissions by @secwexen in https://github.com/secwexen/aapp-mart/pull/12
* Bump actions/checkout from 3 to 6 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/13
* Bump actions/setup-python from 3 to 6 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/17
* Bump actions/cache from 3 to 5 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/16
* Bump actions/upload-artifact from 3 to 6 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/14
* Bump actions/download-artifact from 4 to 7 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/15
* Potential fix for code scanning alert no. 9: Workflow does not contain permissions by @secwexen in https://github.com/secwexen/aapp-mart/pull/18
* Potential fix for code scanning alert no. 3: Workflow does not contain permissions by @secwexen in https://github.com/secwexen/aapp-mart/pull/20
* Potential fix for code scanning alert no. 10: Workflow does not contain permissions by @secwexen in https://github.com/secwexen/aapp-mart/pull/21
* Bump github/codeql-action from 2 to 4 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/26
* Bump actions/checkout from 4 to 6 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/25
* Bump docker/build-push-action from 5 to 6 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/24
* Bump actions/setup-python from 3 to 6 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/23
* Bump actions/upload-artifact from 4 to 6 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/22

## New Contributors

* @dependabot[bot] made their first contribution in https://github.com/secwexen/aapp-mart/pull/13

**Full Changelog**: https://github.com/secwexen/aapp-mart/compare/v0.3.0...v0.4.0
