# Roadmap

This document describes planned improvements to the AAPP-MART Community Edition, focusing on the reliability, transparency, and usability of its existing simulation, risk assessment, and reporting capabilities.

## Short Term (Next Releases)

### Core Engine Improvements

- Improve simulation execution stability
- Strengthen input validation and error handling
- Improve consistency of simulation status reporting
- Expand automated tests for core components
- Improve structured logging and diagnostic messages

### Simulation Workflow Improvements

- Improve predefined attack scenario management
- Make simulated attack steps and outcomes easier to understand
- Improve simulation reproducibility
- Validate scenario data before execution
- Clearly distinguish simulated outcomes from verified security findings

### Risk Assessment

- Document risk scoring weights and calculation methods
- Improve consistency between risk scores and severity labels
- Improve risk summaries and remediation recommendations
- Add tests for risk calculation and classification

### CLI Improvements

- Improve command help and usage documentation
- Improve input validation and error messages
- Improve interruption handling and execution reliability
- Clarify supported targets and simulation limitations

## Mid Term

### Attack-Path Representation

- Improve the representation of relationships between modeled assets
- Provide clearer explanations of predefined attack sequences
- Improve traceability between attack steps, affected assets, and reported risks
- Evaluate graph-based analysis capabilities as a future development direction

### Reporting Improvements

- Improve JSON and CSV report consistency
- Strengthen report schema validation
- Improve report metadata and traceability
- Improve export error handling
- Expand automated tests for report generation

### Documentation and Testing

- Expand installation and usage examples
- Document supported MITRE ATT&CK technique identifiers
- Clarify the role of CVE identifiers in simulated scenarios
- Improve testing and contribution documentation

## Long Term

### Extensibility and Reliability

- Improve the modularity of simulation components
- Establish consistent interfaces for future extensions
- Improve performance and reliability for larger scenarios
- Evaluate additional analysis methods based on implementation and testing results

### Security Data Quality

- Improve validation of vulnerability-related metadata
- Improve consistency of MITRE ATT&CK mappings
- Evaluate options for integrating public vulnerability data
- Document data-source limitations and handling of unavailable information

### Future Analysis Capabilities

- Evaluate graph-based attack-path analysis
- Assess the feasibility of machine-learning-assisted prediction
- Explore more advanced risk prioritization methods
- Validate new capabilities through documented tests and reproducible experiments

This roadmap describes planned development, not a guarantee that every capability is available in the current release. Priorities may change as the project evolves.
