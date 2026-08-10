# Demo

This directory contains runnable demonstration scripts for the AAPP-MART security engine.

## Attack Path Simulation Demo

```bash
python demo/attack_path_simulation.py
```

### Attack Path Simulation Demo Output

```text
=== AAPP-MART — AI-Powered Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine ===

[*] Initial Entry Point Acquired: 10.10.20.15 (WORKSTATION-01)

[+] [Agent-Recon  ] Reconnaissance       | MITRE: T1595 | Severity: LOW      | Status: SUCCESS  | Duration: 1.4s | Active scanning detected
[+] [Agent-Access ] Phishing             | MITRE: T1566 | Severity: MEDIUM   | Status: SUCCESS  | Duration: 2.1s | Credential harvesting attempt
[+] [Agent-Access ] Initial Access       | MITRE: T1078 | Severity: HIGH     | Status: SUCCESS  | Duration: 1.8s | Valid account abuse
[+] [Agent-Exploit] Privilege Escalation | MITRE: T1068 | Severity: CRITICAL | Status: SUCCESS  | Duration: 2.7s | Kernel privilege escalation simulated
[+] [Agent-Pivot  ] Lateral Movement     | MITRE: T1021 | Severity: HIGH     | Status: SUCCESS  | Duration: 3.2s | Remote service pivoting to 10.10.20.45

[✓] Simulation Completed Successfully

=== COMPREHENSIVE RISK SUMMARY ===

[*] Target IP (Initial Entry)  : 10.10.20.15 (WORKSTATION-01)
[*] Risk Score                 : 9.4/10 (CRITICAL)
[*] Summary                    : DC breached via Workstation kernel exploit. High-value target compromise.
[*] Duration                   : 11.2s
[*] Simulated Step Count       : 5 Stages
[*] Affected Assets            : 4 Systems (2 Compromised, 1 Isolated, 1 Blocked)
[*] Generated At               : 2026-01-01T05:30:03.123456+00:00

--- Affected Critical Assets ---

[!] WORKSTATION-01       | IP: 10.10.20.15 | Type: Endpoint     | Severity: HIGH     | Status: Compromised | Detail: Initial Vector
[!] FILE-SERVER-01       | IP: 10.10.20.2  | Type: Storage      | Severity: HIGH     | Status: Isolated    | Detail: Domain Admin
[!] DOMAIN-CONTROLLER-01 | IP: 10.10.20.45 | Type: Identity/AD  | Severity: CRITICAL | Status: Compromised | Detail: Data Exfiltrated
[!] HR-DB-01             | IP: 10.10.20.12 | Type: SQL Database | Severity: CRITICAL | Status: Blocked     | Detail: Attack Blocked

[+] Report Exported: aapp-mart/logs/attack-path/attack_path_10_10_20_15_20260101_053003.json
```

See the [Attack Path Simulation Logs](demo/logs/attack-path/attack_path_simulation_logs.json) json file.

> [!NOTE]
> This IP/hostname is an example target used for demonstration purposes only.

## Executive Summary

AAPP-MART simulated a 5-stage attack chain from WORKSTATION-01 (10.10.20.15) to DOMAIN-CONTROLLER-01 (10.10.20.45) in 11.2 seconds, yielding a Critical Risk Score of 9.4/10. While the Domain Controller was compromised, automated security controls successfully contained the breach by isolating the file server and protecting the HR database.