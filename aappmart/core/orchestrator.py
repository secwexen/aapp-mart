import logging
from aappmart.core.simulation_engine import SimulationEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class Orchestrator:

    def __init__(self):
        self.engine = SimulationEngine()

    def run(self):
        logging.info("Orchestrator started")
        self.engine.run()
        logging.info("Orchestrator finished")

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run()
