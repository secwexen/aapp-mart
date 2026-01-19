import logging

class Pipeline:

    def __init__(self, steps=5):
        self.steps = steps

    def execute(self, agents):
        logging.info("Pipeline execution started")
        for step in range(self.steps):
            logging.info(f"Pipeline step {step}")
            for agent in agents:
                action = agent.decide({"step": step})
                logging.info(f"{agent.name} action: {action}")
        logging.info("Pipeline execution finished")
