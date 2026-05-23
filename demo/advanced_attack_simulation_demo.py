import json
import random
import time
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


@dataclass
class SimulationReport:
    target: str
    risk_score: float
    attack_path: List[AttackStep]
    compromised_assets: List[str]
    generated_at: str


# =========================
# Demo Engine
# =========================

class AAPPMartDemo:

    def __init__(self, target: str):
        self.target = target

    def run(self) -> SimulationReport:

        print("\n=== AAPP-MART Autonomous Simulation ===\n")

        self._log(f"Target acquired: {self.target}")
        time.sleep(1)

        attack_chain = [
            AttackStep(
                phase="Reconnaissance",
                mitre_id="T1595",
                description="Active scanning detected",
                severity="LOW"
            ),
            AttackStep(
                phase="Phishing",
                mitre_id="T1566",
                description="Credential harvesting attempt",
                severity="MEDIUM"
            ),
            AttackStep(
                phase="Initial Access",
                mitre_id="T1078",
                description="Valid account abuse",
                severity="HIGH"
            ),
            AttackStep(
                phase="Lateral Movement",
                mitre_id="T1021",
                description="Remote service pivoting",
                severity="HIGH"
            ),
            AttackStep(
                phase="Privilege Escalation",
                mitre_id="T1068",
                description="Kernel privilege escalation simulated",
                severity="CRITICAL"
            ),
        ]

        for step in attack_chain:
            self._simulate_step(step)

        risk_score = round(random.uniform(7.8, 9.6), 1)

        compromised_assets = [
            "FILE-SERVER-01",
            "DOMAIN-CONTROLLER",
            "HR-DB"
        ]

        self._log("Simulation completed successfully", success=True)

        return SimulationReport(
            target=self.target,
            risk_score=risk_score,
            attack_path=attack_chain,
            compromised_assets=compromised_assets,
            generated_at=time.strftime("%Y-%m-%d %H:%M:%S")
        )

    def _simulate_step(self, step: AttackStep):
        print(
            f"[+] {step.phase:<22}"
            f" | MITRE: {step.mitre_id:<8}"
            f" | Severity: {step.severity:<8}"
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

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        report_data = asdict(report)

        # dataclass nested conversion
        report_data["attack_path"] = [
            asdict(step)
            for step in report.attack_path
        ]

        with open(output_path, "w") as f:
            json.dump(report_data, f, indent=4)

        print(f"\n[+] Report exported → {output_path}")


# =========================
# Main
# =========================

def main():

    target = "192.168.1.10"

    engine = AAPPMartDemo(target=target)

    report = engine.run()

    print("\n=== Risk Summary ===\n")

    print(f"Target              : {report.target}")
    print(f"Risk Score          : {report.risk_score}/10")
    print(f"Compromised Assets  : {len(report.compromised_assets)}")

    print("\nCritical Assets:")
    for asset in report.compromised_assets:
        print(f" - {asset}")

    output_file = (
        f"./logs/attack-path/"
        f"attack_report_{target}.json"
    )

    ReportExporter.export_json(report, output_file)


if __name__ == "__main__":
    main()
