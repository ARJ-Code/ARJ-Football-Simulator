from abc import ABC, abstractmethod
from .game import Game
from typing import Tuple
from typing import List
from .team import HOME, AWAY
from .data import StatisticsTeam, StatisticsPLayer
from .player_data import PlayerData
from random import random, randint


class Action(ABC):
    def __init__(self, src: Tuple[int, int], dest: Tuple[int, int], player: int, team: int, game: Game) -> None:
        super().__init__()
        self.src: Tuple[int, int] = src
        self.dest: Tuple[int, int] = dest
        self.player: int = player
        self.team: str = ''
        self.game: Game = game

    def get_player_data(self) -> PlayerData:
        if self.team == HOME:
            return self.game.game_data.home_players_data[self.player]
        else:
            return self.game.game_data.away_players_data[self.player]

    def get_statistics(self) -> StatisticsTeam:
        if self.team == HOME:
            return self.game.game_data.home_statistics
        else:
            return self.game.game_data.away_statistics

    def get_player_statistics(self) -> StatisticsPLayer:
        if self.team == HOME:
            return self.game.game_data.home_players_statistics[self.player]
        else:
            return self.game.game_data.away_players_statistics[self.player]

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def reset(self):
        pass


class Nothing(Action):
    def __init__(self) -> None:
        super().__init__((0, 0), (0, 0), -1, '', None)

    def execute(self):
        return super().execute()

    def reset(self):
        return super().reset()


class Pass(Action):
    def __init__(self, src: Tuple[int, int], dest: Tuple[int, int], player: int, team: str, game: Game) -> None:
        super().__init__(src, dest, player, team, game)

    def execute(self):
        self.get_player_data().power_stamina -= 1
        self.game.field.move_ball(self.src, self.dest)

    def reset(self):
        self.get_player_data().power_stamina += 1
        self.game.field.move_ball(self.dest, self.src)


class MoveWithBall(Action):
    def __init__(self, src: Tuple[int, int], dest: Tuple[int, int], player: int, team: str, game: Game) -> None:
        super().__init__(src, dest, player, team, game)

    def execute(self):
        self.get_player_data().power_stamina -= 2
        self.game.field.move_player(self.src, self.dest)
        self.game.field.move_ball(self.src, self.dest)

    def reset(self):
        self.get_player_data().power_stamina += 2
        self.game.field.move_player(self.dest, self.src)
        self.game.field.move_ball(self.dest, self.src)


class Move(Action):
    def __init__(self, src: Tuple[int, int], dest: Tuple[int, int], player: int, team: str, game: Game) -> None:
        super().__init__(src, dest, player, team, game)

    def execute(self):
        self.get_player_data().power_stamina -= 2
        self.game.field.move_player(self.src, self.dest)

    def reset(self):
        self.get_player_data().power_stamina += 2
        self.game.field.move_player(self.dest, self.src)


class Dribble(MoveWithBall):
    def __init__(self, src: Tuple[int, int], dest: Tuple[int, int], player: int, team: str, game: Game) -> None:
        super().__init__(src, dest, player, team, game)

    def execute(self):
        self.get_player_data().power_stamina -= 1
        return super().execute(self.game)

    def reset(self):
        self.get_player_data().power_stamina += 1
        return super().execute(self.game)


class StealBall(Action):
    def __init__(self, src: Tuple[int, int], dest: Tuple[int, int], player: int, team: str, game: Game) -> None:
        super().__init__(src, dest, player, team, game)

    def execute(self):
        self.get_player_data().power_stamina -= 1

    def reset(self):
        self.get_player_data().power_stamina += 1


class StealBallTrigger(Action):
    def __init__(self, action: StealBall) -> None:
        super().__init__(action.src, action.dest, action.player, action.game)

    def execute(self):
        self.game.field.move_ball(self.src, self.dest)

    def reset(self):
        self.game.field.move_ball(self.dest, self.src)


class Shoot(Action):
    def __init__(self, src: Tuple[int, int], player: int, team: str, game: Game) -> None:
        super().__init__(src, (0, 0), player, team, game)
        self.ok: bool = False

    def execute(self):
        self.get_player_data().power_stamina -= 2

        x, y = self.src
        q = self.get_player_data().shooting*2/100 / \
            ((self.game.field.distance_goal_h(self.src)
             if self.game.field[x][y].team == AWAY else self.game.field.distance_goal_b(self.src))+1)

        self.ok = random() <= q

        self.player.stamina -= 2
        if self.game.field.grid[x][y].team == AWAY:
            self.game.field.move_ball(self.src, self.game.field.goal_h)
        else:
            self.game.field.move_ball(self.src, self.game.field.goal_a)

    def reset(self):
        self.get_player_data().power_stamina += 2

        x, y = self.src

        self.player.stamina -= 2
        if self.game.field.grid[x][y].team == AWAY:
            self.game.field.move_ball(self.game.field.goal_h, self.src)
        else:
            self.game.field.move_ball(self.game.field.goal_a, self.src)


class GoalTrigger(Action):
    def __init__(self, action: Shoot) -> None:
        super().__init__((0, 0), (0, 0), action.player, action.team, action.game)

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


