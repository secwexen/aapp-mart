#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=== AAPP-MART Security Engine ===

An AI-Powered Autonomous Attack Path Prediction and Multi-Agent Red Team Simulation Engine
designed for enterprise security analysis.

Key Features:
    - Multi-Agent Red Team (Recon, Access, Exploit, Pivot, Collection)
    - Automated Risk Scoring & MITRE ATT&CK Mapping
    - Automated Incident Report Generation (JSON Export)

Usage: 
    python demo/attack_path_simulation.py

Requirements:
    - Python >= 3.11
    - Standard Library (json, time, uuid, datetime, pathlib, dataclasses)

Outputs:
    - JSON Execution Logs: aapp-mart/logs/attack-path/attack_path_<target>_<timestamp>.json
"""

import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List

# =========================
# Data Models
# =========================

@dataclass
class AttackStep:
    agent: str
    phase: str
    mitre_id: str
    description: str
    severity: str
    status: str
    duration: float
    remediation: str

@dataclass
class CompromisedAsset:
    system: str
    ip: str
    type: str
    severity: str
    status: str
    detail: str

@dataclass
class SimulationReport:
    simulation_id: str
    target: str
    hostname: str
    status: str
    risk_score: float
    risk_label: str
    engine_version: str
    short_summary: str
    executive_summary: str
    attack_path: List[AttackStep]
    compromised_assets: List[CompromisedAsset]
    terminal_compromised_assets: List[str]
    generated_at: str
    duration: float

# =========================
# Demo Engine
# =========================

class AAPPMartDemo:

    def __init__(self, target: str):
        self.target = target
        self.hostname = "WORKSTATION-01"
        self.engine_version = "v1.0.0-demo"
        self.simulation_id = str(uuid.uuid4())
        self.started_at = datetime.now(timezone.utc).isoformat()

    def run(self) -> SimulationReport:

        print("\n=== AAPP-MART — AI-Powered Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine ===\n")

        self._log(f"Initial Entry Point Acquired: {self.target} ({self.hostname}) \n")
        time.sleep(1)

        attack_chain = [
            AttackStep(
                agent="Agent-Recon",
                phase="Reconnaissance",
                mitre_id="T1595",
                description="Active scanning detected on (10.10.20.15)",
                severity="LOW",
                status="SUCCESS",
                duration=1.4,
                remediation="Update firewall rules and IDS/IPS signatures."
            ),
            AttackStep(
                agent="Agent-Access",
                phase="Phishing",
                mitre_id="T1566",
                description="Credential harvesting attempt",
                severity="MEDIUM",
                status="SUCCESS",
                duration=2.1,
                remediation="Enforce Multi-Factor Authentication (MFA) and tighten email filters."
            ),
            AttackStep(
                agent="Agent-Access",
                phase="Initial Access",
                mitre_id="T1078",
                description="Valid account abuse",
                severity="HIGH",
                status="SUCCESS",
                duration=1.8,
                remediation="Audit account privileges and enforce Privileged Access Management (PAM)."
            ),
            AttackStep(
                agent="Agent-Exploit",
                phase="Privilege Escalation",
                mitre_id="T1068",
                description="Kernel privilege escalation simulated",
                severity="CRITICAL",
                status="SUCCESS",
                duration=2.7,
                remediation="Apply the latest OS kernel patches and security updates."
            ),
            AttackStep(
                agent="Agent-Pivot",
                phase="Lateral Movement",
                mitre_id="T1021",
                description="Remote service pivoting to (10.10.20.45)",
                severity="HIGH",
                status="SUCCESS",
                duration=3.2,
                remediation="Implement network micro-segmentation and restrict RDP/SSH access."
            ),
            AttackStep(
                agent="Agent-Collection",
                phase="Collection",
                mitre_id="T1005",
                description="Backup data discovery and collection on (10.10.20.25)",
                severity="CRITICAL",
                status="SUCCESS",
                duration=2.5,
                remediation="Restrict access, enforce least-privilege permissions, and isolate backup infrastructure."
            ),
        ]

        total_duration = round(sum(step.duration for step in attack_chain), 1)

        for step in attack_chain:
            self._simulate_step(step)

        risk_score = 9.6
        risk_label = "CRITICAL"

        compromised_assets = [
            CompromisedAsset(
                system="WORKSTATION-01",
                ip="10.10.20.15",
                type="Endpoint",
                severity="HIGH",
                status="Compromised",
                detail="Initial Vector"
            ),
            CompromisedAsset(
                system="FILE-SERVER-01",
                ip="10.10.20.2",
                type="Storage",
                severity="HIGH",
                status="Isolated",
                detail="Domain Admin"
            ),
            CompromisedAsset(
                system="DOMAIN-CONTROLLER-01",
                ip="10.10.20.45",
                type="Identity/AD",
                severity="CRITICAL",
                status="Compromised",
                detail="Data Exfiltrated"
            ),
            CompromisedAsset(
                system="BACKUP-SERVER-01",
                ip="10.10.20.25",
                type="Backup Server",
                severity="HIGH",
                status="Compromised",
                detail="Backup Access"
            ),
            CompromisedAsset(
                system="HR-DB-01",
                ip="10.10.20.12",
                type="SQL Database",
                severity="CRITICAL",
                status="Blocked",
                detail="Attack Blocked"
            ),
        ]
        
        terminal_compromised_assets = [
            "WORKSTATION-01       | IP: 10.10.20.15 | Type: Endpoint      | Severity: HIGH     | Status: Compromised | Detail: Initial Vector",
            "FILE-SERVER-01       | IP: 10.10.20.2  | Type: Storage       | Severity: HIGH     | Status: Isolated    | Detail: Domain Admin",
            "DOMAIN-CONTROLLER-01 | IP: 10.10.20.45 | Type: Identity/AD   | Severity: CRITICAL | Status: Compromised | Detail: Data Exfiltrated",
            "BACKUP-SERVER-01     | IP: 10.10.20.25 | Type: Backup Server | Severity: HIGH     | Status: Compromised | Detail: Backup Access",
            "HR-DB-01             | IP: 10.10.20.12 | Type: SQL Database  | Severity: CRITICAL | Status: Blocked     | Detail: Attack Blocked"
        ]

        short_summary = (
            f"DC (10.10.20.45) breached via Workstation (10.10.20.15) kernel exploit. Backup Server (10.10.20.25) compromise."
        )

        executive_summary = (
            f"Simulated attack initiated on ({self.target}) ({self.hostname}) resulted in a {risk_label} risk environment. "
            f"The AI engine successfully pivoted through the network, affecting {len(compromised_assets)} "
            f"critical assets including the Domain Controller and Backup Server."
        )

        print()
        self._log("Simulation Completed Successfully", success=True)

        return SimulationReport(
            simulation_id=self.simulation_id,
            target=self.target,
            hostname=self.hostname,
            status="COMPLETED",
            risk_score=risk_score,
            risk_label=risk_label,
            engine_version=self.engine_version,
            short_summary=short_summary,
            executive_summary=executive_summary,
            attack_path=attack_chain,
            compromised_assets=compromised_assets,
            terminal_compromised_assets=terminal_compromised_assets,
            generated_at=datetime.now(timezone.utc).isoformat(),
            duration=total_duration
        )

    def _simulate_step(self, step: AttackStep):
        print(
            f"[+] [{step.agent:<16}]"
            f" {step.phase:<22}"
            f" | MITRE: {step.mitre_id:<8}"
            f" | Severity: {step.severity:<8}"
            f" | Status: {step.status:<8}"
            f" | Duration: {step.duration:.1f}s"
            f" | {step.description}"
        )
        time.sleep(0.8)

    def _log(self, message: str, success: bool = False):
        prefix = "[✓]" if success else "[*]"
        print(f"{prefix} {message}")

# =========================
# Report Export
# =========================

class ReportExporter:

    @staticmethod
    def export_json(report: SimulationReport, output_path: str):
        try:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            report_data = asdict(report)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=4, ensure_ascii=False)
                
            print(f"\n[+] Report Exported: {output_path}")
            return True
        except (PermissionError, OSError, TypeError) as e:
            print(f"\n[!] Error exporting report: ({type(e).__name__}) {e}")
            return False

# =========================
# Main
# =========================

def main():

    target = "10.10.20.15"

    engine = AAPPMartDemo(target=target)
    report = engine.run()

    print("\n=== COMPREHENSIVE RISK SUMMARY ===\n")

    print(f"[*] Target IP (Initial Entry)  : {report.target} ({report.hostname})")
    print(f"[*] Risk Score                 : {report.risk_score}/10 ({report.risk_label})")
    print(f"[*] Summary                    : {report.short_summary}")
    print(f"[*] Duration                   : {report.duration:.1f}s")
    print(f"[*] Simulated Step Count       : {len(report.attack_path)} Stages")
    print(f"[*] Affected Assets            : {len(report.compromised_assets)} Systems (3 Compromised, 1 Isolated, 1 Blocked)")
    print(f"[*] Generated At               : {report.generated_at}")

    print("\n--- Affected Critical Assets ---\n")
    for asset in report.terminal_compromised_assets:
        print(f"[!] {asset}")

    clean_target = report.target.replace(".", "_")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_file = (
        f"aapp-mart/logs/attack-path/attack_path_{clean_target}_{timestamp}.json"
    )

    ReportExporter.export_json(report, output_file)

if __name__ == "__main__":
    main()
