from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from football_agent.behavior import *
from football_agent.fuzzy_rules import fuzzy_defensive_position, fuzzy_ofensive_position
from football_simulator.simulator import SimulatorActionSimulatePlayer
from football_tools.data import StatisticsTeam
from .actions import Action
from football_tools.game import Game, GridField
from football_tools.enum import HOME, AWAY

DEFENSE = 'DEFENSE'
MIDFIELD = 'MIDFIELD'
ATTACK = 'ATTACK'
GOALKEEPER = 'GOALKEEPER'


class PlayerStrategy(ABC):
    def __init__(self) -> None:
        self.strategy = self.select_action
        

    @abstractmethod
    def select_action(self, actions: List[Action], game: Game) -> Action:
        pass
        # return max(actions, key=lambda a: sum([b.eval(a, game) for b in self.behaviors]))
    
class BehaviorStrategy(PlayerStrategy):
    def __init__(self) -> None:
        super().__init__()
        self.behaviors: List[Behavior] = []

    def select_action(self, actions: List[Action], game: Game) -> Action:
        return max(actions, key=lambda a: sum([b.eval(a, game) for b in self.behaviors]))

class FootballStrategy(PlayerStrategy):
    def __init__(self) -> None:
        super().__init__()
        self.defensor = DefensorStrategy()
        self.ofensor = OfensorStrategy()
        self.midfield = MidfielderStrategy()

    def select_action(self, actions: List[Action], game: Game) -> Action:
        player = actions[0].player
        team = actions[0].team
        player_function = game.home.line_up.get_player_function(
            player) if team == 'H' else game.away.line_up.get_player_function(player)
        if player_function == ATTACK:
            return self.ofensor.select_action(actions, game)
        elif player_function == MIDFIELD:
            return self.midfield.select_action(actions, game)
        else:
            return self.defensor.select_action(actions, game)


class RandomStrategy(BehaviorStrategy):
    def __init__(self) -> None:
        super().__init__()
        self.behaviors: List[Behavior] = [Random()]


class DefensorStrategy(BehaviorStrategy):
    def __init__(self) -> None:
        super().__init__()
        self.behaviors: List[Behavior] = [Defensive(importance=0.8),
                                          ReturnToPosition(importance=0.5),
                                          Ofensive(importance=0.2),
                                          Random(importance=0.2),
                                          AvoidFatigue(importance=0.1)]


class OfensorStrategy(BehaviorStrategy):
    def __init__(self) -> None:
        super().__init__()
        self.behaviors: List[Behavior] = [Ofensive(importance=1.8),
                                          ReturnToPosition(importance=0.5),
                                          Defensive(importance=0.2),
                                          Random(importance=0.2),
                                          AvoidFatigue(importance=0.1)]


class MidfielderStrategy(BehaviorStrategy):
    def __init__(self) -> None:
        super().__init__()
        self.behaviors: List[Behavior] = [Ofensive(importance=0.6),
                                          Defensive(importance=0.6),
                                          ReturnToPosition(importance=0.5),
                                          Random(importance=0.2),
                                          AvoidFatigue(importance=0.1),
                                          Random(importance=0.2)]
        
MIN = -10000000000
MAX = 10000000000

CANT_SIMULATIONS = 1
        
class MinimaxStrategy(PlayerStrategy):
    def __init__(self) -> None:
        super().__init__()
        self.evaluator = GameEvaluator()

    def select_action(self, actions: List[Action], simulator: SimulatorActionSimulatePlayer) -> Action:
        team = actions[0].team
        player = actions[0].player
        print(f'{"HOME" if team == HOME else "AWAY"}-{player} player is thinking')

        depth = 2

        simulator.simulate_current()
        action = self.home_function(simulator, depth, MIN, MAX)[1] if team == HOME else self.away_function(
            simulator, depth, MIN, MAX)[1]
        simulator.reset_current()

        return action

    def home_function(self, actions: List[Action], simulator: SimulatorActionSimulatePlayer, 
                      depth: int, alpha: int, beta: int) -> Tuple[int, Action | None]:

        if depth == 0 or simulator.game.is_finish():
            return self.evaluation(simulator.game, HOME)
    
        best = MIN
        best_action = 0

        player = actions[0].player
        simulator.simulate(player)

        for i, action in enumerate(actions):
            simulator.dispatch().dispatch(action)

            r, _ = self.away_function(simulator, depth-1, alpha, beta)

            if r > best:
                best = r
                best_action = i

            simulator.dispatch().reset()

            if best > beta:
                return best, best_action
            
        simulator.reset()

        return best, actions[best_action]

    def away_function(self, actions: List[Action],simulator: SimulatorActionSimulatePlayer, 
                      depth: int, alpha: int, beta: int) -> Tuple[int, Action | None]:
        if depth == 0 or simulator.game.is_finish():
            return self.evaluation(simulator.game, AWAY)

        best = MAX
        best_action = 0

        player = actions[0].player
        simulator.simulate(player)

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
                
        simulator.reset()

        return best, actions[best_action]

    def evaluation(self, game: Game, team: str) -> Tuple[int, Action | None]:
        return self.evaluator.eval(game, team), None


