from typing import List,  Dict
from .football_agent import Player

AWAY = 'A'
HOME = 'H'

class TeamAgent:
    def __init__(self, name: str, players: Dict[int, Player]) -> None:
        self.name = name
        self.players: List[Player] = players
