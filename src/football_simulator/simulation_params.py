from typing import Tuple
from football_agent.manager_line_up_strategy import ManagerLineUpStrategy


class SimulationParams:
    def __init__(self, names: Tuple[str, str], managers_line_up: Tuple[ManagerLineUpStrategy,  ManagerLineUpStrategy]) -> None:
        self.names = names
        self.managers_line_up = managers_line_up
