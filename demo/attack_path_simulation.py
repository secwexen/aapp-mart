#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AAPP-MART Security Engine

An AI-Powered Autonomous Attack Path Prediction and Multi-Agent Red Team Simulation Engine designed for enterprise security analysis.

Use: python demo/attack_path_simulation.py
Version: v1.0.0-demo
"""

import json
import random
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
    duration: float
    remediation: str

@dataclass
class SimulationReport:
    simulation_id: str
    target: str
    risk_score: float
    risk_label: str
    executive_summary: str
    attack_path: List[AttackStep]
    compromised_assets: List[str]
    generated_at: str
    duration: float
    engine_version: str

# =========================
# Demo Engine
# =========================

class AAPPMartDemo:

    def __init__(self, target: str):
        self.target = target
        self.engine_version = "v1.0.0-demo"

    def run(self) -> SimulationReport:

        print("\n=== AAPP-MART — AI-Powered Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine ===\n")

        self._log(f"Initial Entry Point Acquired: {self.target} (WORKSTATION-01)")
        time.sleep(1)

        attack_chain = [
            AttackStep(
                agent="Agent-Recon",
                phase="Reconnaissance",
                mitre_id="T1595",
                description="Active scanning detected",
                severity="LOW",
                duration=1.4,
                remediation="Update firewall rules and IDS/IPS signatures."
            ),
            AttackStep(
                agent="Agent-Access",
                phase="Phishing",
                mitre_id="T1566",
                description="Credential harvesting attempt",
                severity="MEDIUM",
                duration=2.1,
                remediation="Enforce Multi-Factor Authentication (MFA) and tighten email filters."
            ),
            AttackStep(
                agent="Agent-Access",
                phase="Initial Access",
                mitre_id="T1078",
                description="Valid account abuse",
                severity="HIGH",
                duration=1.8,
                remediation="Audit account privileges and enforce Privileged Access Management (PAM)."
            ),
            AttackStep(
                agent="Agent-Exploit",
                phase="Privilege Escalation",
                mitre_id="T1068",
                description="Kernel privilege escalation simulated",
                severity="CRITICAL",
                duration=2.7,
                remediation="Apply the latest OS kernel patches and security updates."
            ),
            AttackStep(
                agent="Agent-Pivot",
                phase="Lateral Movement",
                mitre_id="T1021",
                description="Remote service pivoting to 10.10.20.45",
                severity="HIGH",
                duration=3.2,
                remediation="Implement network micro-segmentation and restrict RDP/SSH access."
            ),
        ]

        total_duration = round(sum(step.duration for step in attack_chain), 1)

        for step in attack_chain:
            self._simulate_step(step)

        risk_score = round(random.uniform(7.8, 9.6), 1)
        risk_label = get_risk_label(risk_score)

        compromised_assets = [
            "WORKSTATION-01       | IP: 10.10.20.15 | Type: Endpoint      | Severity: HIGH     | Status: Compromised | Detail: Initial Vector",
            "FILE-SERVER-01       | IP: 10.10.20.2  | Type: Storage       | Severity: HIGH     | Status: Isolated    | Detail: Domain Admin",
            "DOMAIN-CONTROLLER-01 | IP: 10.10.20.45 | Type: Identity/AD   | Severity: CRITICAL | Status: Compromised | Detail: Data Exfiltrated",
            "HR-DB-01             | IP: 10.10.20.12 | Type: SQL Database  | Severity: CRITICAL | Status: Compromised | Detail: Attack Blocked"
        ]

        executive_summary = (
            f"Simulated attack initiated on {self.target} resulted in a {risk_label} risk environment. "
            f"The AI engine successfully pivoted through the network, compromising {len(compromised_assets)} "
            f"critical assets including the Domain Controller."
        )

        self._log("Simulation Completed Successfully", success=True)

        return SimulationReport(
            simulation_id=str(uuid.uuid4()),
            target=self.target,
            risk_score=risk_score,
            risk_label=risk_label,
            engine_version=self.engine_version,
            executive_summary=executive_summary,
            attack_path=attack_chain,
            compromised_assets=compromised_assets,
            generated_at=datetime.now(timezone.utc).isoformat(),
            duration=total_duration
        )

    def _simulate_step(self, step: AttackStep):
        print(
            f"[+] [{step.agent:<13}]"
            f" {step.phase:<22}"
            f" | MITRE: {step.mitre_id:<8}"
            f" | Severity: {step.severity:<8}"
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
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            report_data = asdict(report)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=4)

            print(f"\n[+] Report Exported: {output_path}")
        except Exception as e:
            print(f"\n[!] Error exporting report: {e}")

# =========================
# Helper Functions
# =========================

def get_risk_label(score: float) -> str:
    if score >= 9.0:
        return "CRITICAL"
    elif score >= 7.0:
        return "HIGH"
    elif score >= 4.0:
        return "MEDIUM"
    else:
        return "LOW"

# =========================
# Main
# =========================

def main():

    target = "10.10.20.15"

    engine = AAPPMartDemo(target=target)

    report = engine.run()

    print("\n=== Comprehensive Risk Summary ===\n")

    print(f"[*] Target IP (Initial Entry)  : {report.target} (WORKSTATION-01)")
    print(f"[*] Risk Score                 : {report.risk_score}/10 ({report.risk_label})")
    print(f"[*] Duration                   : {report.duration:.1f}s")
    print(f"[*] Simulated Step Count       : {len(report.attack_path)} Stages")
    print(f"[*] Compromised Assets         : {len(report.compromised_assets)} Systems (1 Isolated)")
    print(f"[*] Generated At               : {report.generated_at}")

    print("\nAffected Critical Assets:")
    for asset in report.compromised_assets:
        print(f" [!] {asset}")

    clean_target = report.target.replace(".", "_")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_file = (
        f"aapp-mart/logs/attack-path/attack_path_{clean_target}_{timestamp}.json"
    )

    ReportExporter.export_json(report, output_file)

if __name__ == "__main__":
    main()