from typing import List
from football_tools.line_up import LineUp
from football_tools.player_data import PlayerData
from .player_agent import Player
from .manager_strategy import ManagerStrategy


class Manager:
    def __init__(self, strategy: ManagerStrategy, team: str, players: List[PlayerData]) -> None:
        self.strategy: ManagerStrategy = strategy
        self.team: str = team
        self.players: List[Player] = players

    def get_line_up(self) -> LineUp:
        return self.strategy.get_line_up(self.players, self.team)
