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
        game.field.grid[self.src[0]][self.src[1]].player.stamina -= 1
        game.field.grid[self.src[0]][self.src[1]].ball = False
        game.field.grid[self.dest[0]][self.dest[1]].ball = True

    def reset(self, game: Game):
        game.field.grid[self.src[0]][self.src[1]].player.stamina += 1

        game.field.grid[self.src[0]][self.src[1]].ball = True
        game.field.grid[self.dest[0]][self.dest[1]].ball = False


class MoveWithBall(Action):
    def __init__(self, src: Tuple[int], dest: Tuple[int], player: Player) -> None:
        super().__init__(src, dest, player)

    def execute(self, game: Game):
        game.field.grid[self.src[0]][self.src[1]].player.stamina -= 2

        player = game.field.grid[self.src[0]][self.src[1]].player

        game.field.grid[self.src[0]][self.src[1]].ball = False
        game.field.grid[self.dest[0]][self.dest[1]].ball = True

        game.field.grid[self.dest[0]][self.dest[1]].player = player

    def reset(self, game: Game):
        game.field.grid[self.src[0]][self.src[1]].player.stamina += 2

        player = game.field.grid[self.dest[0]][self.dest[1]].player

        game.field.grid[self.dest[0]][self.dest[1]].ball = False
        game.field.grid[self.src[0]][self.src[1]].ball = True

        game.field.grid[self.src[0]][self.src[1]].player = player


class Dribble(MoveWithBall):
    def __init__(self, src: Tuple[int], dest: Tuple[int], player: Player) -> None:
        super().__init__(src, dest, player)

    def execute(self, game: Game):
        game.field.grid[self.src[0]][self.src[1]].player.stamina -= 1
        return super().execute(game)


class StillBall(Action):
    def __init__(self, src: Tuple[int], dest: Tuple[int], player: Player) -> None:
        super().__init__(src, dest)

    def execute(self, game: Game):
        game.field.grid[self.src[0]][self.src[1]].player.stamina -= 1

        game.field.grid[self.src[0]][self.src[1]].ball = True
        game.field.grid[self.dest[0]][self.dest[1]].ball = False

    def reset(self, game: Game):
        game.field.grid[self.src[0]][self.src[1]].player.stamina += 1

        game.field.grid[self.src[0]][self.src[1]].ball = False
        game.field.grid[self.dest[0]][self.dest[1]].ball = True

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
