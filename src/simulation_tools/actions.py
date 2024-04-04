from abc import ABC, abstractmethod
from .game import Game
from typing import Tuple
from typing import List
from .football_agent import Player
from .game import A, B
from random import random


class Action(ABC):
    def __init__(self, src: Tuple[int, int], dest: Tuple[int, int], player: Player, game: Game) -> None:
        super().__init__()
        self.src: Tuple[int, int] = src
        self.dest: Tuple[int, int] = dest
        self.player: Player = player
        self.game: Game = game

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def reset(self):
        pass


class Pass(Action):
    def __init__(self, src: Tuple[int], dest: Tuple[int], player: Player, game: Game) -> None:
        super().__init__(src, dest, player, game)

    def execute(self):
        self.player.stamina -= 1
        self.game.field.move_ball(self.src, self.dest)

    def reset(self):
        self.player.stamina += 1
        self.game.field.move_ball(self.dest, self.src)


class MoveWithBall(Action):
    def __init__(self, src: Tuple[int], dest: Tuple[int], player: Player, game: Game) -> None:
        super().__init__(src, dest, player, game)

    def execute(self):
        self.player.stamina -= 2
        self.game.field.move_player(self.src, self.dest, self.player)

    def reset(self):
        self.player.stamina += 2
        self.game.field.move_player(self.dest, self.src, self.player)


class Dribble(MoveWithBall):
    def __init__(self, src: Tuple[int], dest: Tuple[int], player: Player, game: Game) -> None:
        super().__init__(src, dest, player, game)

    def execute(self):
        self.player.stamina -= 1
        return super().execute(self.game)

    def reset(self):
        self.player.stamina += 1
        return super().execute(self.game)


class StealBall(Action):
    def __init__(self, src: Tuple[int], dest: Tuple[int], player: Player, game: Game) -> None:
        super().__init__(src, dest, player, game)

    def execute(self):
        self.player.stamina -= 1
        self.game.field.move_ball(self.src, self.dest)

    def reset(self):
        self.player.stamina += 1
        self.game.field.move_ball(self.dest, self.src)


class Shoot(Action):
    def __init__(self, src: Tuple[int], player: Player, game: Game) -> None:
        super().__init__(src, (0, 0), player, game)
        self.ok: bool = False

    def execute(self):
        x, y = self.src
        q = self.player.data.shooting*2/100 / \
            ((self.game.field.distance_goal_a(self.src)
             if self.game.field[x][y].team == B else self.game.field.distance_goal_a(self.src))+1)

        self.ok = random() <= q

        self.player.stamina -= 2
        if self.game.field.grid[x][y].team == A:
            self.game.field.move_ball(self.src, self.game.field.goal_b)
        else:
            self.game.field.move_ball(self.src, self.game.field.goal_b)

    def reset(self):
        x, y = self.src

        self.player.stamina -= 2
        if self.game.field.grid[x][y].team == A:
            self.game.field.move_ball(self.game.field.goal_b, self.src)
        else:
            self.game.field.move_ball(self.game.field.goal_b, self.src)


class Goal(Action):
    def __init__(self, player: Player, game: Game, team: str) -> None:
        super().__init__((0, 0), (0, 0), player, game)
        self.team: str = team

    def execute(self, game: Game):
        if self.team == A:
            game.statistics_team_h.goals += 1
        else:
            game.statistics_team_a.goals += 1

    def reset(self, game: Game):
        if self.team == A:
            game.statistics_team_h.goals -= 1
        else:
            game.statistics_team_a.goals -= 1


class Dispatch:
    def __init__(self) -> None:
        self.stack: List[Action] = []

    def dispatch(self, action: Action, team: str):
        attack = True

        if isinstance(action, StealBall):
            attack = False

        if attack:
            self.stack.append(action)
            return

    def shoot_trigger(self, action: Shoot, game, team: str):
        # x,y=
        # gk=
        pass

    def duel(props_h: List[int], props_a: List[int]) -> str:
        mh = sum(props_h)/len(props_h)
        ma = sum(props_a)/len(props_a)

        rnd_h, rnd_a = random()*(100-mh), random()*(100-ma)

        return A if rnd_h > rnd_a else B

    def reset(self, game: Game):
        self.stack[-1].reset(game)
        self.stack.pop()
