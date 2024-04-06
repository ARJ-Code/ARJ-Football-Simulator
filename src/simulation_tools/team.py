from typing import List
from simulation_tools.player_data import PlayerData

AWAY = 'A'
HOME = 'H'


class Team:
    def __init__(self, name: str, players: List[PlayerData]) -> None:
        self.name = name
        self.players: List[PlayerData] = players
