from abc import ABC, abstractmethod
from .game import Game
from typing import Tuple
from typing import List
from .football_agent import Player
from .team import HOME, AWAY
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
            ((self.game.field.distance_goal_h(self.src)
             if self.game.field[x][y].team == AWAY else self.game.field.distance_goal_b(self.src))+1)

        self.ok = random() <= q

        self.player.stamina -= 2
        if self.game.field.grid[x][y].team == AWAY:
            self.game.field.move_ball(self.src, self.game.field.goal_h)
        else:
            self.game.field.move_ball(self.src, self.game.field.goal_a)

    def reset(self):
        x, y = self.src

        self.player.stamina -= 2
        if self.game.field.grid[x][y].team == AWAY:
            self.game.field.move_ball(self.game.field.goal_h, self.src)
        else:
            self.game.field.move_ball(self.game.field.goal_a, self.src)


class Goal(Action):
    def __init__(self, game: Game, team: str) -> None:
        super().__init__((0, 0), (0, 0), None, game)
        self.team: str = team

    def execute(self):
        if self.team == AWAY:
            self.game.statistics_team_a.goals += 1
        else:
            self.game.statistics_team_h.goals += 1

    def reset(self):
        if self.team == AWAY:
            self.game.statistics_team_a.goals -= 1
        else:
            self.game.statistics_team_h.goals -= 1


class Dispatch:
    def __init__(self) -> None:
        self.stack: List[Action] = []

    def dispatch(self, action: Action):
        attack = True

        if isinstance(action, StealBall):
            attack = False

        if attack:
            self.stack.append(action)
            if isinstance(action, Shoot) and action.ok:
                self.shoot_trigger(action)

            return

    def shoot_trigger(self, action: Shoot):
        data = action.game.game_data

        x, y = action.src
        player = action.game.field.grid[x][y].player
        team = action.game.field.grid[x][y].team

        x, y = action.game.field.goal_h if team == AWAY else action.game.field.goal_a
        gk = action.game.field.grid[x][y].player

        props_h = []
        props_a = []

        if team == AWAY:
            props_a = [data.home_players_data[player].shots]
            props_h = [data.home_players_data[gk].goal_keep_reflexes,
                       data.home_players_data[gk].goal_keep_diving]
        else:
            props_h = [data.home_players_statistics[player].shots]
            props_a = [data.away_players_data[gk].goal_keep_reflexes,
                       data.away_players_data[gk].goal_keep_diving]

        if self.duel(props_h, props_a) == team:
            action = Goal(action.game, team)
            self.stack.append(action)
            action.execute()

    def duel(self, props_h: List[int], props_a: List[int]) -> str:
        mh = sum(props_h)/len(props_h)
        ma = sum(props_a)/len(props_a)

        rnd_h, rnd_a = random()*(100-mh), random()*(100-ma)

        return HOME if rnd_h > rnd_a else AWAY

    def reset(self, game: Game):
        self.stack[-1].reset(game)
        self.stack.pop()
