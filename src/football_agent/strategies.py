from random import choice
from typing import List
from .actions import Action
from football_tools.game import Game


class Strategy:
    def __init__(self) -> None:
        self.strategy = self.select_action

    def select_action(self, actions: List[Action], game: Game) -> Action:
        pass


class RandomStrategy(Strategy):
    def select_action(self, actions: List[Action], game: Game) -> Action:
        return choice(actions)
