#!/usr/bin/env python3
"""
=== AAPP-MART — AI-Powered Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine Demo ===

Features:
   - Multi-Agent Red Team Attack Simulation
   - MITRE ATT&CK Mapping
   - CVE-Associated Attack Steps
   - Risk Scoring & Severity Classification
   - Attack Path Prediction Confidence Scoring
   - Attack Path Simulation
   - Compromised Asset Analysis
   - Simulation Metrics & Attack Outcome Analytics
   - Security Remediation Recommendations
   - Simulation Workflow Execution
   - JSON Report Generation
   - CSV Report Generation
   - CLI-Based Local Execution

Usage:
    python aapp_mart.py --target 10.10.20.15
    python aapp_mart.py --help

Safety:
    This demo does NOT perform real exploitation, network scanning,
    credential access, lateral movement, persistence, or data collection.
    All activities are simulated using predefined or scenario-based attack paths.
"""

import argparse
import csv
import ipaddress
import json
import re
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
from rich.console import Console

console = Console()

def clear_screen() -> None:
    """Clear the terminal screen."""
    console.clear()


def confirm_exit() -> bool:
    """Ask whether to exit after an interruption."""
    while True:
        try:
            answer = (
                input("\n[!] Simulation interrupted. Exit? [y/N]: ").strip().lower()
            )

            if answer in {"y", "yes"}:
                print("[!] Exiting...")
                return True

            if answer in {"", "N", "no"}:
                print("[*] Resuming simulation...")
                return False

            print("[!] Please enter y or N.")

        except EOFError:
            print("\n[!] Input stream closed. Exiting...")
            return True

# =========================
# Data Models
# =========================

@dataclass
class AttackStep:
    """Represent one step in a simulated attack path."""
    agent: str
    phase: str
    mitre_id: str
    cve_id: Optional[str]
    description: str
    severity: str
    status: str
    confidence: float
    remediation: str


@dataclass
class CompromisedAsset:
    """Represent an asset in the simulation results."""
    system: str
    ip: str
    type: str
    severity: str
    status: str
    detail: str


@dataclass
class SimulationReport:
    """Store simulation metadata, attack steps, and results."""
    schema_version: str
    simulation_id: str
    target: str
    hostname: str
    os: str
    status: str
    risk_score: float
    risk_label: str
    generated_by: str
    engine_version: str
    short_summary: str
    executive_summary: str
    attack_path: List[AttackStep]
    compromised_assets: List[CompromisedAsset]
    remediation_summary: List[str]
    started_at: str
    generated_at: str
    duration: float


# =========================
# MITRE ATT&CK Mapping
# =========================


MITRE_ATTACK = {
    "T1595",
    "T1078",
    "T1068",
    "T1021",
    "T1005"
}

MITRE_PATTERN = re.compile(r"^T\d{4}(\.\d{3})?$")
CVE_PATTERN = re.compile(r"^CVE-\d{4}-\d{4,}$")

VALID_SEVERITIES = {
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL"
}


VALID_ASSET_STATUSES = {
    "COMPROMISED",
    "ISOLATED",
    "BLOCKED"
}


VALID_STATUSES = {
    "SUCCESS",
    "FAILED",
    "BLOCKED"
}


def validate_attack_steps(steps: list[AttackStep]) -> bool:
    """Validate simulation steps and their supported ATT&CK techniques."""
    return all(
        MITRE_PATTERN.fullmatch(step.mitre_id) is not None
        and step.mitre_id in MITRE_ATTACK
        and step.severity.upper() in VALID_SEVERITIES
        and step.status.upper() in VALID_STATUSES
        and 0.0 <= step.confidence <= 1.0
        and (step.cve_id is None or CVE_PATTERN.fullmatch(step.cve_id) is not None)
        for step in steps
    )


