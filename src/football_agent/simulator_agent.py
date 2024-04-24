from football_tools.game import Game
from abc import ABC, abstractmethod


class SimulatorAgent(ABC):
    def __init__(self, game: Game):
        self.game = game

    @abstractmethod
    def simulate(self):
        pass

    @abstractmethod
    def reset(self):
        pass
