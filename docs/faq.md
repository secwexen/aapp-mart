# AAPP-MART FAQ

This document provides answers to the most frequently asked questions about **AAPP-MART**.

---

## 1. What is AAPP-MART?

AAPP-MART is an **autonomous attack path prediction and multi-agent red team simulation engine**.  
It uses AI to predict potential attack paths and simulates them, helping organizations **identify and mitigate security risks before they are exploited**.

---

## 2. Which platforms are supported?

- **Linux**  
- **macOS**  
- **Windows**  

A cross-platform Python project with no platform-specific dependencies.  
All requirements are listed in [requirements.txt](requirements.txt).

---

## 3. Can I run AAPP-MART safely?

Yes. AAPP-MART is designed to be run **only in authorized and controlled environments**.  
Simulation modes are **non-destructive** and safe for lab environments.  
Running it on production systems **without explicit authorization is strictly prohibited**.

---

## 4. How do I install AAPP-MART?

1. Clone the repository:  
   ```bash
   git clone https://github.com/secwexen/aapp-mart.git
   cd aapp-mart
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Follow the [Installation Guide](https://github.com/secwexen/aapp-mart/blob/main/docs/installation.md) for platform-specific setup.

---

## 5. How do I run a simulation?

**Python API Example:**

```python
from aapp_mart.core.orchestrator import AAPP_MART

engine = AAPP_MART(target="192.168.1.10")
engine.run()
report = engine.get_report()
print(report)
```

**CLI Example:**

```bash
# Run full simulation
$ aapp-mart --target 192.168.1.10 --mode full

# Generate latest report
$ aapp-mart --report latest
```

> ⚠ Always run simulations in **isolated lab environments** with **explicit authorization**.

---

## 6. Can I contribute to AAPP-MART?

Yes. Contributions are welcome!
Refer to the [Contributing Guide](https://github.com/secwexen/aapp-mart/blob/main/CONTRIBUTING.md) for instructions on:

- Submitting bug reports
- Adding new features or modules
- Improving documentation and examples

---

## 7. Where can I find updates and changelogs?

All updates, bug fixes, and version history are tracked in the [CHANGELOG](https://github.com/secwexen/aapp-mart/blob/main/CHANGELOG.md).

---

## 8. Is AAPP-MART free to use?

Yes. AAPP-MART is **open-source** under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
It is free to use for **authorized security testing and research purposes**.

---

## 9. Who maintains AAPP-MART?

The project is maintained by **[secwexen](https://github.com/secwexen)**.  
For issues, questions, or discussions, use [GitHub Issues](https://github.com/secwexen/aapp-mart/issues) or [GitHub Discussions](https://github.com/secwexen/aapp-mart/discussions).

---

## 10. Legal and ethical considerations

AAPP-MART is intended **strictly for authorized security assessments and defensive research**.
Unauthorized use against systems, networks, or applications is **illegal and strictly prohibited**.

Refer to the [Security Policy](https://github.com/secwexen/aapp-mart/blob/main/SECURITY.md) for responsible usage guidelines.
