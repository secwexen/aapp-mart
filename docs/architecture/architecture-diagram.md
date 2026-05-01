# System Architecture Diagram

The following diagram illustrates the high-level architecture of the project:

```mermaid
flowchart TD

    Client[Client CLI Dashboard] --> API[API Layer FastAPI]

    API --> Orchestrator[Orchestration and Decision Engine]

    Orchestrator <--> Graph[Attack Graph and Knowledge Graph]

    Orchestrator --> AAPP[AAPP Engine Prediction and Path Scoring]
    AAPP <--> Graph

    Orchestrator --> MART[MART Engine Simulation Controller]
    MART --> Agents[Autonomous Agent System]
    MART <--> Graph

    Agents --> Recon[Recon Agent]
    Agents --> Exploit[Exploit Agent]
    Agents --> Lateral[Lateral Movement Agent]
    Agents --> PrivEsc[Privilege Escalation Agent]
    Agents --> Persistence[Persistence Agent]

    Agents <--> Graph

    Graph --> Risk[Risk Analysis and Scoring Engine]
    Risk --> Reports[Report Generator]

    Reports --> Export[Export JSON PDF SIEM]
    Reports --> Visualization[Visualization Dashboard]

    External[Threat Intel CVE Assets Configs] --> Graph

    Graph --> GraphDB[(Graph Database)]
    Orchestrator <--> DB[(Relational Database)]
    Reports --> Storage[(Artifact Storage)]

    Orchestrator --> Obs[Observability Layer]
    AAPP --> Obs
    MART --> Obs
    API --> Obs

    Obs --> Logs[Logging]
    Obs --> Metrics[Metrics]
    Obs --> Tracing[Tracing]
```
