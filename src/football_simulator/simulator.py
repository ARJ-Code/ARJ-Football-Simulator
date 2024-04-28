from football_agent.actions import Dispatch, MiddleTime, IncrementInstance, IncrementPossession
from football_tools.game import Game
from football_tools.data import TeamData
from football_agent.team import TeamAgent
from typing import Generator, Tuple, Set, List
from football_agent.simulator_agent import SimulatorAgent
from football_agent.manager_agent import Manager
from football_agent.manager_action_strategy import ActionSimulateStrategy, ActionMiniMaxStrategy
from football_tools.enum import HOME, AWAY

import math

CANT_INSTANCES = 180
INTERVAL_MANGER = 20


class FootballSimulation:
    def __init__(self, home: Tuple[TeamAgent, TeamData], away: Tuple[TeamAgent, TeamData]) -> None:
        self.home: TeamAgent = home[0]
        self.away: TeamAgent = away[0]
        self.game: Game = Game(home[1], away[1], CANT_INSTANCES)

    def simulate(self) -> Generator[str, None, None]:
        simulator = Simulator(self.home, self.away, self.game)

        simulator.start_instance()

        field_str = str(self.game.field)

        statistics = self.game_statistics(
            self.game.instance-1, self.game.cant_instances)

        yield field_str+'\n'+statistics

        while not self.game.is_finish():
            simulator.simulate_instance(set([]))

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
        self.stack: List[int] = []
        self.dispatch = Dispatch()

    def start_instance(self):
        self.game.instance = 0

        home_line_up = self.home.manager.get_line_up(
            SimulatorLineUpManager(self))
        away_line_up = self.away.manager.get_line_up(
            SimulatorLineUpManager(self))

        self.game.conf_line_ups(home_line_up, away_line_up)
        self.game.instance = 1

    def simulate_players(self, team: str, player_with_ball: int, mask: Set[Tuple[int, str]], heuristic_player: bool):
        sim = self.get_player_simulator(team, mask)

        if team == HOME and not (player_with_ball, team) in mask:
            self.dispatch.dispatch(
                self.home.players[player_with_ball].play_heuristic(sim) if heuristic_player else
                self.home.players[player_with_ball].play(sim))
        if team == AWAY and not (player_with_ball, team) in mask:
            self.dispatch.dispatch(
                self.away.players[player_with_ball].play_heuristic(sim) if heuristic_player else
                self.away.players[player_with_ball].play(sim))

        mask.add((player_with_ball, team))

        for l in self.game.field.grid:
            for n in l:

                if (n.player, n.team) in mask:
                    continue

                if not n.ball:
                    mask.add((n.player, n.team))
                    if n.team == HOME:
                        self.dispatch.dispatch(
                            self.home.players[n.player].play_heuristic(sim) if heuristic_player else
                            self.home.players[n.player].play(sim))
                    if n.team == AWAY:
                        self.dispatch.dispatch(
                            self.away.players[n.player].play_heuristic(sim) if heuristic_player else
                            self.away.players[n.player].play(sim))

    def get_simulator(self, manager: Manager, team: str, mask: Set[Tuple[int, str]]):
        if isinstance(manager.action_strategy, ActionSimulateStrategy):
            return SimulatorActionSimulateManager(self, team, mask)
        if isinstance(manager.action_strategy, ActionMiniMaxStrategy):
            return SimulatorActionMiniMaxManager(self, team, mask)

        return SimulatorRandom(self.game)

    def get_player_simulator(self, team: str, mask: Set[Tuple[int, str]]):
        return SimulatorActionSimulatePlayer(self, team, mask)

    def simulate_managers(self, mask: Set[Tuple[int, str]], heuristic_manager: bool):

        if self.game.instance % INTERVAL_MANGER == 0:
            if not (100, HOME) in mask:
                mask.add((100, HOME))
                sim = self.get_simulator(self.home.manager, HOME, mask)
                self.dispatch.dispatch(self.home.manager.heuristic_action(sim) if heuristic_manager else
                                       self.home.manager.action(sim))

            if not (100, AWAY) in mask:
                mask.add((100, AWAY))
                sim = self.get_simulator(self.away.manager, AWAY, mask)
                self.dispatch.dispatch(self.away.manager.heuristic_action(sim) if heuristic_manager else
                                       self.away.manager.action(sim))

    def simulate_instance(self, mask: Set[Tuple[int, str]], heuristic_manager: bool = False, heuristic_player: bool = False):
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

        self.simulate_players(team, player_with_ball, mask, heuristic_player)
        self.simulate_managers(mask, heuristic_manager)

        if team == HOME:
            self.dispatch.dispatch(IncrementPossession(HOME, self.game))
        if team == AWAY:
            self.dispatch.dispatch(IncrementPossession(AWAY, self.game))

        self.dispatch.dispatch(IncrementInstance(self.game))

    def reset_all(self):
        while self.game.instance != 1:
            self.reset_instance()

    def reset_instance(self):
        self.dispatch.reset()

        while len(self.dispatch.stack) != self.stack[-1]:
            self.dispatch.reset()

        self.stack.pop()


