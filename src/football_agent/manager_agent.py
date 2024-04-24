from typing import List, Callable
from football_tools.line_up import LineUp
from football_tools.player_data import PlayerData
from .player_agent import Player
from .manager_strategy import ManagerStrategy
from football_tools.line_up import *
from football_tools.data import HOME
from .simulator_agent import SimulatorAgent

import random


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


class Manager:
    def __init__(self, strategy: ManagerStrategy, team: str, players: List[PlayerData]) -> None:
        self.strategy: ManagerStrategy = strategy
        self.team: str = team
        self.players: List[Player] = players

    def get_line_up(self, simulator: SimulatorAgent) -> LineUp:
        return self.strategy.get_line_up(self.team, possibles_line_up(self.players, self.team), simulator)
