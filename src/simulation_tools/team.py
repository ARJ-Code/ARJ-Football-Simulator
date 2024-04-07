from typing import List,Tuple
from simulation_tools.player_data import PlayerData

AWAY = 'A'
HOME = 'H'


class Team:
    def __init__(self, name: str, players: List[PlayerData]) -> None:
        self.name = name
        self.players: List[PlayerData] = players
        self.line_up :List[Tuple[int,int,int]]= []

    def line_up(self,line_up:List[Tuple[int,int,int]]) -> None:
        self.line_up = line_up