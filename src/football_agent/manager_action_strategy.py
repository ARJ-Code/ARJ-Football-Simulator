from abc import ABC, abstractmethod
from typing import List, Set
from random import choice

from football_agent.actions import Action
from .simulator_agent import SimulatorAgent
from football_tools.game import Game
from .actions import *
from .manager_line_up_strategy import possibles_line_up

HOME = 'H'
AWAY = 'A'


def possibles_change_player(game: Game, team: str) -> List[Action]:
    possibles = []

    team_data = game.home if team == HOME else game.away

    if len(team_data.change_history) == 5:
        return []

    for k, v in team_data.line_up.line_up.items():
        if any([p for p in team_data.change_history if p[0] == v.player]) or v.player in team_data.unavailable:
            continue

        q = []

        for player in team_data.on_bench:
            if any([p for p in team_data.change_history if p[1] == player]):
                continue
            for pos in team_data.data[player].player_positions:
                if pos in k:
                    aux = v.player
                    v.conf_player(team_data.data[player])
                    q.append((team_data.data[player].overall, player))
                    v.conf_player(team_data.data[aux])
                    break

        if len(q) == 0:
            continue
        possibles.append(ChangePlayer(v.player, max(
            q, key=lambda x: x[0])[1], team, game))

    return possibles


def possibles_action(game: Game, team: str) -> List[Action]:
    change_options = possibles_change_player(
        game, team)

    team_data = game.home if team == HOME else game.away

    def get_player(player: int):
        for p in team_data.change_history:
            if p[0] == player:
                return p[1]

        return player

    line_up_players = [team_data.data[get_player(p.player)]
                       for p in team_data.line_up.line_up.values()]

    line_up_options = [ChangeLineUp(team, game, l)
                       for l in possibles_line_up(line_up_players, team)]

    return change_options+line_up_options+[Nothing()]


class ManagerActionStrategy(ABC):
    @abstractmethod
    def action(self, team: str, simulator: SimulatorAgent) -> Action:
        pass


class ActionRandomStrategy(ManagerActionStrategy):
    def action(self, team: str,  simulator: SimulatorAgent) -> Action:
        return choice(possibles_action(simulator.game, team))


class ActionSimulateStrategy(ManagerActionStrategy):
    def action(self, team: str, simulator: SimulatorAgent) -> Action:
        actions = possibles_action(simulator.game, team)

        results = {i: (0, 0) for i, _ in enumerate(actions)}

        for i, action in enumerate(actions):
            simulator.dispatch().dispatch(action)
            simulator.simulate_current()
            simulator.simulate()

            r = simulator.game.home.statistics.goals-simulator.game.away.statistics.goals
            if team == AWAY:
                r = -r

            c, g = results[i]

            if r > 0:
                c += 1

            results[i] = (c, g+r)

            simulator.reset()
            simulator.reset_current()

        action, _ = max(results.items(), key=lambda x: x[1][0]*1000+x[1][1])

        return actions[action]
