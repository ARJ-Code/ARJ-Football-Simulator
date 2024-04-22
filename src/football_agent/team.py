from typing import Dict
from .football_agent import Player, Manager

AWAY = 'A'
HOME = 'H'


class TeamAgent:
    def __init__(self, name: str, manager: Manager, players: Dict[int, Player]) -> None:
        self.name = name
        self.manager: Manager = manager
        self.players: Dict[int, Player] = players