def validate_assets(assets: list[CompromisedAsset]) -> bool:
    """Validate asset IP addresses, severity levels, and statuses."""
    try:
        for asset in assets:
            ipaddress.ip_address(asset.ip)

            if asset.severity.upper() not in VALID_SEVERITIES:
                return False

            if asset.status.upper() not in VALID_ASSET_STATUSES:
                return False

        return True

    except (ValueError, AttributeError, TypeError):
        return False


# =========================
# Dynamic Risk Engine
# =========================


class RiskEngine:
    """Calculate a basic risk score for a simulated attack path."""

    W: dict[str, int] = {
        "LOW": 2,
        "MEDIUM": 5,
        "HIGH": 8,
        "CRITICAL": 10,
    }

    @classmethod
    def calculate(
        cls,
        steps: list[AttackStep],
        assets: list[CompromisedAsset],
    ) -> float:
        """Calculate a risk score from attack steps and affected assets."""
        if not steps:
            return 0.0

        step_score = sum(cls.W.get(step.severity.upper(), 0) for step in steps) / len(
            steps
        )

        asset_score = sum(
            cls.W.get(asset.severity.upper(), 0) for asset in assets
        ) / max(len(assets), 1)

        success_ratio = sum(step.status.upper() == "SUCCESS" for step in steps) / len(
            steps
        )

        return round(
            min(step_score * 0.45 + asset_score * 0.40 + success_ratio * 1.5, 10),
            2,
        )


# =========================
# Risk Label Calculation
# =========================


