import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List

# =========================
# Data Models
# =========================

@dataclass
class AttackStep:
    phase: str
    mitre_id: str
    description: str
    severity: str
    duration: float

@dataclass
class SimulationReport:
    target: str
    risk_score: float
    attack_path: List[AttackStep]
    compromised_assets: List[str]
    generated_at: str
    duration: float

# =========================
# Demo Engine
# =========================

class AAPPMartDemo:

    def __init__(self, target: str):
        self.target = target

    def run(self) -> SimulationReport:

        print("\n=== AAPP-MART — Attack Path Simulation ===\n")

        self._log(f"Target Acquired: {self.target}")
        time.sleep(1)

        attack_chain = [
            AttackStep(
                phase="Reconnaissance",
                mitre_id="T1595",
                description="Active scanning detected",
                severity="LOW",
                duration=1.4
            ),
            AttackStep(
                phase="Phishing",
                mitre_id="T1566",
                description="Credential harvesting attempt",
                severity="MEDIUM",
                duration=2.1
            ),
            AttackStep(
                phase="Initial Access",
                mitre_id="T1078",
                description="Valid account abuse",
                severity="HIGH",
                duration=1.8
            ),
            AttackStep(
                phase="Lateral Movement",
                mitre_id="T1021",
                description="Remote service pivoting",
                severity="HIGH",
                duration=3.2
            ),
            AttackStep(
                phase="Privilege Escalation",
                mitre_id="T1068",
                description="Kernel privilege escalation simulated",
                severity="CRITICAL",
                duration=2.7
            ),
        ]

        total_duration = sum(step.duration for step in attack_chain)

        for step in attack_chain:
            self._simulate_step(step)

        risk_score = round(random.uniform(7.8, 9.6), 1)

        compromised_assets = [
            "FILE-SERVER-01       | IP: 10.10.20.2  | Type: Storage       | Severity: HIGH     | Status: Isolated",
            "DOMAIN-CONTROLLER-01 | IP: 10.10.20.45 | Type: Identity/AD   | Severity: CRITICAL | Status: Compromised",
            "HR-DB-01             | IP: 10.10.20.12 | Type: SQL Database  | Severity: CRITICAL | Status: Compromised"
        ]

        self._log("Simulation Completed Successfully", success=True)

        return SimulationReport(
            target=self.target,
            risk_score=risk_score,
            attack_path=attack_chain,
            compromised_assets=compromised_assets,
            generated_at=datetime.now(timezone.utc).isoformat(),
            duration=total_duration
        )

    def _simulate_step(self, step: AttackStep):
        print(
            f"[+] {step.phase:<22}"
            f" | MITRE: {step.mitre_id:<8}"
            f" | Severity: {step.severity:<8}"
            f" | Duration: {step.duration:.1f}s"
            f" | Description: {step.description}"
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

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        report_data = asdict(report)

        # dataclass nested conversion
        report_data["attack_path"] = [
            asdict(step)
            for step in report.attack_path
        ]

        with open(output_path, "w") as f:
            json.dump(report_data, f, indent=4)

        print(f"\n[+] Report Exported: {output_path}")

# =========================
# Helper Functions
# =========================

def get_risk_label(score: float) -> str:
    if score >= 9.0:
        return "(CRITICAL)"
    elif score >= 7.0:
        return "(HIGH)"
    elif score >= 4.0:
        return "(MEDIUM)"
    else:
        return "(LOW)"

# =========================
# Main
# =========================

def main():

    target = "10.10.20.15"

    engine = AAPPMartDemo(target=target)

    report = engine.run()

    print("\n=== Risk Summary ===\n")
    
    print(f"Target             : {report.target}")
    print(f"Risk Score         : {report.risk_score}/10")
    print(f"Duration           : {report.duration:.1f}s")
    print(f"Compromised Assets : {len(report.compromised_assets)}")
    print(f"Generated At       : {report.generated_at}")

    print("\n[!] Affected Critical Assets (3):")
    for asset in report.compromised_assets:
        print(f" [!] {asset}")

    output_file = (
        f"./aapp-mart/logs/attack-path/"
        f"attack_path_report.json"
    )

    ReportExporter.export_json(report, output_file)

if __name__ == "__main__":
    main()
