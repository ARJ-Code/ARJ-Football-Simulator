from football_agent.actions import Dispatch, MiddleTime
from football_tools.game import Game
from football_tools.data import TeamData
from football_agent.team import HOME, AWAY, TeamAgent
from typing import Generator, Tuple
from football_agent.simulator_agent import SimulatorAgent
import math
from typing import List


class FootballSimulation:
    def __init__(self, home: Tuple[TeamAgent, TeamData], away: Tuple[TeamAgent, TeamData]) -> None:
        self.home: TeamAgent = home[0]
        self.away: TeamAgent = away[0]
        self.game: Game = Game(home[1], away[1], 180)

    def simulate(self) -> Generator[str, None, None]:
        simulator = Simulator(self.home, self.away, self.game)

        simulator.start_instance()

        field_str = str(self.game.field)

        statistics = self.game_statistics(
            self.game.instance-1, self.game.cant_instances)

        yield field_str+'\n'+statistics

        while not self.game.is_finish():
            simulator.simulate_instance()

            field_str = str(self.game.field)
            statistics = self.game_statistics(
                self.game.instance-1, self.game.cant_instances)

            yield field_str+'\n'+statistics

    def game_statistics(self, instance: int, actions: int) -> str:
        nh = f'\033[34m{self.home.name}\033[0m'
        na = f'\033[31m{self.away.name}\033[0m'
        gh = self.game.home.statistics.goals
        ga = self.game.away.statistics.goals
        yh = self.game.home.statistics.yellow_cards
        ya = self.game.away.statistics.yellow_cards
        rh = self.game.home.statistics.red_cards
        ra = self.game.away.statistics.red_cards
        ph = self.game.home.statistics.possession_instances*100//(instance+1)
        pa = self.game.away.statistics.possession_instances*100//(instance+1)
        tm = int(math.modf(instance/actions*90)[1])
        ts = int(math.modf(instance/actions*90)[0]*60)

        def get_spaces(n):
            return ' '*(n)

        def get_num(n):
            if n < 10:
                return '  '+str(n)
            if n < 100:
                return ' '+str(n)
            return str(n)

        def get_num1(n):
            if n < 10:
                return '0'+str(n)
            return str(n)

        len_s = len(nh)+len(na)-18

        return f"""
{get_spaces(24)}{get_num1(tm)}:{get_num1(ts)}
{nh}{get_spaces(52-len_s)}{na}
⚽ {get_num(gh)}{get_spaces(40)}{get_num(ga)} ⚽
⌛ {get_num(ph)}{get_spaces(40)}{get_num(pa)} ⌛
🟨 {get_num(yh)}{get_spaces(40)}{get_num(ya)} 🟨
🟥 {get_num(rh)}{get_spaces(40)}{get_num(ra)} 🟥
                """


class Simulator:
    def __init__(self, home: TeamAgent, away: TeamAgent, game: Game) -> None:
        self.home: TeamAgent = home
        self.away: TeamAgent = away
        self.game: Game = game
        self.stack: List = []
        self.dispatch = Dispatch()

    def start_instance(self):
        self.game.instance = 0
        self.game.conf_line_ups(
            self.home.manager.get_line_up(SimulatorManager(self)), self.away.manager.get_line_up(SimulatorManager(self)))
        self.game.instance = 1

    def simulate_instance(self, current_player: Tuple[int, str] = (-1, '')):
        self.stack.append(len(self.dispatch.stack))

        if self.game.is_middle():
            self.dispatch.dispatch(MiddleTime(self.game, HOME))

        player_with_ball = -1
        team = ''

        for l in self.game.field.grid:
            for n in l:
                if n.ball:
                    player_with_ball = n.player
                    team = n.team

        if team == HOME:
            self.game.home.statistics.possession_instances += 1
            if current_player[1] != HOME and current_player[0] != player_with_ball:
                self.dispatch.dispatch(
                    self.home.players[player_with_ball].play(self.game))
        if team == AWAY:
            self.game.away.statistics.possession_instances += 1
            if current_player[1] != AWAY and current_player[0] != player_with_ball:
                self.dispatch.dispatch(
                    self.away.players[player_with_ball].play(self.game))

        mask = set()

        for l in self.game.field.grid:
            for n in l:

                if (n.player, n.team) in mask:
                    continue

                if n.team == current_player[1] and n.player == current_player[0]:
                    continue
                if not n.ball:
                    mask.add((n.player, n.team))
                    if n.team == HOME:
                        self.dispatch.dispatch(
                            self.home.players[n.player].play(self.game))
                    if n.team == AWAY:
                        self.dispatch.dispatch(
                            self.away.players[n.player].play(self.game))

        self.game.instance += 1

    def reset_all(self):
        while self.game.instance != 1:
            self.reset_instance()

    def reset_instance(self):
        self.game.instance -= 1

        while len(self.dispatch.stack) != self.stack[-1]:
            self.dispatch.reset()
        self.stack.pop()

        team = ''

        for l in self.game.field.grid:
            for n in l:
                if n.ball:
                    team = n.team

        if team == HOME:
            self.game.home.statistics.possession_instances -= 1
        if team == AWAY:
            self.game.away.statistics.possession_instances -= 1


class SimulatorManager(SimulatorAgent):
    def __init__(self, simulator: Simulator):
        super().__init__(simulator.game)
        self.simulator = simulator

    def simulate(self):
        while not self.game.is_finish():
            self.simulator.simulate_instance()

    def reset(self):
        self.simulator.reset_all()