def calculate_risk_label(score: float) -> str:
    """Convert a risk score into a severity label."""
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
    """Run the predefined AAPP-MART demonstration workflow."""

    def __init__(self, target: str):
        """Initialize the demo with a target IP address."""
        self.target = target
        self.hostname = "WORKSTATION-01"
        self.os = "Linux"
        self.generated_by = "AAPP-MART"
        self.engine_version = "v1.0.0-demo"
        self.schema_version = "1.1.0"
        self.simulation_id = str(uuid.uuid4())
        self.started_at = ""

    def run(self) -> SimulationReport:
        """Execute the predefined simulation and return its report."""
        start = time.perf_counter()
        self.started_at: str = datetime.now(timezone.utc).isoformat()

        clear_screen()

        print(
            "\n=== AAPP-MART — AI-Powered Autonomous Attack Path Prediction "
            "& Multi-Agent Red Team Simulation Engine Demo ===\n"
        )

        print("[*] Simulation Workflow Started")
        print(f"[*] Initial Entry Point: {self.target} ({self.hostname}, {self.os})\n")

        attack_chain = [
            AttackStep(
                agent="Agent-Recon",
                phase="Reconnaissance",
                mitre_id="T1595",
                cve_id=None,
                description=f"Active scanning detected on ({self.target})",
                severity="LOW",
                status="SUCCESS",
                confidence=0.91,
                remediation="Update firewall rules and IDS/IPS signatures."
            ),
            AttackStep(
                agent="Agent-Access",
                phase="Initial Access",
                mitre_id="T1078",
                cve_id=None,
                description="Valid account abuse",
                severity="HIGH",
                status="SUCCESS",
                confidence=0.94,
                remediation="Audit account privileges and enforce Privileged Access Management (PAM)."
            ),
            AttackStep(
                agent="Agent-Exploitation",
                phase="Privilege Escalation",
                mitre_id="T1068",
                cve_id="CVE-2024-1086",
                description="Kernel privilege escalation simulated",
                severity="CRITICAL",
                status="SUCCESS",
                confidence=0.97,
                remediation="Apply the latest OS kernel patches and security updates."
            ),
            AttackStep(
                agent="Agent-Pivot",
                phase="Lateral Movement",
                mitre_id="T1021",
                cve_id=None,
                description="Remote service pivoting to (10.10.20.45)",
                severity="HIGH",
                status="SUCCESS",
                confidence=0.89,
                remediation="Implement network micro-segmentation and restrict RDP/SSH access."
            ),
            AttackStep(
                agent="Agent-Collection",
                phase="Collection",
                mitre_id="T1005",
                cve_id=None,
                description="Backup data discovery and collection on (10.10.20.25)",
                severity="CRITICAL",
                status="SUCCESS",
                confidence=0.93,
                remediation="Restrict access, enforce least-privilege permissions, and isolate backup infrastructure."
            ),
        ]

        if not validate_attack_steps(attack_chain):
            raise ValueError("Invalid MITRE ATT&CK technique detected.")

        for step in attack_chain:
            self._simulate_step(step)

            try:
                time.sleep(0.5)
            except KeyboardInterrupt:
                if confirm_exit():
                    raise

                print("[*] Continuing simulation...")

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
                detail="Domain Admin Access"
            ),
            CompromisedAsset(
                system="DOMAIN-CONTROLLER-01",
                ip="10.10.20.45",
                type="Identity/AD",
                severity="CRITICAL",
                status="Compromised",
                detail="Simulated Data Access"
            ),
            CompromisedAsset(
                system="BACKUP-SERVER-01",
                ip="10.10.20.25",
                type="Backup Server",
                severity="HIGH",
                status="Compromised",
                detail="Backup Access"
            ),
        ]

        if not validate_assets(compromised_assets):
            raise ValueError("Invalid compromised asset data.")

        remediation_summary = list(dict.fromkeys(
            step.remediation
            for step in attack_chain
        ))

        risk_score = RiskEngine.calculate(attack_chain, compromised_assets)
        risk_label = calculate_risk_label(risk_score)

        short_summary = (
            f"DC (10.10.20.45) breached via "
            f"Workstation ({self.target}) kernel privilege escalation "
            f"using CVE-2024-1086. "
            f"Backup Server (10.10.20.25) compromise."
        )

        executive_summary = (
            f"Simulated attack initiated on ({self.target}) ({self.hostname}) "
            f"resulted in a {risk_label} risk environment. "
            f"The simulation engine successfully performed simulated "
            f"privilege escalation using CVE-2024-1086, affecting "
            f"{len(compromised_assets)} assets including the Domain Controller "
            f"and Backup Server."
        )

        total_duration = time.perf_counter() - start

        print()
        self._log("Simulation Completed Successfully", success=True)

        return SimulationReport(
            schema_version=self.schema_version,
            simulation_id=self.simulation_id,
            target=self.target,
            hostname=self.hostname,
            os=self.os,
            status="COMPLETED",
            risk_score=risk_score,
            risk_label=risk_label,
            generated_by=self.generated_by,
            engine_version=self.engine_version,
            executive_summary=executive_summary,
            remediation_summary=remediation_summary,
            attack_path=attack_chain,
            short_summary=short_summary,
            compromised_assets=compromised_assets,
            started_at=self.started_at,
            generated_at=datetime.now(timezone.utc).isoformat(),
            duration=round(total_duration, 2)
        )


    def _simulate_step(self, step: AttackStep):
        """Display one simulated attack step."""
        cve_part = f" | CVE: {step.cve_id}" if step.cve_id else ""

        print(
            f"[+] [{step.agent:<18}]"
            f" {step.phase:<20}"
            f" | MITRE: {step.mitre_id:<5}"
            f"{cve_part}"
            f" | Severity: {step.severity:<8}"
            f" | Status: {step.status:<7}"
            f" | {step.description}"
        )


    def _log(self, message: str, success: bool = False):
        """Print a simulation status message."""
        prefix = "[✓]" if success else "[*]"
        print(f"{prefix} {message}")


# =========================
# JSON Report Export
# =========================


class ReportExporter:
    """Export simulation results as JSON."""

    @staticmethod
    def export_json(report: SimulationReport, output_path: str) -> bool:
        """Export the simulation report as JSON."""
        try:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            report_data = asdict(report)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)

            print(f"\n[+] JSON Report Exported: {output_path}")
            return True

        except (PermissionError, OSError, TypeError) as e:
            print(f"\n[!] Error Exporting JSON Report: ({type(e).__name__}) {e}")
            return False


