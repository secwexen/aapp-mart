# Demo

This directory contains runnable demonstration scripts for the AAPP-MART system.

All demos are safe, non-destructive simulations intended for showcasing attack-path prediction, adversarial modeling, and risk analysis concepts.

## Attack Path Simulation Demo

```bash
python demo/advanced_attack_simulation.py
```

### Attack Path Simulation Demo Output

```text
=== AAPP-MART — Attack Path Simulation ===

[*] Target Acquired: 10.10.20.15
[+] Reconnaissance       | MITRE: T1595 | Severity: LOW      | Active scanning detected
[+] Phishing             | MITRE: T1566 | Severity: MEDIUM   | Credential harvesting attempt
[+] Initial Access       | MITRE: T1078 | Severity: HIGH     | Valid account abuse
[+] Lateral Movement     | MITRE: T1021 | Severity: HIGH     | Remote service pivoting
[+] Privilege Escalation | MITRE: T1068 | Severity: CRITICAL | Kernel privilege escalation simulated
[✓] Simulation Completed Successfully

=== Risk Summary ===

Target              : 10.10.20.15
Risk Score          : 9.1/10
Duration            : 11.2s
Compromised Assets  : 3
Generated At        : 2026-01-01T05:30:00.123456+00:00

Affected Critical Assets:
[!] FILE-SERVER-01 (10.10.20.2)
[!] DOMAIN-CONTROLLER-01 (10.10.20.45)
[!] HR-DB-01 (10.10.20.12)

[+] Report Exported: /var/log/aapp-mart/logs/attack-path/attack_path_report.json
```

See the [Attack Path Simulation Report](demo/reports/attack_report.json) file.

> [!NOTE]
> This IP/hostname is an example target.