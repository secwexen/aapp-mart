# AAPP-MART Open Source Roadmap

This document outlines the planned evolution of **AAPP-MART** as an open-source research and security simulation platform.  
The roadmap focuses on improving attack path prediction, red-team simulation capabilities, observability, and developer extensibility.

The roadmap is not fixed; priorities may evolve based on community feedback, research outcomes, and contributions.

## Short Term (Next Releases)

### Core Engine Improvements

- Improve stability of the core simulation engine
- Optimize agent scheduling and task orchestration
- Improve configuration validation and error handling
- Standardize internal module interfaces
- Expand logging capabilities and structured logging

### Attack Graph & Prediction Engine

- Improved attack graph generation algorithms
- Attack path prioritization improvements
- Better hybrid prediction strategies combining:
  - rule-based analysis
  - machine learning predictors
- Path pruning and optimization algorithms
- Attack path confidence scoring

### Risk Engine Enhancements

- Expanded vulnerability scoring support
- Improved risk aggregation model
- Environmental risk factors (network exposure, privilege level, etc.)
- Better integration with the Common Vulnerability Scoring System (CVSS)

### CLI Improvements

- Interactive CLI mode
- Improved command help and documentation
- Simulation templates
- Batch scanning and automation support

## Mid Term

### Advanced Attack Simulation

- Additional MART agents:
  - cloud attack agent
  - identity attack agent
  - container attack agent
- Multi-stage attack chain simulation
- Realistic lateral movement modeling
- Privilege escalation path discovery improvements

### AI-Based Prediction Enhancements

- Graph-based machine learning predictors
- Reinforcement learning strategy tuning
- Attack strategy learning from simulation results
- Predictor benchmarking framework

### Visualization & Dashboard

- Interactive attack graph explorer
- Attack path timeline visualization
- Risk heatmap improvements
- Agent activity tracking dashboards
- Attack scenario replay

### Reporting Improvements

- Extended HTML security reports
- Executive risk summaries
- Attack path explanations
- Forensic investigation reports

## Long Term

### Research Capabilities

- Large-scale simulation environments
- Attack campaign modeling
- Autonomous red-team simulations
- AI-driven adversary behavior models
- Threat emulation based on real-world attack patterns

### Security Knowledge Integration

- Integration with public vulnerability databases
- Threat intelligence enrichment
- ATT&CK-style attack technique mapping
- Automated attack technique classification

### Plugin Ecosystem

- Plugin framework for:
  - custom agents
  - prediction engines
  - reporting modules
  - simulation modules

- Community extension marketplace
- Third-party module support

### Distributed Simulation

- Distributed attack simulations across multiple nodes
- Parallel simulation execution
- Large environment modeling
- Cluster-based simulation execution

## Developer Experience

### SDK & Extension Development

- Developer SDK for creating custom agents
- Predictor development framework
- Module testing harness
- Plugin scaffolding tools

### Testing Infrastructure

- Improved end-to-end simulation testing
- Predictor stability tests
- Scenario-based regression tests
- Continuous simulation validation

## Community & Ecosystem

### Documentation Expansion

- Advanced tutorials
- Architecture deep dives
- Research documentation
- Simulation scenario guides

### Community Collaboration

- Community attack modules
- Shared simulation scenarios
- Research collaboration support
- Contributor-driven feature development

## Future Exploration

The following areas are under research and may appear in future versions:

- autonomous attack planning
- adaptive red-team agents
- attack graph neural networks
- cyber range integration
- digital twin security simulations
- AI-driven defense modeling

## Contributing

Community contributions are welcome.

Please see:

- [CONTRIBUTING.md](/CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](/CODE_OF_CONDUCT.md)
- [SECURITY.md](/SECURITY.md)

for guidelines on contributing to the project.

## Disclaimer

AAPP‑MART is intended solely for ethical, legal, and explicitly authorized security research, penetration testing, and defensive security validation.

Using this tool against any system, network, or application without the explicit permission of the system owner is strictly prohibited and may violate local, national, or international laws.