# =========================
# CSV Report Export
# =========================


class CSVReportExporter:
    """Export simulated attack steps as CSV."""

    @staticmethod
    def export_csv(report: SimulationReport, output_path: str) -> bool:
        """Export the simulation attack steps as CSV."""
        try:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)

                writer.writerow([
                    "simulation_id",
                    "agent",
                    "phase",
                    "mitre_id",
                    "cve_id",
                    "severity",
                    "status",
                    "confidence",
                    "description",
                    "remediation"
                ])

                for step in report.attack_path:
                    writer.writerow([
                        report.simulation_id,
                        step.agent,
                        step.phase,
                        step.mitre_id,
                        step.cve_id or "",
                        step.severity,
                        step.status,
                        step.confidence,
                        step.description,
                        step.remediation
                    ])

            print(f"[+] CSV Report Exported: {output_path}")
            return True

        except (PermissionError, OSError, csv.Error) as e:
            print(f"[!] Error Exporting CSV Report: ({type(e).__name__}) {e}")
            return False

# =========================
# Main
# =========================


def main() -> int:
    """Parse CLI arguments, run the demo, and export the selected report."""

    parser = argparse.ArgumentParser(
        prog="aapp-mart",
        description=(
            "AAPP-MART — AI-Powered Autonomous Attack Path Prediction & Multi-Agent Red Team Simulation Engine Demo"
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

    try:
        ipaddress.ip_address(target)
    except ValueError:
        parser.error("Target must be a valid IP address.")

    if target != "10.10.20.15":
        parser.error(
            "This demo only supports target (10.10.20.15)"
        )
    try:
        engine = AAPPMARTDemo(target=target)
        report = engine.run()

    except KeyboardInterrupt:
        return 130

    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(f"\n[!] Simulation workflow failed: {exc}")
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

    print("\n=== COMPREHENSIVE RISK SUMMARY ===\n")

    print(f"[*] Target IP (Initial Entry Point) : {report.target} ({report.hostname})")
    print(f"[*] Risk Score                      : {report.risk_score}/10 ({report.risk_label})")
    print(f"[*] Summary                         : {report.short_summary}")
    print(f"[*] Duration                        : {report.duration:.2f}s")
    print(f"[*] Simulated Step Count            : {len(report.attack_path)} Stages")
    print(
        f"[*] Affected Assets                 : "
        f"{len(report.compromised_assets)} Systems "
        f"({compromised} Compromised, "
        f"{isolated} Isolated, {blocked} Blocked)"
    )
    print(f"[*] Started At                      : {report.started_at}")
    print(f"[*] Generated At                    : {report.generated_at}")

    print("\n--- Affected Critical Assets ---\n")

    for asset in report.compromised_assets:
        print(
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

    json_output_file = (
        f"logs/"
        f"attack_path_{clean_target}_{timestamp}.json"
    )

    csv_output_file = (
        f"logs/"
        f"attack_path_{clean_target}_{timestamp}.csv"
    )

    print("\n=== REPORT EXPORT FORMAT ===\n")

    print("[1] JSON Report")
    print("[2] CSV Report")
    print("[3] JSON + CSV Report")

    while True:
        try:
            choice = input("\nSelect Report Format [1-3]: ").strip()

            if choice in {"1", "2", "3"}:
                break

            print("[!] Invalid Selection. Please Choose 1, 2, and 3.")

        except KeyboardInterrupt:
            if confirm_exit():
                return 130

        except EOFError:
            print("\n[!] Input Stream Closed.")
            return 130

    json_success = True
    csv_success = True

    if choice in {"1", "3"}:
        json_success = ReportExporter.export_json(report, json_output_file)

    if choice in {"2", "3"}:
        csv_success = CSVReportExporter.export_csv(report, csv_output_file)

    return 0 if json_success and csv_success else 1


if __name__ == "__main__":
    raise SystemExit(main())
