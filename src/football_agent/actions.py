from abc import ABC, abstractmethod
from football_tools.game import Game
from football_tools.data import StatisticsTeam, StatisticsPLayer, PlayerData
from typing import List, Tuple, Dict
from random import random, randint
from football_tools.line_up import LineUp

AWAY = 'A'
HOME = 'H'


class Action(ABC):
    def __init__(self, src: Tuple[int, int], dest: Tuple[int, int], player: int, team: int, game: Game) -> None:
        super().__init__()
        self.src: Tuple[int, int] = src
        self.dest: Tuple[int, int] = dest
        self.player: int = player
        self.team: str = team
        self.game: Game = game

    def get_player_data(self) -> PlayerData:
        if self.team == HOME:
            return self.game.home.data[self.player]
        else:
            return self.game.away.data[self.player]

    def get_statistics(self) -> StatisticsTeam:
        if self.team == HOME:
            return self.game.home.statistics
        else:
            return self.game.away.statistics

    def get_player_statistics(self) -> StatisticsPLayer:
        if self.team == HOME:
            return self.game.home.players_statistics[self.player]
        else:
            return self.game.away.players_statistics[self.player]

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
        return super().execute()

    def reset(self):
        self.get_player_data().power_stamina += 1
        return super().execute()


class StealBall(Action):
    def __init__(self, src: Tuple[int, int], dest: Tuple[int, int], player: int, team: str, game: Game) -> None:
        super().__init__(src, dest, player, team, game)

    def execute(self):
        self.get_player_data().power_stamina -= 1

    def reset(self):
        self.get_player_data().power_stamina += 1


class StealBallTrigger(Action):
    def __init__(self, action: StealBall) -> None:
        super().__init__(action.dest, action.src, action.player, action.team, action.game)

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
             if self.game.field.grid[x][y].team == AWAY else self.game.field.distance_goal_a(self.src))+1)

        self.ok = random() <= q

    def reset(self):
        self.get_player_data().power_stamina += 2

        x, y = self.src

        self.player.stamina -= 2
        if self.game.field.grid[x][y].team == AWAY:
            self.game.field.move_ball(self.game.field.goal_h, self.src)
        else:
            self.game.field.move_ball(self.game.field.goal_a, self.src)


class GoalTrigger(Action):
    def __init__(self, action: Shoot, team: str) -> None:
        super().__init__((0, 0), (0, 0), -1, team, action.game)

    def execute(self):
        if self.team == AWAY:
            self.game.away.statistics.goals += 1
        else:
            self.game.home.statistics.goals += 1

    def reset(self):
        if self.team == AWAY:
            self.game.statistics_team_a.goals -= 1
        else:
            self.game.statistics_team_h.goals -= 1


class AggressionTrigger(Action):
    def __init__(self, action: StealBall, level: int) -> None:
        super().__init__(action.src, action.dest, action.player, action.team, action.game)
        self.level: int = level
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


class ReorganizeField(Action):
    def __init__(self, game: Game, team: str, has_ball: bool) -> None:
        super().__init__((0, 0), (0, 0), -1, team, game)
        self.team: str = team
        self.line_up: LineUp = game.home.line_up if team == HOME else game.away.line_up
        self.memory: List[Tuple[int, int, int, str]] = []
        self.memory_ball: Tuple[int, int] = (0, 0)
        self.has_ball: bool = has_ball

    def execute(self):
        for l in self.game.field.grid:
            for n in l:
                if self.team != n.team:
                    continue
                if n.ball:
                    n.ball = False
                    self.memory_ball = (n.row, n.col)

                self.memory.append((n.player, n.row, n.col, n.team))
                n.player = -1
                n.team = ''

        for i in self.line_up.line_up.values():
            r, c, d = i.row, i.col, i.player
            self.game.field.grid[r][c].player = d
            self.game.field.grid[r][c].team = self.team

        if self.has_ball:
            r, c = -1, -1
            if self.team == HOME:
                r, c = 18, 5
            else:
                r, c = 1, 5
            self.game.field.grid[r][c].ball = True

    def reset(self):
        for _, r, c in self.line_up:
            self.game.field.grid[r][c].ball = False
            self.game.field.grid[r][c].player = -1
            self.game.field.grid[r][c].team = ''

        r, c = self.memory_ball
        self.game.field.grid[r][c].ball = True

        for d, r, c in self.memory:
            self.game.field.grid[r][c].player = d
            self.game.field.grid[r][c].team = self.team


class ChangeLineUp(Action):
    def __init__(self,  team: int, game: Game, line_up: LineUp) -> None:
        super().__init__((0, 0), (0, 0), -1, team, game)
        self.line_up: LineUp = line_up
        self.memory: LineUp = game.home.line_up if team == HOME else game.away.line_up

    def execute(self):
        if self.team == HOME:
            self.game.home.line_up = self.line_up
        else:
            self.game.away.line_up = self.line_up

    def reset(self):
        if self.team == HOME:
            self.game.home.line_up = self.memory
        else:
            self.game.away.line_up = self.memory