class AggressionTrigger(Action):
    def __init__(self, action: StealBall, level: int) -> None:
        super().__init__(action.src, action.dest, action.player, action.team, action.game)
        self.level: int = level
        self.break_play: bool = False
        x, y = self.src
        dorsal = self.game.field[x][y].player

        self.dorsal: int = dorsal

    def execute(self):
        x, y = self.src

        team_statistics = self.get_statistics()
        player_statistics = self.get_player_statistics()

        team_statistics.fouls += 1
        player_statistics.fouls += 1

        if self.level == 1:
            team_statistics.yellow_cards += 1
            player_statistics.yellow_cards += 1

        if self.level == 2:
            team_statistics.red_cards += 1
            player_statistics.red_cards += 1

        if player_statistics.red_cards == 1 or player_statistics.yellow_cards == 2:
            self.game.field[x][y].player = -1
            self.game.field[x][y].team = ''
            self.break_play = True

    def reset(self):
        x, y = self.src

        if player_statistics.red_cards == 1 or player_statistics.yellow_cards == 2:
            self.game.field[x][y].player = self.player
            self.game.field[x][y].team = self.team
            self.break_play = True

        team_statistics = self.get_statistics()
        player_statistics = self.get_player_statistics()

        team_statistics.fouls -= 1
        player_statistics.fouls -= 1

        if self.level == 1:
            team_statistics.yellow_cards -= 1
            player_statistics.yellow_cards -= 1

        if self.level == 2:
            team_statistics.red_cards -= 1
            player_statistics.red_cards -= 1


class ReorganizeLineUp(Action):
    def __init__(self, game: Game, line_up: List[Tuple[int, int, int]], team: str) -> None:
        super().__init__((0, 0), (0, 0), -1, team, game)
        self.team: str = team
        self.line_up: List[Tuple[int, int, int]] = line_up
        self.memory: List[Tuple[int, int, int]] = []

    def execute(self):
        for l in self.game.field.grid:
            for n in l:
                if self.team != n.team:
                    continue
                self.memory.append((n.player, n.row, n.col))
                n.player = -1
                n.team = ''

        for d, r, c in self.line_up:
            self.game.field.grid[r][c].player = d
            self.game.field.grid[r][c].team = self.team

    def reset(self):
        for _, r, c in self.line_up:
            self.game.field.grid[r][c].player = -1
            self.game.field.grid[r][c].team = ''

        for d, r, c in self.memory:
            self.game.field.grid[r][c].player = d
            self.game.field.grid[r][c].team = self.team


class Dispatch:
    def __init__(self) -> None:
        self.stack: List[Action] = []

    def dispatch(self, action: Action):
        self.stack.append(action)
        action.execute()

        if isinstance(action, StealBall):
            if isinstance(self.stack[-1], Dribble):
                self.dribbling_trigger(action)
            else:
                self.intercept_trigger(action)

    def intercept_trigger(self, action: StealBall):
        data = action.game.game_data

        x, y = action.src
        player_src = action.game.field.grid[x][y].player
        team = action.game.field.grid[x][y].team

        x, y = action.dest
        player_dest = action.game.field.grid[x][y].player

        if team == AWAY:
            props_a = [data.home_players_data[player_src].defending,
                       data.home_players_data[player_src].mentality_interceptions]
            props_h = [data.home_players_data[player_dest].movement_reactions,
                       data.home_players_data[player_dest].skill_ball_control]
        else:
            props_h = [data.home_players_data[player_src].defending,
                       data.home_players_data[player_src].mentality_interceptions]
            props_a = [data.home_players_data[player_dest].movement_reactions,
                       data.home_players_data[player_dest].skill_ball_control]

        if self.duel(props_h, props_a) == team:
            action = StealBallTrigger(action)
            self.stack.append(action)
            action.execute()

    def dribbling_trigger(self, action: StealBall):
        data = action.game.game_data

        x, y = action.src
        player_src = action.game.field.grid[x][y].player
        team = action.game.field.grid[x][y].team

        x, y = action.dest
        player_dest = action.game.field.grid[x][y].player

        if team == AWAY:
            props_a = [data.home_players_data[player_src].defending,
                       data.home_players_data[player_src].pace]
            props_h = [data.home_players_data[player_dest].pace,
                       data.home_players_data[player_dest].dribbling]
        else:
            props_h = [data.home_players_data[player_src].defending,
                       data.home_players_data[player_src].mentality_interceptions]
            props_a = [data.home_players_data[player_dest].pace,
                       data.home_players_data[player_dest].dribbling]

        if self.duel(props_h, props_a) == team:
            action = StealBallTrigger(action)
            self.stack.append(action)
            action.execute()
        else:
            rnd = randint(
                data.home_players_data[player_src].mentality_aggression, 100)
            if rnd >= 90 and rnd < 95:
                action = AggressionTrigger(action, 0, team)
                self.stack.append(action)
                action.execute()
            if rnd >= 95 and rnd < 100:
                action = AggressionTrigger(action, 1, team)
                self.stack.append(action)
                action.execute()
            if rnd == 100:
                action = AggressionTrigger(action, 2, team)
                self.stack.append(action)
                action.execute()

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
            action = GoalTrigger(action.game, team)
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
