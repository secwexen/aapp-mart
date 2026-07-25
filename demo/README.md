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

[*] Initial Entry Point Acquired: 10.10.20.15
[+] [Agent-Recon  ] Reconnaissance       | MITRE: T1595 | Severity: LOW      | Active scanning detected
[+] [Agent-Access ] Phishing             | MITRE: T1566 | Severity: MEDIUM   | Credential harvesting attempt
[+] [Agent-Access ] Initial Access       | MITRE: T1078 | Severity: HIGH     | Valid account abuse
[+] [Agent-Exploit] Privilege Escalation | MITRE: T1068 | Severity: CRITICAL | Kernel privilege escalation simulated
[+] [Agent-Pivot] Lateral Movement     | MITRE: T1021 | Severity: HIGH     | Remote service pivoting to 10.10.20.45
[✓] Simulation Completed Successfully

=== Risk Summary ===

Initial Entry Point Target  : 10.10.20.15
Risk Score                  : 9.1/10 (CRITICAL)
Duration                    : 11.2s
Compromised Assets          : 3
Generated At                : 2026-01-01T05:30:03.123456+00:00

Affected Critical Assets:
[!] FILE-SERVER-01       | IP: 10.10.20.2  | Type: Storage      | Severity: HIGH     | Status: Isolated
[!] DOMAIN-CONTROLLER-01 | IP: 10.10.20.45 | Type: Identity/AD  | Severity: CRITICAL | Status: Compromised
[!] HR-DB-01             | IP: 10.10.20.12 | Type: SQL Database | Severity: CRITICAL | Status: Compromised

[+] Report Exported: /home/user/aapp-mart/logs/attack-path/attack_path_report.json
```

See the [Attack Path Simulation Report](demo/reports/attack_report.json) file.

> [!NOTE]
> This IP/hostname is an example target.