# Demo

This directory contains runnable demonstration scripts for the AAPP-MART system.

## Attack Path Simulation Demo

```bash
python demo/attack_path_simulation.py
```

### Attack Path Simulation Demo Output

```text
=== AAPP-MART — AI-Powered Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine ===

[*] Initial Entry Point Acquired: 10.10.20.15 (WORKSTATION-01)
[+] [Agent-Recon  ] Reconnaissance       | MITRE: T1595 | Severity: LOW      | Duration: 1.4s | Active scanning detected
[+] [Agent-Access ] Phishing             | MITRE: T1566 | Severity: MEDIUM   | Duration: 2.1s | Credential harvesting attempt
[+] [Agent-Access ] Initial Access       | MITRE: T1078 | Severity: HIGH     | Duration: 1.8s | Valid account abuse
[+] [Agent-Exploit] Privilege Escalation | MITRE: T1068 | Severity: CRITICAL | Duration: 2.7s | Kernel privilege escalation simulated
[+] [Agent-Pivot  ] Lateral Movement     | MITRE: T1021 | Severity: HIGH     | Duration: 3.2s | Remote service pivoting to 10.10.20.45
[✓] Simulation Completed Successfully

=== Comprehensive Risk Summary ===

[*] Target IP (Initial Entry)   : 10.10.20.15 (WORKSTATION-01)
[*] Risk Score                  : 9.1/10 (CRITICAL)
[*] Duration                    : 11.2s
[*] Simulated Step Count        : 5 Stages
[*] Compromised Assets          : 4 Systems (1 Isolated)
[*] Generated At                : 2026-01-01T05:30:03.123456+00:00

Affected Critical Assets:
[!] WORKSTATION-01       | IP: 10.10.20.15 | Type: Endpoint     | Severity: HIGH     | Status: Compromised | Detail: Initial Vector
[!] FILE-SERVER-01       | IP: 10.10.20.2  | Type: Storage      | Severity: HIGH     | Status: Isolated    | Detail: Domain Admin
[!] DOMAIN-CONTROLLER-01 | IP: 10.10.20.45 | Type: Identity/AD  | Severity: CRITICAL | Status: Compromised | Detail: Data Exfiltrated
[!] HR-DB-01             | IP: 10.10.20.12 | Type: SQL Database | Severity: CRITICAL | Status: Compromised | Detail: Attack Blocked

[+] Report Exported: /home/user/aapp-mart/logs/attack-path/attack_path_10_10_20_15_20260101_053003.json
```

See the [Attack Path Simulation Logs](demo/logs/attack-path/attack_path_simulation_logs.json) json file.

> [!NOTE]
> This IP/hostname is an example target used for demonstration purposes only.
