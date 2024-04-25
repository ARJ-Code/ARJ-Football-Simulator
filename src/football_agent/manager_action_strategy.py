from abc import ABC, abstractmethod
from typing import List, Set
from random import choice
from .simulator_agent import SimulatorAgent
from football_tools.game import Game
from .actions import *

HOME = 'H'
AWAY = 'A'


def possibles_change_player(game: Game, team: str) -> List[Action]:
    possibles = []

    team_data = game.home if team == HOME else game.away

    # if len(in_players) == 5:
    #     return []

    for k, v in team_data.line_up.line_up.items():
        if v.player in team_data.out_players:
            continue
        for player in team_data.on_bench:
            if player in team_data.in_players:
                continue
            for pos in team_data.data[player].player_positions:
                if pos in k:
                    possibles.append(ChangePlayer(
                        v.player, player, team, game))

    return possibles


class ManagerActionStrategy(ABC):
    @abstractmethod
    def action(self, team: str, in_players: Set[int], out_players: Set[int], simulator: SimulatorAgent) -> Action:
        pass


class ActionRandomStrategy(ManagerActionStrategy):
    def action(self, team: str,  simulator: SimulatorAgent) -> Action:
        action = choice(possibles_change_player(
            simulator.game, team,)+[Nothing()])

        if isinstance(action, ChangePlayer):
            team_data = simulator.game.home if team == HOME else simulator.game.away

            team_data.in_players.add(action.new_player)
            team_data.out_players.add(action.player)

        return action
