# Concepts

This document introduces the core concepts behind AAPP-MART (AI-Powered Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine).

## Core Concepts

### 1. Attack Graph

An attack graph represents relationships between assets, security-relevant states, and potential attack transitions.

- **Vertices (V):** Represent assets or security-relevant states.
- **Edges (E):** Represent potential transitions between states.
- **Graph Analysis:** Helps identify relationships and potential paths through the graph.

Graph weights and exploitability metrics may be used when supported by the implemented model and available input data.

### 2. AI-Powered Autonomous Attack Path Prediction (AAPP)

AAPP focuses on analyzing security-related data and attack graph structures to identify and prioritize potential attack paths.

Its intended responsibilities include:

- Graph-based analysis.
- Attack-path identification and prioritization.
- Risk-related scoring.
- Processing relevant vulnerability information.

The prediction methods and accuracy depend on the algorithms and models implemented in the application.

### 3. Multi-Agent Red Team Simulation (MART)

MART represents the multi-agent simulation subsystem of AAPP-MART.

Its intended responsibilities include:

- Coordinating supported simulation workflows.
- Modeling adversarial behavior through implemented agent components.
- Tracking simulation state and outcomes.
- Associating relevant actions with MITRE ATT&CK techniques where supported.

The available agents and their capabilities depend on the current implementation. Simulated actions should not be interpreted as proof that a real system has been compromised.

### 4. Analysis and Simulation Workflows

AAPP-MART is designed to support attack-path analysis, risk assessment, simulation, and reporting workflows.

The exact workflow depends on the available commands and implemented components.

Analysis results and simulation outcomes should be distinguished clearly. A simulated attack path does not, by itself, confirm a vulnerability or demonstrate successful exploitation.

### 5. Risk Scoring

Risk scoring helps prioritize potential security issues and attack paths.

Depending on the implemented model, risk assessment may consider factors such as:

- Vulnerability severity.
- Asset criticality.
- Attack-path characteristics.
- Exploitability-related information.
- Other documented scoring factors.

The calculation method, score range, and interpretation must follow the actual implementation. Risk scores should not be interpreted as precise probabilities unless the model explicitly supports that interpretation.

### 6. Operational Safeguards

AAPP-MART is intended for authorized security assessment, defensive research, and controlled simulation.

Responsible operation includes:

- Testing only within authorized environments.
- Defining and reviewing the intended scope.
- Understanding the behavior of the selected workflow.
- Reviewing execution results and logs where available.
- Avoiding assumptions that simulated outcomes represent real security incidents.

Specific safety controls depend on the implemented functionality and configuration.

### 7. MITRE ATT&CK Mapping

MITRE ATT&CK provides a common reference for describing adversary tactics and techniques.

AAPP-MART can use ATT&CK mapping to associate supported attack information or simulation steps with relevant techniques.

The scope of mapping depends on the techniques and data structures implemented in the application. Mapping does not imply that every ATT&CK technique is supported or simulated.

### 8. Execution and Deployment

AAPP-MART Free is designed to support local execution through its command-line interface.

Other execution options depend on the components included and configured in the installed version.

- **CLI:** Provides access to supported command-line operations.
- **API:** Exposes supported operations where the API implementation is available.
- **Containerization:** Can be used according to the repository's Docker configuration.

Deployment requirements and supported configurations should be documented based on tested implementations.
