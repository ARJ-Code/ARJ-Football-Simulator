from typing import List

from football_agent.behavior import *
from .actions import Action
from football_tools.game import Game


class Strategy:
    def __init__(self) -> None:
        self.strategy = self.select_action
        self.behaviors: List[Behavior] = []

    def select_action(self, actions: List[Action], game: Game) -> Action:
        actions.sort(key=lambda a: sum([b.eval(a, game) for b in self.behaviors]))
        return actions[-1]


class RandomStrategy(Strategy):
    def __init__(self) -> None:
        super().__init__()
        self.behaviors: List[Behavior] = [Random()]

    # def select_action(self, actions: List[Action], game: Game) -> Action:
    #     return choice(actions)
        
class DefensorStrategy(Strategy):
    def __init__(self) -> None:
        super().__init__()
        self.behaviors: List[Behavior] = [Defensive(importance=0.8), 
                                          ReturnToPosition(importance=0.5),
                                          Ofensive(importance=0.2),
                                          Random(importance=0.2)]
        
class OfensorStrategy(Strategy):
    def __init__(self) -> None:
        super().__init__()
        self.behaviors: List[Behavior] = [Ofensive(importance=0.8), 
                                          ReturnToPosition(importance=0.5),
                                            Defensive(importance=0.2),
                                          Random(importance=0.2)]
        
class MidfielderStrategy(Strategy):
    def __init__(self) -> None:
        super().__init__()
        self.behaviors: List[Behavior] = [Ofensive(importance=0.6), 
                                          Defensive(importance=0.6),
                                          ReturnToPosition(importance=0.5),
                                          Random(importance=0.2)]
