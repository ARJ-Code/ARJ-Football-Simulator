from abc import ABC, abstractmethod
from .player_data import PlayerData


class FootballAgent(ABC):
    pass


class Player(FootballAgent):
    def __init__(self, data: PlayerData) -> None:
        super().__init__()
        self.stamina: int = 100
        self.data: PlayerData = data


class Manager(FootballAgent):
    pass
