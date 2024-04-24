from football_tools.line_up import LineUp
from .manager_strategy import ManagerStrategy
from football_tools.line_up import *
from .simulator_agent import SimulatorAgent


class Manager:
    def __init__(self, strategy: ManagerStrategy, team: str) -> None:
        self.strategy: ManagerStrategy = strategy
        self.team: str = team

    def get_line_up(self, simulator: SimulatorAgent) -> LineUp:
        return self.strategy.get_line_up(self.team, simulator)
