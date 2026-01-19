import logging
from core.pipeline import Pipeline
from agents.agent_registry import AgentRegistry

class SimulationEngine:

    def __init__(self):
        self.agents = AgentRegistry.get_all_agents()
        self.pipeline = Pipeline(steps=5)

    def run(self):
        logging.info("Simulation Engine started")
        self.pipeline.execute(self.agents)
        logging.info("Simulation Engine finished")
