# Demo

This directory contains runnable demonstration scripts for the AAPP-MART system.

All demos are safe, non-destructive simulations intended for showcasing attack-path prediction, adversarial modeling, and risk analysis concepts.

## Advanced Attack Simulation Demo

```bash
python demo/advanced_attack_simulation.py
```

### Advanced Attack Simulation Demo Output

```text
=== AAPP-MART Autonomous Simulation ===

[*] Target acquired: 10.10.20.15
[+] Reconnaissance       | MITRE: T1595 | Severity: LOW      | Active scanning detected
[+] Phishing             | MITRE: T1566 | Severity: MEDIUM   | Credential harvesting attempt
[+] Initial Access       | MITRE: T1078 | Severity: HIGH     | Valid account abuse
[+] Lateral Movement     | MITRE: T1021 | Severity: HIGH     | Remote service pivoting
[+] Privilege Escalation | MITRE: T1068 | Severity: CRITICAL | Kernel privilege escalation simulated
[✓] Simulation completed successfully

=== Risk Summary ===

Target              : 10.10.20.15
Risk Score          : 8.9/10
Duration            : 11.2s
Compromised Assets  : 3
Generated At        : 2026-01-01 09:58:45

Critical Assets:
- FILE-SERVER-01
- DOMAIN-CONTROLLER
- HR-DB

[+] Report exported → aapp-mart/logs/attack-path/attack_report.json
```

See the [Attack Simulation Report](demo/reports/attack_report.json) file.

> [!NOTE]
> This IP/hostname is an example target. You will write the actual target IP/hostname yourself in the main project.
