from numpy import double, random
from football_tools.game import Game, GridField
from .actions import Action, Dribble, Move, Nothing, Pass, Shoot, StealBall

HOME = 'HOME'

class Behavior:
    def __init__(self, importance: double = 1) -> None:
        self.importance = importance

    def eval(self, action: Action, game: Game) -> double:
        pass

    def change_importance(self, importance: double) -> None:
        self.importance = importance

class Random(Behavior):
    def eval(self, action: Action, game: Game) -> double:
        return random.rand() * self.importance
    
class ReturnToPosition(Behavior):
    def eval(self, action: Action, game: Game) -> double:
        team = game.home if action.team == HOME else game.away
        line_up_position = team.line_up.get_player_position(action.player)
        line_up_position = (line_up_position.row, line_up_position.col)
        source = action.src
        destination = action.dest

        if action is Move:
            return (1 if game.field.distance(destination, line_up_position) < game.field.distance(source, line_up_position) else 0) \
                * self.importance
        else: 
            return 0

class Defensive(Behavior):
    def eval(self, action: Action, game: Game) -> double:
        source = action.src
        destination = action.dest
        ball_position = game.field.find_ball()
        self_goal = game.field.goal_h if action.team == HOME else game.field.goal_a

        value = 0

        if ball_position.team == action.team:
            if action is not Nothing:
                neighbor_enemies = 0
                x, y = destination
                dest_grid: GridField = GridField(x, y, -1, False, '')
                for grid in game.field.neighbor_grids(dest_grid, 2):
                    if grid.team != action.team:
                        neighbor_enemies += 1

                value += 1 / (neighbor_enemies + 1)
        else:
            if action is Move:
                move_value = 0
                if game.field.distance(destination, self_goal[1]) < game.field.distance(source, self_goal[1]):
                    move_value += 1 / 3
                b_x, b_y = ball_position.row, ball_position.col
                if game.field.distance(destination, (b_x, b_y)) < game.field.distance(source, (b_x, b_y)):
                    move_value += 2 / 3
                value = move_value
            if action is StealBall:
                value = 1

        return value * self.importance

class Ofensive(Behavior):
    def eval(self, action: Action, game: Game) -> double:
        source = action.src
        destination = action.dest
        ball_position = game.field.find_ball()
        enemy_goal = game.field.goal_h if action.team != HOME else game.field.goal_a

        value = 0

        if ball_position.team == action.team:
            if action is Move:
                move_value = 0
                if game.field.distance(destination, enemy_goal[1]) < game.field.distance(source, enemy_goal[1]):
                    move_value += 1 / 2
                    x, y = destination
                    dest_grid: GridField = GridField(x, y, -1, False, '')
                    if action is Dribble and any(g.team != action.team for g in game.field.neighbor_grids(dest_grid, 1)):
                        move_value += 1 / 4
            if action is Shoot:
                value += 1
            if action is Pass:
                diff_distance = game.field.distance(source, enemy_goal[1]) - game.field.distance(destination, enemy_goal[1])
                if diff_distance > 0:
                    value += 1 - 1 / (diff_distance + 1)
        # else:
        #     if action is Move:
        #         move_value = 0
        #         if game.field.distance(destination, enemy_goal[1]) < game.field.distance(source, enemy_goal[1]):
        #             move_value += 1 / 3
        #         b_x, b_y = ball_position.row, ball_position.col
        #         if game.field.distance(destination, (b_x, b_y)) < game.field.distance(source, (b_x, b_y)):
        #             move_value += 2 / 3
        #         value = move_value
        #     if action is StealBall:
        #         value = 1

        return value * self.importance

