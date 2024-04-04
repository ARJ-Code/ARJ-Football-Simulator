from abc import ABC, abstractmethod

from numpy import double

from simulation_tools.game import *
from simulation_tools.game import Game

class FootballAgent(ABC):
    pass


class Player(FootballAgent):
    def __init__(self, stamina: int, vision: int, dorsal: int, team: str) -> None:
        super().__init__()
        self.stamina = stamina
        self.vision: double = vision / 10
        self.dorsal = dorsal
        self.team = team

    def get_perceptions(self, game: Game):
        x, y = game.field.find_player(self.dorsal, self.team)
        visible_grids = game.field.neighbor_grids(x, y, self.vision)
        empty_contigous_grids: List[GridField] = []
        for g, _ in visible_grids:
            if not g.is_empty and game.field.contigous_grids(g, (x, y)):
                empty_contigous_grids.append(g)
        friendly_grids = []
        for g, d in visible_grids:
            if game.field.friendly_grid(self.team, g):
                friendly_grids.append((g, d))
        


class Manager(FootballAgent):
    pass
