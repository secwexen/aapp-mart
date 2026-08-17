#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=== AAPP-MART Security Engine ===

An AI-Powered Autonomous Attack Path Prediction and Multi-Agent Red Team Simulation Engine designed for enterprise security analysis.

Key Features:
    - Multi-Agent Red Team (Recon, Access, Exploit, Pivot, Collection)
    - Automated Risk Scoring & MITRE ATT&CK Mapping
    - Automated Incident Report Generation (JSON Export)

Usage:
    python aapp_mart.py --target 10.10.20.15
    python aapp_mart.py --help
"""

import argparse
import json
import time
import uuid
import logging
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List

# =========================
# Logging Configuration
# =========================

Path("logs/attack-path").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger("AAPPMART")

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
    started_at: str
    generated_at: str
    duration: float
    duration=round(total_duration, 2)

# =========================
# Risk Label Calculation
# =========================

def calculate_risk_label(score: float) -> str:
    if score >= 9.0:
        return "CRITICAL"
    elif score >= 7.0:
        return "HIGH"
    elif score >= 4.0:
        return "MEDIUM"
    else:
        return "LOW"

# =========================
# Demo Engine
# =========================

class AAPPMARTDemo:

    def __init__(self, target: str):
        self.target = target
        self.hostname = "WORKSTATION-01"
        self.engine_version = "v1.0.0-demo"
        self.simulation_id = str(uuid.uuid4())
        self.started_at = ""

    def run(self) -> SimulationReport:
        start = time.perf_counter()
        self.started_at: str = datetime.now(timezone.utc).isoformat()

        logger.info("\n=== AAPP-MART — AI-Powered Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine ===\n")

        self._log("Simulation Workflow Started")
        self._log(f"Initial Entry Point: {self.target} ({self.hostname})\n")

        attack_chain = [
            AttackStep(
                agent="Agent-Recon",
                phase="Reconnaissance",
                mitre_id="T1595",
                description=f"Active scanning detected on ({self.target})",
                severity="LOW",
                status="SUCCESS",
                remediation="Update firewall rules and IDS/IPS signatures."
            ),
            AttackStep(
                agent="Agent-Access",
                phase="Phishing",
                mitre_id="T1566",
                description="Credential harvesting attempt",
                severity="MEDIUM",
                status="SUCCESS",
                remediation="Enforce Multi-Factor Authentication (MFA) and tighten email filters."
            ),
            AttackStep(
                agent="Agent-Access",
                phase="Initial Access",
                mitre_id="T1078",
                description="Valid account abuse",
                severity="HIGH",
                status="SUCCESS",
                remediation="Audit account privileges and enforce Privileged Access Management (PAM)."
            ),
            AttackStep(
                agent="Agent-Exploit",
                phase="Privilege Escalation",
                mitre_id="T1068",
                description="Kernel privilege escalation simulated",
                severity="CRITICAL",
                status="SUCCESS",
                remediation="Apply the latest OS kernel patches and security updates."
            ),
            AttackStep(
                agent="Agent-Pivot",
                phase="Lateral Movement",
                mitre_id="T1021",
                description="Remote service pivoting to (10.10.20.45)",
                severity="HIGH",
                status="SUCCESS",
                remediation="Implement network micro-segmentation and restrict RDP/SSH access."
            ),
            AttackStep(
                agent="Agent-Collection",
                phase="Collection",
                mitre_id="T1005",
                description="Backup data discovery and collection on (10.10.20.25)",
                severity="CRITICAL",
                status="SUCCESS",
                remediation="Restrict access, enforce least-privilege permissions, and isolate backup infrastructure."
            ),
        ]

        for step in attack_chain:
            self._simulate_step(step)
            time.sleep(0.5)

        risk_score = 9.6
        risk_label = calculate_risk_label(risk_score)

        compromised_assets = [
            CompromisedAsset(
                system="WORKSTATION-01",
                ip=self.target,
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

        short_summary = (
            f"DC (10.10.20.45) breached via "
            f"Workstation ({self.target}) kernel exploit. "
            f"Backup Server (10.10.20.25) compromise."
        )

        executive_summary = (
            f"Simulated attack initiated on ({self.target}) ({self.hostname}) resulted in a {risk_label} risk environment. "
            f"The AI engine successfully pivoted through the network, affecting {len(compromised_assets)} "
            f"critical assets including the Domain Controller and Backup Server."
        )

        total_duration = time.perf_counter() - start

        logger.info("")
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
            started_at=self.started_at,
            generated_at=datetime.now(timezone.utc).isoformat(),
            duration=total_duration
        )

    def _simulate_step(self, step: AttackStep):
        logger.info(
            f"[+] [{step.agent:<16}]"
            f" {step.phase:<20}"
            f" | MITRE: {step.mitre_id:<5}"
            f" | Severity: {step.severity:<8}"
            f" | Status: {step.status:<7}"
            f" | {step.description}"
        )

    def _log(self, message: str, success: bool = False):
        prefix = "[✓]" if success else "[*]"
        logger.info(f"{prefix} {message}")

# =========================
# Report Export
# =========================

class ReportExporter:

    @staticmethod
    def export_json(report: SimulationReport, output_path: str) -> bool:
        try:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            report_data = asdict(report)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)

            logger.info(f"\n[+] Report Exported: {output_path}")
            return True
        except (PermissionError, OSError, TypeError) as e:
            logger.error(f"\n[!] Error exporting report: ({type(e).__name__}) {e}")
            return False

# =========================
# Main
# =========================

def main() -> int:

    parser = argparse.ArgumentParser(
        prog="aapp-mart",
        description=(
            "AAPP-MART — AI-Powered Autonomous Attack Path "
            "Prediction & Multi-Agent Red Team Simulation Engine"
        )
    )

    parser.add_argument(
        "--target",
        required=True,
        help="Target IP address"
    )

    args = parser.parse_args()

    target = args.target.strip()

    if not target:
        parser.error("Target cannot be empty.")

    if target != "10.10.20.15":
        parser.error(
            "This demo only supports target (10.10.20.15)"
        )
    try:
        engine = AAPPMARTDemo(target=target)
        report = engine.run()

    except KeyboardInterrupt:
        logger.warning("\n[!] Simulation Workflow Interrupted by User")
        return 130

    except Exception as e:
        logger.error(f"\n[!] Simulation Workflow Failed: {e}")
        return 1

    compromised = sum(
        asset.status.lower() == "compromised"
        for asset in report.compromised_assets
    )
    isolated = sum(
        asset.status.lower() == "isolated"
        for asset in report.compromised_assets
    )
    blocked = sum(
        asset.status.lower() == "blocked"
        for asset in report.compromised_assets
    )

    logger.info("\n=== COMPREHENSIVE RISK SUMMARY ===\n")

    logger.info(f"[*] Target IP (Initial Entry Point) : {report.target} ({report.hostname})")
    logger.info(f"[*] Risk Score                      : {report.risk_score}/10 ({report.risk_label})")
    logger.info(f"[*] Summary                         : {report.short_summary}")
    logger.info(f"[*] Duration                        : {report.duration:.2f}s")
    logger.info(f"[*] Simulated Step Count            : {len(report.attack_path)} Stages")
    logger.info(f"[*] Affected Assets                 : {len(report.compromised_assets)} Systems ({compromised} Compromised, {isolated} Isolated, {blocked} Blocked)")
    logger.info(f"[*] Started At                      : {report.started_at}") 
    logger.info(f"[*] Generated At                    : {report.generated_at}")

    logger.info("\n--- Affected Critical Assets ---\n")

    for asset in report.compromised_assets:
        logger.info(
            f"[!] "
            f"{asset.system:<20} | "
            f"IP: {asset.ip:<11} | "
            f"Type: {asset.type:<13} | "
            f"Severity: {asset.severity:<8} | "
            f"Status: {asset.status:<11} | "
            f"Detail: {asset.detail}"
        )

    clean_target = report.target.replace(".", "_")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    output_file = (
        f"logs/attack-path/"
        f"attack_path_{clean_target}_{timestamp}.json"
    )

    success = ReportExporter.export_json(report, output_file)

    return 0 if success else 1

if __name__ == "__main__":
    raise SystemExit(main())
