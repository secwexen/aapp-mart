# AAPP-MART Demo Script
# This script demonstrates a minimal example of running an attack path simulation.

from aapp_mart.core.orchestrator import AAPP_MART

engine = AAPP_MART(target="192.168.1.10")
engine.run()

report = engine.get_report()
report.export(format="json", path="./logs/attack-path/attack_report.json")
