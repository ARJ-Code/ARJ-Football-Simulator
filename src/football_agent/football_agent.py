from abc import ABC

from .actions import *
from football_tools.game import *
from typing import List, Tuple, Generator

from football_agent.strategies import Strategy

AWAY = 'A'
HOME = 'H'


class FootballAgent(ABC):
    def __init__(self, strategy: Strategy) -> None:
        self.strategy = strategy

    def select_action(self, actions: List[Action], game: Game) -> Action:
        return self.strategy.select_action(actions, game)


class Player(FootballAgent):
    def __init__(self,  vision: int, dorsal: int, team: str, strategy: Strategy) -> None:
        super().__init__(strategy)
        self.vision: int = vision / 10
        self.dorsal = dorsal
        self.team = team

    def play(self, game: Game):
        visible_grids, p_grid = self.get_perceptions(game)

        actions = self.construct_actions(game, visible_grids, p_grid)

        action = self.select_action(actions, game)

        return action

    def get_data(self, game: Game) -> PlayerData:
        if self.team == HOME:
            return game.home.data[self.dorsal]
        else:
            return game.away.data[self.dorsal]

    def get_perceptions(self, game: Game) -> Tuple[List[GridField], GridField]:
        p_grid: GridField = game.field.find_player(self.dorsal, self.team)
        visible_grids: List[GridField] = game.field.neighbor_grids(
            p_grid, self.vision)

        return visible_grids, p_grid

    def is_contiguous(self, f: GridField, s: GridField):
        return (abs(f.row - s.row) == 1 and abs(f.col - s.col) == 1) or (abs(f.row - s.row) + abs(f.col - s.col) == 1)

    def empty_contiguous_grids(self, visible_grids: List[GridField], p_grid: GridField) -> Generator[GridField, None, None]:
        for g in visible_grids:
            if self.is_contiguous(p_grid, g) and g.is_empty():
                yield g

    def friendly_grids(self, visible_grids: List[GridField]) -> Generator[GridField, None, None]:
        for g in visible_grids:
            if g.team is not None and g.team == self.team:
                yield g

    def enemy_contiguous_grids(self, visible_grids: List[GridField], p_grid: GridField) -> Generator[GridField, None, None]:
        for g in visible_grids:
            if g.team is not None and g.team != self.team and self.is_contiguous(p_grid, g):
                yield g

    def construct_actions(self, game: Game, visible_grids: List[GridField], p_grid: GridField) -> List[Action]:
        actions: List[Action] = []

        actions.append(Nothing())

        if self.get_data(game).power_stamina <= 0:
            return actions

        if not p_grid.ball:
            src = (p_grid.row, p_grid.col)
            for grid in self.enemy_contiguous_grids(visible_grids, p_grid):
                if grid.ball:
                    dest = (grid.row, grid.col)
                    actions.append(
                        StealBall(src, dest, self.dorsal, self.team, game))
                    break
            for grid in self.empty_contiguous_grids(visible_grids, p_grid):
                if src == (1, 5) or src == (18, 5):
                    break
                dest = (grid.row, grid.col)
                actions.append(Move(src, dest, self.dorsal, self.team, game))
        else:
            src = (p_grid.row, p_grid.col)
            for grid in self.empty_contiguous_grids(visible_grids, p_grid):
                if src == (1, 5) or src == (18, 5):
                    break
                dest = (grid.row, grid.col)
                actions.append(MoveWithBall(
                    src, dest, self.dorsal, self.team, game))
                actions.append(
                    Dribble(src, dest, self.dorsal, self.team, game))
            for grid in self.friendly_grids(visible_grids):
                dest = (grid.row, grid.col)
                actions.append(Pass(src, dest, self.dorsal, self.team, game))
            actions.append(Shoot(src, self.dorsal, self.team, game))

        return actions
    
    # def filter_actions(self, )


class Manager(FootballAgent):
    pass
