from typing import List, Tuple, Dict
from simulation_tools.player_data import PlayerData
from .football_agent import Player

AWAY = 'A'
HOME = 'H'


class Team:
    def __init__(self, name: str, players_data: List[PlayerData], players: Dict[int, Player]) -> None:
        self.name = name
        self.players_data: List[PlayerData] = players_data
        self.players: List[Player] = players
        self.line_up: List[Tuple[int, int, int]] = []

    def line_up(self, line_up: List[Tuple[int, int, int]]) -> None:
        self.line_up = line_up
