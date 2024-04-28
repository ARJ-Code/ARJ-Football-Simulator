from football_agent.simulator_agent import SimulatorAgent
from .actions import *
from football_tools.game import *
from typing import List, Tuple, Generator
from .player_strategy import FootballStrategy, PlayerStrategy


class Player:
    def __init__(self,  vision: int, dorsal: int, team: str, strategy: PlayerStrategy) -> None:
        self.strategy = strategy
        self.heuristic_strategy = FootballStrategy()
        self.vision: int = vision / 10
        self.dorsal = dorsal
        self.team = team

    def possible_actions(self, game: Game) -> List[Action]:
        visible_grids, p_grid = self.get_perceptions(game)

        actions = self.construct_actions(game, visible_grids, p_grid)

        return actions

    def play(self, simulator: SimulatorAgent):
        action = self.strategy.select_action(self.possible_actions, simulator)

        return action

    def play_heuristic(self, simulator: SimulatorAgent):

        action = self.heuristic_strategy.select_action(
            self.possible_actions, simulator)

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

    def empty_contiguous_grids(self, visible_grids: List[GridField], p_grid: GridField) -> Generator[GridField, None, None]:
        for g in visible_grids:
            if p_grid.is_contiguous(g) and g.is_empty():
                yield g

    def friendly_grids(self, visible_grids: List[GridField]) -> Generator[GridField, None, None]:
        for g in visible_grids:
            if g.team is not None and g.team == self.team:
                yield g

    def enemy_contiguous_grids(self, visible_grids: List[GridField], p_grid: GridField) -> Generator[GridField, None, None]:
        for g in visible_grids:
            if g.team is not None and g.team != self.team and p_grid.is_contiguous(g):
                yield g

    def construct_actions(self, game: Game, visible_grids: List[GridField], p_grid: GridField) -> List[Action]:
        actions: List[Action] = []

        actions.append(Nothing(self.dorsal, self.team, game))

        if self.get_data(game).power_stamina <= 0:
            return actions
        
        home_goal = game.field.goal_h[1]
        away_goal = game.field.goal_a[1]

        if not p_grid.ball:
            src = (p_grid.row, p_grid.col)
            if src != home_goal and src != away_goal:
                for grid in self.enemy_contiguous_grids(visible_grids, p_grid):
                    if grid.ball:
                        dest = (grid.row, grid.col)
                        actions.append(
                            StealBall(src, dest, self.dorsal, self.team, game))
                        break
                for grid in self.empty_contiguous_grids(visible_grids, p_grid):
                    dest = (grid.row, grid.col)
                    actions.append(Move(src, dest, self.dorsal, self.team, game))
        else:
            src = (p_grid.row, p_grid.col)
            for grid in self.empty_contiguous_grids(visible_grids, p_grid):
                if src == home_goal or src == away_goal:
                    break
                dest = (grid.row, grid.col)
                actions.append(MoveWithBall(
                    src, dest, self.dorsal, self.team, game))
                actions.append(
                    Dribble(src, dest, self.dorsal, self.team, game))
            for grid in self.friendly_grids(visible_grids):
                dest = (grid.row, grid.col)
                actions.append(Pass(src, dest, self.dorsal, self.team, game))
            if src != home_goal and src != away_goal:
                actions.append(Shoot(src, self.dorsal, self.team, game))

        return actions