class ChangePlayer(Action):
    def __init__(self, player: int, new_player: int, team: int, game: Game) -> None:
        super().__init__((0, 0), (0, 0), player, team, game)
        self.new_player: int = new_player

    def execute(self):
        line_up = self.game.home.line_up if self.team == HOME else self.game.away.line_up
        pos = line_up.get_player_position(self.player)

        pos.conf_player(self.game.home.data[self.new_player] if self.team ==
                        HOME else self.game.away.data[self.new_player])

    def reset(self):
        line_up = self.game.home.line_up if self.team == HOME else self.game.away.line_up
        pos = line_up.get_player_position(self.new_player)

        pos.conf_player(self.game.home.data[self.player] if self.team ==
                        HOME else self.game.away.data[self.player])


class MiddleTime(Action):
    def __init__(self, team: str, game: Game) -> None:
        super().__init__((0, 0), (0, 0), -1, team, game)
        self.memory: Dict[int, int] = {}

    def execute(self):
        data = self.game.home.data if self.team == HOME else self.game.away.data

        for p in data.keys():
            self.memory[p] = data[p].power_stamina
            data[p].power_stamina = min(
                data[p].power_stamina+data[p].o_power_stamina/2, data[p].o_power_stamina)

    def reset(self):
        data = self.game.home.data if self.team == HOME else self.game.away.data

        for p in data.keys():
            data[p].power_stamina = self.memory[p]


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
        if isinstance(action, Shoot):
            if action.ok:
                self.shoot_trigger(action)

            action_h = ReorganizeField(action.game, HOME, action.team != HOME)
            action_a = ReorganizeField(action.game, AWAY, action.team != AWAY)
            self.stack.append(action_h)
            self.stack.append(action_a)
            action_h.execute()
            action_a.execute()

    def intercept_trigger(self, action: StealBall):
        game = action.game

        x, y = action.src
        player_src = action.game.field.grid[x][y].player
        team = action.game.field.grid[x][y].team

        x, y = action.dest
        player_dest = action.game.field.grid[x][y].player

        if action.team == HOME:
            props_h = [game.home.data[player_src].defending,
                       game.home.data[player_src].mentality_interceptions]
            props_a = [game.away.data[player_dest].movement_reactions,
                       game.away.data[player_dest].skill_ball_control]
        else:
            props_h = [game.home.data[player_dest].defending,
                       game.home.data[player_dest].mentality_interceptions]
            props_a = [game.away.data[player_src].movement_reactions,
                       game.away.data[player_src].skill_ball_control]

        if self.duel(props_h, props_a) == team:
            action = StealBallTrigger(action)

            self.stack.append(action)

            action.execute()

    def dribbling_trigger(self, action: StealBall):
        game = action.game

        x, y = action.src
        player_src = action.game.field.grid[x][y].player
        team = action.game.field.grid[x][y].team

        x, y = action.dest
        player_dest = action.game.field.grid[x][y].player

        props_h = [game.home.data[player_src].defending,
                   game.home.data[player_src].pace]
        props_a = [game.away.data[player_dest].pace,
                   game.away.data[player_dest].dribbling]

        if team == AWAY:
            props_a, props_h = props_h, props_a

        if self.duel(props_h, props_a) == team:
            action = StealBallTrigger(action)
            self.stack.append(action)
            action.execute()
        else:
            rnd = randint(
                game.home.data[player_src].mentality_aggression, 100)
            if rnd >= 90 and rnd < 95:
                action = AggressionTrigger(action, 0, team)
                self.stack.append(action)
                action.execute()
                self.break_play = True
            if rnd >= 95 and rnd < 100:
                action = AggressionTrigger(action, 1, team)
                self.stack.append(action)
                action.execute()
                self.break_play = True
            if rnd == 100:
                action = AggressionTrigger(action, 2, team)
                self.stack.append(action)
                action.execute()

    def shoot_trigger(self, action: Shoot):
        game = action.game
        x, y = action.src
        player = action.game.field.grid[x][y].player
        team = action.game.field.grid[x][y].team

        x, y = (1, 5) if team == AWAY else (18, 5)
        gk = action.game.field.grid[x][y].player

        if team == AWAY:
            props_a = [game.away.data[player].shooting]

            props_h = [game.home.data[gk].goal_keep_reflexes,
                       game.home.data[gk].goal_keep_diving]

        else:
            props_h = [game.home.data[player].shooting]

            props_a = [game.away.data[gk].goal_keep_reflexes,
                       game.away.data[gk].goal_keep_diving]

        if self.duel(props_h, props_a) == team:
            action = GoalTrigger(action, team)
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
