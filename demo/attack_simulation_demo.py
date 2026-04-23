# AAPP-MART Demo Script
# Minimal CLI demo for attack path simulation

import importlib
import time

def is_package_available():
    return importlib.util.find_spec("aapp_mart") is not None


if is_package_available():
    from aapp_mart.core.orchestrator import AAPP_MART
    DEMO_MODE = False
else:
    DEMO_MODE = True

    class AAPP_MART:
        def __init__(self, target):
            self.target = target

        def run(self):
            print(f"[+] Target: {self.target}")
            time.sleep(1)
            print("[+] Simulating attack path prediction...")
            time.sleep(1)
            print("[+] Running adversarial simulation...")
            time.sleep(1)
            print("[✓] Simulation completed")

        def get_report(self):
            class Report:
                def export(self, format, path):
                    print(f"[+] Report exported → {path} ({format})")
            return Report()


def main():
    print("=== AAPP-MART Demo ===")

    if DEMO_MODE:
        print("[!] Running in DEMO MODE (package not installed)\n")

    target = "192.168.1.10"

    engine = AAPP_MART(target=target)
    engine.run()

    report = engine.get_report()
    report.export(format="json", path="./logs/attack-path/attack_report.json")


if __name__ == "__main__":
    main()
