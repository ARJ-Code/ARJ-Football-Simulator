from abc import ABC, abstractmethod
from .game import Game
from typing import Tuple
from typing import List
from .football_agent import Player
from .game import A, B
from random import random


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
        super().__init__(src, dest, player)

    def execute(self, game: Game):
        self.player.stamina -= 1
        game.field.move_ball(self.src, self.dest)

    def reset(self, game: Game):
        self.player.stamina += 1
        game.field.move_ball(self.dest, self.src)


class Shoot(Action):
    def __init__(self, src: Tuple[int], player: Player) -> None:
        super().__init__(src, (0, 0), player)
        self.ok: bool = False

    def execute(self, game: Game):
        x, y = self.src
        q = self.player.data.shooting*2/100 / \
            ((game.field.distance_goal_a(self.src)
             if game.field[x][y].team == B else game.field.distance_goal_a(self.src))+1)

        self.ok = random() <= q

        self.player.stamina -= 2
        if game.field.grid[x][y].team == A:
            game.field.move_ball(self.src, game.field.goal_b)
        else:
            game.field.move_ball(self.src, game.field.goal_b)

    def reset(self, game: Game):
        x, y = self.src

        self.player.stamina -= 2
        if game.field.grid[x][y].team == A:
            game.field.move_ball(game.field.goal_b, self.src)
        else:
            game.field.move_ball(game.field.goal_b, self.src)


class Goal(Action):
    def __init__(self, player: Player, team: str) -> None:
        super().__init__((0, 0), (0, 0), player)
        self.team: str = team

    def execute(self, game: Game):
        if self.team == A:
            game.statistics_team_a.goals += 1
        else:
            game.statistics_team_b.goals += 1

    def reset(self, game: Game):
        if self.team == A:
            game.statistics_team_a.goals -= 1
        else:
            game.statistics_team_b.goals -= 1


class Dispatch:
    def __init__(self) -> None:
        self.stack: List[Action] = []

    def dispatch(self, action: Action, game: Game, team: str):
        attack = True

        if isinstance(action, StealBall):
            attack = False

        if attack:
            self.stack.append(action)
            return

    def duel(props_a: List[int], props_b: List[int]) -> str:
        ma = sum(props_a)/len(props_a)
        mb = sum(props_a)/len(props_b)

        rnd_a, rnd_b = random()*(100-ma), random()*(100-mb)

        return A if rnd_a > rnd_b else B

    def reset(self, game: Game):
        self.stack[-1].reset(game)
        self.stack.pop()
