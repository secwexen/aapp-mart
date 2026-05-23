# Demo

This directory contains runnable demonstration scripts and notebooks for the AAPP-MART platform.

All demos are **safe, non-destructive simulations** intended for showcasing attack-path prediction, adversarial modeling, and risk analysis concepts.

> [!NOTE]
> DEMO: This IP/hostname is an example target. You will write the actual target IP/hostname yourself in the main project.

## How to Run

From the project root directory, execute the following commands

## Advanced Attack Simulation Demo

```bash
python demo/advanced_attack_simulation_demo.py
```

### Output Example

```text
=== AAPP-MART Autonomous Simulation ===

[*] Target acquired: 192.168.1.10

[+] Reconnaissance       | MITRE: T1595 | Severity: LOW      | Active scanning detected
[+] Phishing             | MITRE: T1566 | Severity: MEDIUM   | Credential harvesting attempt
[+] Initial Access       | MITRE: T1078 | Severity: HIGH     | Valid account abuse
[+] Lateral Movement     | MITRE: T1021 | Severity: HIGH     | Remote service pivoting
[+] Privilege Escalation | MITRE: T1068 | Severity: CRITICAL | Kernel privilege escalation simulated

[✓] Simulation completed successfully

=== Risk Summary ===

Target              : 192.168.1.10
Risk Score          : 8.9/10
Compromised Assets  : 3

Critical Assets:
- FILE-SERVER-01
- DOMAIN-CONTROLLER
- HR-DB

[+] Report exported → ./logs/attack-path/attack_report_192.168.1.10.json
```

## Attack Simulation Demo

```bash
python demo/attack_simulation_demo.py
```

### Output Example

```text
=== AAPP-MART Demo ===
[!] Running in DEMO MODE (package not installed)
[+] Target: 192.168.1.10
[+] Simulating attack path prediction...
[+] Running adversarial simulation...
[✓] Simulation completed
[+] Report exported → ./logs/attack-path/attack_report_192.168.1.10.json
```

## Run on Google Colab

Launch the interactive demo:

[Attack Path Demo Notebook](https://colab.research.google.com/github/secwexen/aapp-mart/blob/main/demo/attack_path_demo.ipynb)

### Colab Output

```
Environment is ready for AAPP-MART demo.
Simulating attack path prediction for target: 192.168.1.10
Report exported in json format to ./logs/attack-path/attack_report_192.168.1.10.json
```
