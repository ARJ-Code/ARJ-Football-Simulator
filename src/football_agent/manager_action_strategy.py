from abc import ABC, abstractmethod
from typing import List, Tuple
from random import choice

from football_agent.actions import Action, ReorganizeField
from football_agent.fuzzy_rules import fuzzy_defensive_position, fuzzy_ofensive_position
from .simulator_agent import SimulatorAgent
from football_tools.game import Game, GridField
from .actions import *
from .manager_line_up_strategy import possibles_line_up
from football_tools.enum import HOME, AWAY

DEFENSE = 'DEFENSE'
MIDFIELD = 'MIDFIELD'
ATTACK = 'ATTACK'
GOALKEEPER = 'GOALKEEPER'

MIN = -10000000000
MAX = 10000000000

CANT_SIMULATIONS = 10


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

    return change_options+line_up_options+[ManagerNothing()]


class ManagerActionStrategy(ABC):
    @abstractmethod
    def action(self, team: str, simulator: SimulatorAgent) -> Action:
        pass


class ActionRandomStrategy(ManagerActionStrategy):
    def action(self, team: str,  simulator: SimulatorAgent) -> Action:
        return choice(possibles_action(simulator.game, team))


class ActionSimulateStrategy(ManagerActionStrategy):
    def action(self, team: str, simulator: SimulatorAgent) -> Action:
        print(f'{"HOME" if team ==HOME else "AWAY"} manager is thinking')

        actions = possibles_action(simulator.game, team)

        results = {i: (0, 0) for i, _ in enumerate(actions)}

        for i, action in enumerate(actions):
            for _ in range(CANT_SIMULATIONS):
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


class ActionMiniMaxStrategy(ManagerActionStrategy):
    def action(self, team: str, simulator: SimulatorAgent) -> Action:
        print(f'{"HOME" if team ==HOME else "AWAY"} manager is thinking')

        depth = 2

        simulator.simulate_current()
        action = self.home_function(simulator, depth, MIN, MAX)[1] if team == HOME else self.away_function(
            simulator, depth, MIN, MAX)[1]
        simulator.reset_current()

        return action

    def home_function(self, simulator: SimulatorAgent, depth: int, alpha: int, beta: int) -> Tuple[int, Action | None]:

        if depth == 0 or simulator.game.is_finish():
            return self.evaluation(simulator)

        best = MIN
        best_action = 0

        actions = possibles_action(simulator.game, HOME)

        for i, action in enumerate(actions):
            simulator.dispatch().dispatch(action)

            r, _ = self.away_function(simulator, depth-1, alpha, beta)

            if r > best:
                best = r
                best_action = i

            simulator.dispatch().reset()

            if best > beta:
                return best, best_action

        return best, actions[best_action]

    def away_function(self, simulator: SimulatorAgent, depth: int, alpha: int, beta: int) -> Tuple[int, Action | None]:
        if depth == 0 or simulator.game.is_finish():
            return self.evaluation(simulator)

        best = MAX
        best_action = 0

        actions = possibles_action(simulator.game, AWAY)

        for i, action in enumerate(actions):
            for _ in range(CANT_SIMULATIONS):
                simulator.dispatch().dispatch(action)
                simulator.simulate()

                r, _ = self.home_function(simulator, depth-1, alpha, beta)

                if r < best:
                    best = r
                    best_action = i

                simulator.reset()
                simulator.dispatch().reset()

                if best < alpha:
                    return best, best_action

        return best, actions[best_action]

    def evaluation(self, simulator: SimulatorAgent) -> Tuple[int, Action | None]:
        game = simulator.game
        team_with_ball = ''

        for l in game.field.grid:
            for n in l:
                if n.ball:
                    team_with_ball = n.team
                    break

        simulator.dispatch().dispatch(ReorganizeField(game, team_with_ball))

        value = ManagerGameEvaluator().eval(
            game, HOME)-ManagerGameEvaluator().eval(game, AWAY)
        simulator.dispatch().reset()
        simulator.dispatch().reset()

        return value, None


class ManagerGameEvaluator:
    def eval(self, game: Game, team: str) -> float:
        ofensive_importance = 0
        defensive_importance = 0
        goals_diff = game.home.statistics.goals-game.away.statistics.goals

        if team == HOME:
            if goals_diff < 0:
                ofensive_importance = 0.6
            elif goals_diff == 0:
                ofensive_importance = 0.5
            else:
                ofensive_importance = 0.4
        else:
            if goals_diff < 0:
                ofensive_importance = 0.4
            elif goals_diff == 0:
                ofensive_importance = 0.5
            else:
                ofensive_importance = 0.6

        defensive_importance = 1 - ofensive_importance

        value = 0

        value += self.avg_defensive_position(game, team) * defensive_importance
        value += self.avg_ofensive_position(game, team) * ofensive_importance

        return value

    def ball_position(self, game: Game) -> GridField:
        for r in game.field.grid:
            for grid in r:
                if grid.ball:
                    return grid

    def avg_defensive_position(self, game: Game, team: str) -> float:
        defensive_positioning = fuzzy_defensive_position()
        avg = 0
        for r in game.field.grid:
            for grid in r:
                if grid.team == team:
                    team_data = game.home if team == HOME else game.away
                    player_position = team_data.line_up.get_player_position(
                        grid.player)
                    player_function = 0 if player_position.player_function == DEFENSE else 1 if player_position.player_function == MIDFIELD else 2

                    defensive_positioning.input['distance_to_position'] = game.field.int_distance(
                        (grid.row, grid.col), (player_position.row, player_position.col))
                    ball = self.ball_position(game)
                    defensive_positioning.input['distance_to_ball'] = game.field.int_distance(
                        (grid.row, grid.col), (ball.row, ball.col))
                    defensive_positioning.input['player_function'] = player_function

                    defensive_positioning.compute()
                    avg += defensive_positioning.output['defensive_position']
        return avg / 10

    def avg_ofensive_position(self, game: Game, team: str) -> float:
        ofensive_positioning = fuzzy_ofensive_position()
        avg = 0
        for r in game.field.grid:
            for grid in r:
                if grid.team == team:
                    team_data = game.home if team == HOME else game.away
                    player_position = team_data.line_up.get_player_position(
                        grid.player)
                    player_function = 0 if player_position.player_function == DEFENSE else 1 if player_position.player_function == MIDFIELD else 2
                    ofensive_positioning.input['distance_to_position'] = game.field.int_distance(
                        (grid.row, grid.col), (player_position.row, player_position.col))
                    ofensive_positioning.input['distance_to_enemy_goal'] = game.field.int_distance_goal_a(
                        (grid.row, grid.col)) if team == HOME else game.field.int_distance_goal_h((grid.row, grid.col))
                    ball = self.ball_position(game)
                    ofensive_positioning.input['distance_to_ball'] = game.field.int_distance(
                        (grid.row, grid.col), (ball.row, ball.col))
                    ofensive_positioning.input['player_function'] = player_function

                    ofensive_positioning.compute()
                    avg += ofensive_positioning.output['ofensive_position']
        return avg / 10
