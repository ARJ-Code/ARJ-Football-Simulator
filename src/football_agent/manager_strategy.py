from typing import List
from abc import ABC, abstractmethod
from random import choice
from .actions import Action
from football_tools.line_up import *
from football_tools.game import Game


class ManagerStrategy(ABC):
    @abstractmethod
    def get_line_up(self, line_ups: List[LineUp]) -> LineUp:
        pass

    @abstractmethod
    def action(self, game: Game) -> Action:
        pass


class RandomStrategy(ManagerStrategy):
    def get_line_up(self, line_ups: List[LineUp]) -> LineUp:
        return choice(line_ups)

    def action(self, game: Game) -> Action:
        return super().action(game)
