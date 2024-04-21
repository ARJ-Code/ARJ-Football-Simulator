from numpy import double, random
from football_tools.game import Game
from .actions import Action

class Behavior:
    def __init__(self, importance: double = 1) -> None:
        self.importance = importance

    def eval(self, action: Action, game: Game) -> double:
        pass

    def change_importance(self, importance: double) -> None:
        self.importance = importance

class Random(Behavior):
    def eval(self, action: Action, game: Game) -> double:
        return random.rand() * self.importance
    
class ReturnToPosition(Behavior):
    def eval(self, action: Action, game: Game) -> double:
        pass

class Defensive(Behavior):
    def eval(self, action: Action, game: Game) -> double:
        pass

class Ofensive(Behavior):
    def eval(self, action: Action, game: Game) -> double:
        pass

