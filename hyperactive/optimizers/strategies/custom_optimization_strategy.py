# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

from .optimization_strategy import BaseOptimizationStrategy


class CustomOptimizationStrategy(BaseOptimizationStrategy):
    def __init__(self):
        super().__init__()

        self.optimizer_setup_l = []
        self.duration_sum = 0

    def add_optimizer(self, optimizer, duration=1):
        self.duration_sum += duration
        optimizer_setup = {
            "optimizer": optimizer,
            "duration": duration,
        }
        self.optimizer_setup_l.append(optimizer_setup)