class SimulatorRandom(SimulatorAgent):
    def simulate(self):
        pass

    def reset(self):
        pass

    def simulate_current(self):
        pass

    def reset_current(self):
        pass

    def dispatch(self) -> Dispatch:
        pass


class SimulatorLineUpManager(SimulatorAgent):
    def __init__(self, simulator: Simulator):
        super().__init__(simulator.game)
        self.simulator = simulator

    def simulate(self):
        while not self.game.is_finish():
            self.simulator.simulate_instance(
                set([]), heuristic_manager=True, heuristic_player=True)

    def reset(self):
        self.simulator.reset_all()

    def simulate_current(self):
        return super().simulate_current()

    def reset_current(self):
        return super().reset_current()

    def dispatch(self) -> Dispatch:
        return self.simulator.dispatch


class SimulatorActionSimulateManager(SimulatorAgent):
    def __init__(self, simulator: Simulator, team: str, mask: Set[Tuple[int, str]]):
        super().__init__(simulator.game)
        self.team: str = team
        self.simulator: Simulator = simulator
        self.instance: int = simulator.game.instance
        self.stack_len: int = len(simulator.dispatch.stack)
        self.mask: Set[Tuple[int, str]] = mask

    def simulate(self):
        while not self.simulator.game.is_finish():
            self.simulator.simulate_instance(
                set([]), heuristic_manager=True, heuristic_player=True)

    def reset(self):
        while self.simulator.game.instance != self.instance+1:
            self.simulator.reset_instance()

    def simulate_current(self):
        self.simulator.simulate_instance(
            self.mask.copy(), heuristic_manager=True, heuristic_player=True)

    def reset_current(self):
        while len(self.simulator.dispatch.stack) != self.stack_len:
            self.simulator.dispatch.reset()

    def dispatch(self) -> Dispatch:
        return self.simulator.dispatch


class SimulatorActionSimulatePlayer(SimulatorAgent):
    def __init__(self, simulator: Simulator, team: str, mask: Set[Tuple[int, str]]):
        super().__init__(simulator.game)
        self.team: str = team
        self.simulator: Simulator = simulator
        self.instance: int = simulator.game.instance
        self.stack_len: int = len(simulator.dispatch.stack)
        self.mask: Set[Tuple[int, str]] = mask

    def simulate(self, player: int, just_once: bool = False):
        while not self.simulator.game.is_finish():
            self.simulator.simulate_instance(
                set([(player, self.team)]), heuristic_manager=True, heuristic_player=True)
            if just_once:
                break

    def reset(self):
        while self.simulator.game.instance != self.instance + 1:
            self.simulator.reset_instance()

    def simulate_current(self):
        self.simulator.simulate_instance(
            self.mask.copy(), heuristic_manager=True, heuristic_player=True)

    def reset_current(self):
        while len(self.simulator.dispatch.stack) != self.stack_len:
            self.simulator.dispatch.reset()

    def dispatch(self) -> Dispatch:
        return self.simulator.dispatch


class SimulatorActionMiniMaxManager(SimulatorActionSimulateManager):
    def simulate(self):
        for _ in range(INTERVAL_MANGER):
            self.simulator.simulate_instance(set([(100, HOME), (100, AWAY)]))

    def reset(self):
        for _ in range(INTERVAL_MANGER):
            self.simulator.reset_instance()

    def simulate_current(self):
        mask = self.mask.copy()
        if self.team == HOME:
            mask.add((100, AWAY))
        self.simulator.simulate_instance(
            mask)