class GameEvaluator:
    def eval(self, game: Game, team: str) -> float:
        ball_position = self.ball_position(game)
        value = (
            (1 if ball_position.team == team else 0) * 0.2 +
            self.team_advantage(game, team) * 0.2 +
            self.controlled_grids(game, team) / 220 * 0.1
        )

        if ball_position.team == team:
            value += (
                self.distance_from_ball_to_enemy_goal(game, team) * 0.1 +
                self.pass_oportunities(game, team) * 0.1 +
                self.avg_ofensive_position(game, team) * 0.3
            )
        else:
            value += (
                self.distance_from_ball_to_self_goal(game, team) * 0.2 +
                self.avg_defensive_position(game, team) * 0.3
            )

        return value

    def controlled_grids(self, game: Game, team: str) -> int:
        controlled_grids = set()

        h = [1, 0, -1]
        v = [1, 0, -1]

        for r in game.field.grid:
            for grid in r:
                if grid.team == team:
                    for i in h:
                        for j in v:
                            x, y = grid
                            x += i
                            y += j
                            if game.field.is_valid_grid((x, y)):
                                controlled_grids.add((x, y))

        return controlled_grids.__sizeof__()

    def ball_position(self, game: Game) -> GridField:
        for r in game.field.grid:
            for grid in r:
                if grid.ball:
                    return grid

    def distance_from_ball_to_self_goal(self, game: Game, team: str) -> float:
        ball = self.ball_position(game)
        if team == HOME:
            return game.field.distance_goal_h((ball.row, ball.col))
        else:
            return game.field.distance_goal_a((ball.row, ball.col))

    def distance_from_ball_to_enemy_goal(self, game: Game, team: str) -> float:
        ball = self.ball_position(game)
        if team == HOME:
            return game.field.distance_goal_a((ball.row, ball.col))
        else:
            return game.field.distance_goal_h((ball.row, ball.col))

    def pass_oportunities(self, game: Game, team: str) -> int:
        count = 0
        ball = self.ball_position(game)
        for r in game.field.grid:
            for grid in r:
                if grid.team == team:
                    if game.field.distance((ball.row, ball.col), (grid.row, grid.col)) <= 3:
                        count += 1
        return count

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
                        (grid.row, grid.col), player_position.row, player_position.col)
                    defensive_positioning.input['distance_to_ball'] = game.field.int_distance(
                        (grid.row, grid.col), self.ball_position(game))
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
                        (grid.row, grid.col), player_position.row, player_position.col)
                    ofensive_positioning.input['distance_to_enemy_goal'] = game.field.int_distance_goal_a(
                        (grid.row, grid.col)) if team == HOME else game.field.int_distance_goal_h((grid.row, grid.col))
                    ofensive_positioning.input['distance_to_ball'] = game.field.int_distance(
                        (grid.row, grid.col), self.ball_position(game))
                    ofensive_positioning.input['player_function'] = player_function

                    ofensive_positioning.compute()
                    avg += ofensive_positioning.output['ofensive_position']
        return avg / 10

    def team_advantage(self, game: Game, team: str) -> float:
        self_data = game.home if team == HOME else game.away
        enemy_data = game.away if team == HOME else game.home

        self_score = self.team_score(self_data.statistics)
        enemy_score = self.team_score(enemy_data.statistics)

        return self_score - enemy_score

    def team_score(self, statistics: StatisticsTeam) -> float:
        weights: Dict[str, float] = {
            'goal': 1,
            'possession': 0.2,
            'shoots': 0.1,
            'passes': 0.01,
            'fouls': 0.1,
            'yellow_cards': 0.15,
            'red_cards': 0.5
        }

        score = (
            statistics.goals * weights['goals'] +
            statistics.possession_instances * weights['possession'] +
            statistics.shots * weights['shots'] +
            statistics.passes_completed * weights['passes'] -
            statistics.fouls * weights['fouls'] -
            statistics.yellow_cards * weights['yellow_cards'] -
            statistics.red_cards * weights['red_cards']
        )

        return score
