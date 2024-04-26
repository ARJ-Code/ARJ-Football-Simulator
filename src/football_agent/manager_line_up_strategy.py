from typing import List
from abc import ABC, abstractmethod
from random import choice
from .actions import *
from football_tools.line_up import *
from football_tools.game import Game
from .simulator_agent import SimulatorAgent
import random

HOME = 'H'
AWAY = 'A'


def players_by_position(players: List[PlayerData], line_up_grid: LineUpGrid) -> List[PlayerData]:
    r = []

    for player in players:
        for p in player.player_positions:
            if p in line_up_grid.position:
                line_up_grid.set_statistics(player)
                r.append(player)

    r.sort(key=lambda x: x.overall)
    return r


def possibles_conf_line_up(players: List[PlayerData], line_up: LineUp):
    players_d = {k: players_by_position(
        players, v) for k, v in line_up.line_up.items()}

    line_up_d = {}
    mask = set([])

    for k, v in players_d.items():
        while len(v) > 0:
            player = v.pop()

            if player.dorsal not in mask:
                line_up_d[k] = player
                mask.add(player.dorsal)
                break

    available = [p for p in players if p.dorsal not in mask]
    available.sort(key=lambda _: random.random())

    for k in players_d.keys():
        if k not in line_up_d.keys():
            line_up_d[k] = available.pop()

    line_up.conf_players(line_up_d)


def possibles_line_up(players: List[PlayerData], team: str) -> List[LineUp]:
    possibles: List[LineUp] = [Home343(), Home433(), Home442(), Home532(
    )] if team == HOME else [Away343(), Away433(), Away442(), Away532()]

    for p in possibles:
        possibles_conf_line_up(players, p)

    return possibles


class ManagerLineUpStrategy(ABC):
    @abstractmethod
    def get_line_up(self, team: str, simulator: SimulatorAgent) -> LineUp:
        pass


class LineUpRandomStrategy(ManagerLineUpStrategy):
    def get_line_up(self, team: str, simulator: SimulatorAgent) -> LineUp:
        return choice(possibles_line_up(simulator.game.home.data.values(), HOME) if team == HOME else possibles_line_up(simulator.game.away.data.values(), AWAY))

    def action(self, game: Game) -> Action:
        return super().action(game)


class LineUpSimulateStrategy(ManagerLineUpStrategy):
    def get_line_up(self, team: str,  simulator: SimulatorAgent) -> LineUp:
        home_line_ups = possibles_line_up(
            simulator.game.home.data.values(), HOME)[:1]
        away_line_ups = possibles_line_up(
            simulator.game.away.data.values(), AWAY)[:1]

        results = []

        for i, home in enumerate(home_line_ups):
            for j, away in enumerate(away_line_ups):
                simulator.game.instance = 0
                simulator.game.conf_line_ups(home, away)
                simulator.game.instance = 1

                simulator.simulate()

                results.append((i, j, simulator.game.home.statistics.goals,
                                simulator.game.away.statistics.goals))

                simulator.reset()
                simulator.game.reset()

        results_by_sim = {}

        for i, j, _, _ in results:
            results_by_sim[i if team == HOME else j] = (0, 0)

        for i, j, h, a in results:
            r = h-a if team == HOME else a-h

            c, g = results_by_sim[i if team == HOME else j]
            results_by_sim[i if team == HOME else j] = (
                c+(1 if r > 0 else 0), g + r)

        ind, _ = max(results_by_sim.items(), key=lambda x: x[1][0]*1000+x[1][1])

        return home_line_ups[ind] if team == HOME else away_line_ups[ind]

    def action(self, game: Game) -> Action:
        return super().action(game)
