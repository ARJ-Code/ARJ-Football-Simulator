from typing import List
from abc import ABC, abstractmethod
from random import choice
from .actions import Action
from football_tools.line_up import *
from football_tools.game import Game
from .simulator_agent import SimulatorAgent

HOME = 'H'
AWAY = 'A'


class ManagerStrategy(ABC):
    @abstractmethod
    def get_line_up(self, team: str, line_ups: List[LineUp], simulator: SimulatorAgent) -> LineUp:
        pass

    @abstractmethod
    def action(self, game: Game) -> Action:
        pass


class RandomStrategy(ManagerStrategy):
    def get_line_up(self, team: str,line_ups: List[LineUp], simulator: SimulatorAgent) -> LineUp:
        return choice(line_ups)

    def action(self, game: Game) -> Action:
        return super().action(game)


class SimulateStrategy(ManagerStrategy):
    def get_line_up(self, team: str, line_ups: List[LineUp], simulator: SimulatorAgent) -> LineUp:
        def simulation(line_up: LineUp):
            pass
            # simulator = Simulator(agents[0], agents[1], game)
            # game.instance = 0

            # if team == HOME:
            #     game.conf_line_ups(
            #         line_up, agents[1].manager.get_line_up())
            # else:
            #     game.conf_line_ups(
            #         agents[0].manager.get_line_up(), line_up)

            # game.instance = 1

            # while not self.game.is_finish():
            #     simulator.simulate_instance()

    def action(self, game: Game) -> Action:
        return super().action(game)
