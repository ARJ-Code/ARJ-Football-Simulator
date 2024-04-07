from abc import ABC, abstractmethod

from numpy import double

from simulation_tools.actions import *
from simulation_tools.game import *
from simulation_tools.game import Game
from simulation_tools.game import GridField
from typing import List, Tuple

class FootballAgent(ABC):
    pass


class Player(FootballAgent):
    def __init__(self, stamina: int, vision: int, dorsal: int, team: str) -> None:
        super().__init__()
        # self.stamina = stamina
        self.vision: double = vision % 10
        self.dorsal = dorsal
        self.team = team

    def get_perceptions(self, game: Game):
        p_grid: GridField = game.field.find_player(self.dorsal, self.team)
        visible_grids: List[GridField] = game.field.neighbor_grids(p_grid, self.vision)
        self_goal: List[Tuple[int, int]] = game.field.self_goal(self.team)
        enemy_goal: List[Tuple[int, int]] = game.field.enemy_goal(self.team)

        empty_contiguous_grids: List[GridField] = []
        for g in visible_grids:
            if not g.is_empty and self.contiguous_grids(g, (p_grid.row, p_grid.col)):
                empty_contiguous_grids.append(g)
                
        friendly_grids: List[GridField] = []
        for g in visible_grids:
            if self.is_friendly_grid(self.team, g):
                friendly_grids.append(g)
                
        enemy_contiguous_grids: List[GridField] = []
        for g in visible_grids:
            if self.is_enemy_grid(self.team, g) and self.contiguous_grids(g, (p_grid.row, p_grid.col)):
                enemy_contiguous_grids.append(g)

        actions: List[Action] = self.construct_actions(game, p_grid.ball, empty_contiguous_grids, friendly_grids, enemy_contiguous_grids)

    def contiguous_grids(self, f: Tuple[int, int], dest: Tuple[int, int]) -> bool:
        return abs(f[0] - dest[0]) == 1 or abs(f[1] - dest[1]) == 1
    
    def is_friendly_grid(self, g: GridField) -> bool:
        return self.team is not None and g.team == self.team
    
    def is_enemy_grid(self, team: str, g: Tuple[int, int]) -> bool:
        x, y = g
        return self.grid[x][y].team is not None and self.grid[x][y].team != team
    
    def construct_actions(self, game: Game, has_ball: bool, empty_contiguous_grids: List[GridField], 
                          friendly_grids: List[GridField], enemy_contiguous_grids: List[GridField]) -> List[Action]:
        actions: List[Action] = []
        if not has_ball:
            for grid in enemy_contiguous_grids:
                if grid.ball:
                    actions.append(StealBall())
                    break
        else:
            for grid in empty_contiguous_grids:
                actions.append(MoveWithBall())
                actions.append(Dribble())
            for grid in friendly_grids:
                actions.append(Pass())
            actions.append(Shoot())

        return actions
            

class Manager(FootballAgent):
    pass
