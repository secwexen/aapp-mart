# **Developer Guide**

AAPP‑MART is a modular, multi‑agent red team simulation framework powered by AI‑driven decision models. This guide provides developers with the architectural overview, contribution workflow, coding standards, and extension points required to build new features or improve the framework.

---

## **Project Architecture**

AAPP‑MART is built around three core components that work together to simulate realistic offensive security behavior:

- **AAPP (Attack Path Predictor)** — Analyzes the target environment and predicts potential attack paths based on vulnerabilities, configurations, and system topology.
- **MART (Multi‑Agent Red Team)** — Executes offensive actions using specialized agents representing different stages of the attack lifecycle.
- **Orchestrator** — Coordinates agents, manages execution flow, aggregates results, and generates reports.

Each component is designed as an independent module to ensure extensibility and maintainability.

---

## **Agent Development**

Agents are the core of the simulation engine. Each agent represents a specific offensive capability such as reconnaissance, exploitation, privilege escalation, or lateral movement.

Key requirements for creating a new agent:

- Implement the shared **BaseAgent** interface.
- Define the agent’s **role**, **decision logic**, and **action set**.
- Ensure outputs follow the standardized event format used by the Orchestrator.
- Map agent actions to **MITRE ATT&CK** techniques when applicable.
- Keep the agent modular so it can be enabled or disabled independently.

Agents should be deterministic in structure but flexible in behavior to support dynamic simulation scenarios.

---

## **Simulation Workflow**

The simulation pipeline follows a structured sequence:

1. Load the target profile and environment configuration.
2. Generate attack path predictions using AAPP.
3. Execute MART agents sequentially or in parallel depending on the scenario.
4. Collect and normalize agent outputs.
5. Produce reports, risk scores, and attack timelines.

Developers can modify or extend any stage of this workflow by adding new modules or adjusting orchestration logic.

---

## **Setting Up the Development Environment**

Clone the repository and install dependencies:

```bash
git clone https://github.com/secwexen/aapp-mart
cd aapp-mart
pip install -r requirements.txt
```

Run tests to verify the environment:

```bash
pytest -v
```

Create a feature branch before making changes:

```bash
git checkout -b feature/new-module
```

---

## **Coding Standards**

To maintain consistency across the project:

- Follow **PEP8** style guidelines.
- Use clear and descriptive docstrings for all functions and classes.
- Keep modules small, focused, and reusable.
- Avoid unnecessary dependencies.
- Write tests for all new features.
- Ensure backward compatibility when modifying core components.

All pull requests are automatically checked for formatting, linting, and test coverage.

---

## **Testing Guidelines**

Every new feature must include:

- Unit tests for core logic.
- Agent behavior tests.
- Workflow integration tests when applicable.

Tests are stored under the [tests](tests/) directory and should follow a clear naming convention.

---

## **Extending Reporting**

Developers can add new report formats or extend existing ones. A report module should:

- Define a clear output structure (JSON, HTML, or graphical).
- Integrate with the Orchestrator’s result aggregation system.
- Provide meaningful insights such as attack paths, risk scores, or agent activity timelines.

Reports are located under the [reports](reports/) module.

---

## **Framework Extension Points**

AAPP‑MART is designed to be extensible. Developers can add:

- New agents  
- New attack techniques  
- New simulation scenarios  
- New reporting formats  
- New orchestration strategies  

Each extension should be modular and documented to ensure compatibility with the rest of the framework.

---

## **Security and Ethical Requirements**

- All development and testing must be performed in authorized environments.
- Unauthorized use of the framework against real systems is strictly prohibited.
- Vulnerabilities must be reported according to the project’s **[SECURITY.md](SECURITY.md)** policy.
- Ethical guidelines must be followed at all times.

---

## **Contribution Workflow**

To contribute to AAPP‑MART:

1. Open an issue to discuss the proposed change.
2. Create a feature branch.
3. Implement the change with proper documentation.
4. Add tests for the new functionality.
5. Submit a pull request with a clear description.

Pull requests are reviewed for code quality, security, and architectural consistency.
