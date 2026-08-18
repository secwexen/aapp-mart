# Demo

This directory contains runnable demonstration scripts for the AAPP-MART cybersecurity engine.

### Attack Path Simulation

This section demonstrates a runnable attack-path simulation for the AAPP-MART cybersecurity engine.

### Usage

```bash
python aapp_mart.py --target 10.10.20.15
```

### Output

```text
=== AAPP-MART — AI-Powered Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine ===

[*] Simulation Workflow Started
[*] Initial Entry Point: 10.10.20.15 (WORKSTATION-01, Linux) 

[+] [Agent-Recon       ] Reconnaissance       | MITRE: T1595 | Severity: LOW      | Status: SUCCESS | Active scanning detected on (10.10.20.15)
[+] [Agent-Access      ] Initial Access       | MITRE: T1078 | Severity: HIGH     | Status: SUCCESS | Valid account abuse
[+] [Agent-Exploitation] Privilege Escalation | MITRE: T1068 | CVE: CVE-2024-1086 | Severity: CRITICAL | Status: SUCCESS | Kernel privilege escalation simulated
[+] [Agent-Pivot       ] Lateral Movement     | MITRE: T1021 | Severity: HIGH     | Status: SUCCESS | Remote service pivoting to (10.10.20.45)
[+] [Agent-Collection  ] Collection           | MITRE: T1005 | Severity: CRITICAL | Status: SUCCESS | Backup data discovery and collection on (10.10.20.25)

[✓] Simulation Completed Successfully

=== COMPREHENSIVE RISK SUMMARY ===

[*] Target IP (Initial Entry Point) : 10.10.20.15 (WORKSTATION-01)
[*] Risk Score                      : 9.6/10 (CRITICAL)
[*] Summary                         : DC (10.10.20.45) breached via Workstation (10.10.20.15) kernel privilege escalation using CVE-2024-1086. Backup Server (10.10.20.25) compromise.
[*] Duration                        : 1.00s
[*] Simulated Step Count            : 5 Stages
[*] Affected Assets                 : 4 Systems (3 Compromised, 1 Isolated, 0 Blocked)
[*] Started At                      : 2026-01-01T01:01:01.123456+00:00
[*] Generated At                    : 2026-01-01T01:01:01.123456+00:00

--- Affected Critical Assets ---

[!] WORKSTATION-01       | IP: 10.10.20.15 | Type: Endpoint      | Severity: HIGH     | Status: Compromised | Detail: Initial Vector
[!] FILE-SERVER-01       | IP: 10.10.20.2  | Type: Storage       | Severity: HIGH     | Status: Isolated    | Detail: Domain Admin Access
[!] DOMAIN-CONTROLLER-01 | IP: 10.10.20.45 | Type: Identity/AD   | Severity: CRITICAL | Status: Compromised | Detail: Data Exfiltrated
[!] BACKUP-SERVER-01     | IP: 10.10.20.25 | Type: Backup Server | Severity: HIGH     | Status: Compromised | Detail: Backup Access

[+] Report Exported: logs/attack-path/attack_path_10_10_20_15_20260101_010101.json
```

> [!NOTE]
> This IP/hostname is an example target used for demonstration purposes only.
