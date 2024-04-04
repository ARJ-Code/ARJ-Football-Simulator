from abc import ABC, abstractmethod

from simulation_tools.game import Game
from .player_data import PlayerData


class FootballAgent(ABC):
    pass


class Player(FootballAgent):
    def __init__(self, stamina: int) -> None:
        super().__init__()
        self.stamina = stamina

    def get_perceptions(self, game: Game):
        pass


class Manager(FootballAgent):
    pass
