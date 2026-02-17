# Deployment Model

AAPP-MART supports the following deployment patterns:

## Standalone CLI

- Local execution
- Scriptable automation
- CI/CD integration

## REST API Mode (Planned)

- Programmatic integration
- External orchestration support

## Offline / Air-Gapped Operation

- No external service dependency required
- Suitable for isolated environments

## Containerization (Planned)

- Docker-based deployment
- Isolated execution boundary

## System Requirements

- Python 3.11
- Standard system memory sufficient for graph size
- No platform-specific dependencies

---

# Directory Structure

```
aapp-mart
├── src/
│   └── aapp_mart/
│       ├── aapp/                  # Attack Path Predictor
│       ├── agents/                # Autonomous attacker agents
│       ├── api/                   # Optional REST API
│       ├── common/                # Common, reusable base classes or constants
│       ├── cli/                   # Command-line interface
│       ├── core/                  # Autonomous simulation brain
│       ├── data/                  # Sample data & signatures
│       ├── mart/                  # Multi-Agent Red Team
│       ├── modules/               # Pluggable engine modules
│       ├── predictors/            # Prediction logic & models
│       ├── reports/               # Generated reports
│       └── main.py                # AAPP-MART entry point
│
├── assets/
├── docs/
├── examples/
├── internal_api/
├── ml_training/
├── tests/
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── DISCLAIMER.md
├── LICENSE
├── Makefile
├── README.md
├── SECURITY.md
├── pyproject.toml
├── requirements-dev.txt
├── requirements.txt
└── setup.py
```
