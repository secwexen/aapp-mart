# AAPP‑MART Documentation

AAPP‑MART (Autonomous Agent & Predictive Processing Framework) is a modular AI-driven framework designed for autonomous agents, predictive task processing, and scalable tool integration.  
This documentation provides a complete overview of the framework’s architecture, components, usage patterns, and installation guidance.

---

## Table of Contents

- [Overview](#overview)  
- [Platform Support](#platform-support)  
- [Getting Started](#getting-started)  
- [Installation](#installation)  
- [Documentation Structure](#documentation-structure)  
- [Architecture Overview](#architecture-overview)  
- [Examples](#examples)  
- [License](#license)  
- [Contributing](#contributing)  
- [Roadmap](#roadmap)  
- [Ethical Use](#ethical-use)

---

## Overview

Modern infrastructures are too complex for traditional security testing.  
AAPP‑MART combines predictive AI with autonomous agent-based simulation to continuously evaluate an environment’s attack surface.  

It consists of two major components:

- **AAPP (AI Attack Path Predictor)** — Predicts likely attack paths by analyzing systems, services, permissions, and vulnerabilities.  
- **MART (Multi-Agent Red Team)** — Executes autonomous red team simulations to emulate real attacker behavior.  

Together, they create a fully automated offensive security engine capable of forecasting attacks end-to-end.

---

## Platform Support

AAPP‑MART is a **cross-platform Python project** and runs on:

- Linux  
- macOS  
- Windows  

No platform-specific dependencies are required.

---

## Getting Started

AAPP‑MART is built on a modular architecture with the following layers:

- **Core** — Orchestrator, pipeline engine, task manager, knowledge graph, simulation engine  
- **Agents** — System, network, forensic, and custom autonomous agents  
- **Predictors** — Machine learning, rule-based, and hybrid predictive models  
- **Modules** — System, network, memory, automation, and controlled testing tools  
- **API** — REST and WebSocket interfaces  
- **CLI** — Command-line interface for interacting with the framework  
- **Utils** — Logging, configuration, validation helpers  
- **Data** — Sample datasets and model files

---

## Installation

> ⚠️ **Note:** AAPP‑MART is currently under active development.  
> Installation instructions will be provided after the first stable release.

For development setup, you can clone the repository and create a Python virtual environment:

```bash
git clone https://github.com/secwexen/aapp-mart
cd aapp-mart

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
````

---

## Documentation Structure

The documentation is organized as follows:

* [Installation](installation.md)
* [Agents](agents.md)
* [Predictors](predictors.md)
* [Modules](modules.md)
* [API Reference](api_reference.md)
* [Architecture Overview](architecture.md)

---

## Architecture Overview

AAPP‑MART consists of three primary layers:

1. **Agent Layer**
   Autonomous units responsible for executing tasks and interacting with modules.

2. **Predictive Processing Layer**
   Models and logic that support decision-making and task prioritization.

3. **Modular Tool Layer**
   System, network, memory, and automation tools used by agents.

All layers are coordinated by the **Orchestrator** and connected via the **Pipeline** system.

---

## Examples

Example usage scenarios are provided in the `examples/` directory:

* `examples/basic_usage.py`
* `examples/custom_agent_example.py`
* `examples/pipeline_example.py`

**Python usage example:**

```python
from aappmart.core.orchestrator import AAPP_MART

engine = AAPP_MART(target="192.168.1.10")
engine.run()

report = engine.get_report()
print(report)
```

> ⚠️ Core implementation is still in progress. Some modules may not be fully functional yet.

---

## License

This project is licensed under **Apache License 2.0**.  
For full details, see the [LICENSE](LICENSE) file in the repository root.  

---

## Contributing

Contributions are welcome.  
Please open an issue before submitting major changes or new features.  
Refer to [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.  

---

## Roadmap

Planned features include:

* Graph-based attack path visualizer
* Cloud environment support
* Agent marketplace
* Reinforcement learning–based decision engine

---

## Ethical Use

AAPP‑MART is designed **for authorized security testing only**.  
Use against systems without explicit permission is illegal.  
All users must comply with applicable laws and organizational policies.  

---

## Disclaimer

AAPP-MART is intended exclusively for ethical, legal, and authorized security research,
penetration testing, and defensive security validation.

The use of this tool against systems, networks, or applications without explicit
authorization from the system owner is strictly prohibited and may be illegal.

The authors and contributors of this project assume no responsibility or liability
for any misuse, damage, or legal consequences resulting from the use of this software.
Users are solely responsible for ensuring compliance with all applicable laws,
regulations, and organizational policies.

---

## Continuous Updates

The AAPP‑MART documentation is continuously updated.  
New modules, agents, and predictive components will be added as development progresses.  

---

## Author

**Secwexen** – Project Author & Maintainer  
**Role:** Project Manager | Lead Developer   
**GitHub:** [github.com/secwexen](https://github.com/secwexen)  
