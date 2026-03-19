# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/).

# AAPP‑MART v1.0.1 — Initial Open Source Release

Welcome to the first open‑source release of **AAPP‑MART**.  
This version introduces the core architecture, modules, APIs, Helm charts, observability components, and documentation that form the foundation of the project.

## Core Features

- Modular prediction engine  
- Agent framework (offensive, forensic, network, system)  
- Risk engine with CVSS scoring  
- API endpoints for agents, prediction, and reporting  
- Command‑line interface (CLI)  
- Comprehensive test suite  

## Deployment

- Helm chart for Kubernetes deployments  
- Kubernetes manifests (Deployment, Service, Ingress)  
- Observability stack (Grafana dashboards, Promtail, OpenTelemetry)  

## Documentation

- Architecture overview  
- Module and component breakdown  
- API reference  
- Quickstart and examples  
- Ethical use guidelines  
- Development and testing guides  

## Security Notes

- No sensitive or production configuration is included  
- All configuration files are provided as templates  
- Private configuration values are intentionally omitted  

## Open Source

This project is released under an open‑source license and welcomes community contributions, issues, and pull requests.

# 🏷 Release v1.1.0 – 2026-03-19

## **v1.1.0 – Attack Graph Demo, CVE Mapping & Network Simulation Added**

Public demo includes attack path visualization, sample CVE mapping, and network simulation. Core engine and advanced logic remain private.

## Highlights in v1.1.0

- **Attack Path Demo:** Introduced a simplified attack graph demo notebook to showcase potential attack paths in sample networks.  
- **CVE Mapping Integration:** Added CVE data mapping for sample services to demonstrate vulnerability impact.  
- **Network Simulation Module:** Included a network simulation framework for generating sample topologies and assets.  
- **Documentation Updated:** `README.md` and `docs/features.md` updated to reflect new public features.  
- **Examples Provided:** Demo scripts and notebook available under `examples/notebooks` and `examples/scripts`.

> ⚠️ Note: Core engine, CVE matcher, and advanced simulation logic remain private and are not included in the public release.

### Run the Demo (Google Colab)

**Launch the interactive demo here:** [Attack Path Demo Notebook on Google Colab](https://colab.research.google.com/github/secwexen/aapp-mart/blob/main/examples/aapp_mart_attack_path_demo.ipynb)

No installation required — run directly in your browser.

## What's Changed

* Bump actions/checkout from 3 to 6 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/53
* Bump actions/upload-artifact from 4 to 7 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/57
* Bump azure/k8s-bake from 2 to 3 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/56
* Bump docker/login-action from 3 to 4 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/55
* Bump azure/login from 1.4.6 to 2.3.0 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/54
* Bump github/codeql-action from 3 to 4 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/64
* Bump docker/setup-buildx-action from 3 to 4 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/67
* Bump docker/build-push-action from 6 to 7 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/65
* Bump azure/login from 2.3.0 to 3.0.0 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/68
* Bump release-drafter/release-drafter from 6 to 7 by @dependabot[bot] in https://github.com/secwexen/aapp-mart/pull/66


**Full Changelog**: https://github.com/secwexen/aapp-mart/compare/v1.0.1...v1.1.0
