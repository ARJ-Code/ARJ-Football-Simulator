from abc import ABC, abstractmethod
from .game import Game
from typing import Tuple
from typing import List
from .football_agent import Player


class Action(ABC):
    def __init__(self, src: Tuple[int, int], dest: Tuple[int, int], player: Player) -> None:
        super().__init__()
        self.src: Tuple[int, int] = src
        self.dest: Tuple[int, int] = dest
        self.player: Player = player

    @abstractmethod
    def execute(self, game: Game):
        pass

    @abstractmethod
    def reset(self, game: Game):
        pass


class Pass(Action):
    def __init__(self, src: Tuple[int], dest: Tuple[int], player: Player) -> None:
        super().__init__(src, dest, player)

    def execute(self, game: Game):
        self.player.stamina -= 1
        game.field.move_ball(self.src, self.dest)

    def reset(self, game: Game):
        self.player.stamina += 1
        game.field.move_ball(self.dest, self.src)


class MoveWithBall(Action):
    def __init__(self, src: Tuple[int], dest: Tuple[int], player: Player) -> None:
        super().__init__(src, dest, player)

    def execute(self, game: Game):
        self.player.stamina -= 2
        game.field.move_player(self.src, self.dest, self.player)

    def reset(self, game: Game):
        self.player.stamina += 2
        game.field.move_player(self.dest, self.src, self.player)


class Dribble(MoveWithBall):
    def __init__(self, src: Tuple[int], dest: Tuple[int], player: Player) -> None:
        super().__init__(src, dest, player)

    def execute(self, game: Game):
        self.player.stamina -= 1
        return super().execute(game)
    
    def reset(self, game: Game):
        self.player.stamina += 1
        return super().execute(game)


class StealBall(Action):
    def __init__(self, src: Tuple[int], dest: Tuple[int], player: Player) -> None:
        super().__init__(src, dest)

    def execute(self, game: Game):
        self.player.stamina -= 1
        game.field.move_ball(self.src, self.dest)

    def reset(self, game: Game):
        self.player.stamina += 1
        game.field.move_ball(self.dest, self.src)

class Shoot(Action):
    def __init__(self, src: Tuple[int], dest: Tuple[int], player: Player) -> None:
        super().__init__(src, dest, player)

    def execute(self, game: Game):
        
        
        


class Dispatch:
    def __init__(self) -> None:
        self.stack: List[Action] = []

    def dispatch(self, action: Action, game: Game):
        attack = True

        if isinstance(action, StillBall):
            attack = True

        if attack:
            self.stack.append(action)
            return
        
    def reset(self,game:Game):
        self.stack[-1].reset(game)
        self.stack.pop()
