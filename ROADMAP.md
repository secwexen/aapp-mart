# Roadmap

This document outlines the planned evolution of AAPP-MART based on its existing architecture and core components.

## Short Term (Next Releases)

### Core Engine Improvements

- Improve stability of the core execution engine
- Optimize agent scheduling and task orchestration
- Improve input validation and error handling
- Standardize internal module interfaces
- Improve structured logging and audit records

### Attack Graph & Prediction Engine

- Improve attack graph generation algorithms
- Improve attack path prioritization
- Refine prediction strategies combining:
  - Rule-based analysis
  - Existing machine learning predictors
- Improve attack path search and pruning
- Improve prediction scoring consistency

### Risk & Vulnerability Analysis

- Improve vulnerability data analysis and scoring
- Refine risk aggregation and prioritization
- Improve the assessment of environmental risk factors
- Improve CVSS calculation and vulnerability severity assessment

### CLI Improvements

- Improve command help and documentation
- Improve input validation and error messages
- Improve prediction, risk analysis, simulation, and reporting commands
- Improve CLI execution reliability

## Mid Term

### Attack Graph & Simulation Improvements

- Improve attack graph analysis for larger input datasets
- Improve coordination between prediction and simulation workflows
- Improve simulation result consistency and reproducibility
- Expand test coverage for core engine and simulation components

### Reporting Improvements

- Improve JSON and CSV report consistency
- Improve attack path explanations in reports
- Improve risk summaries and prioritization details
- Improve report generation reliability

## Long Term

### Performance & Scalability

- Optimize attack graph construction and path search for larger datasets
- Improve execution efficiency across core components
- Strengthen storage reliability and handling of execution results

### Security Knowledge & Data Quality

- Improve public vulnerability data retrieval and freshness handling
- Improve CVE data caching and recovery when sources are unavailable
- Improve MITRE ATT&CK mapping coverage
- Improve correlation between vulnerability data, attack techniques, and risk assessments
