from .football_agent import *
from typing import List, Tuple, Dict
import math
from numpy import double


class GridField:
    def __init__(self, row: int, col: int, player: int, ball: bool = False, team: str = '') -> None:
        self.row: int = row
        self.col: int = col
        self.ball: bool = ball
        self.player: int = player
        self.is_empty: bool = player == -1
        self.team: str = team

    def __str__(self) -> str:
        if self.player -1:
            return '   '
        return f'{f"0"  if self.player < 10 else ""}{self.player}-{self.team}'

class Field:
    def __init__(self, rows: int = 20, columns: int = 13):
        self.rows = rows
        self.columns = columns
        self.grid: List[List[GridField]] = [
            [GridField(r, c, False) for r in range(columns)] for c in range(rows)]
        self.goal_a = [(0, columns // 2-1), (0, columns // 2),
                       (0, columns // 2 + 1)]
        self.goal_b = [(rows - 1, columns // 2 - 1),
                       (rows - 1, columns // 2), (rows - 1, columns // 2 + 1)]

    # def conf_teams(self, team_a: Team, team_b: Team):
    #     for d, r, c in team_a.line_up:
    #         self.grid[r][c].player = team_a.dorsal_to_player[d]
    #     for d, r, c in team_b.line_up:
    #         self.grid[r][c].player = team_a.dorsal_to_player[d]

    def move_ball(self, src: Tuple[int, int], dest: Tuple[int, int]):
        x, y = src
        if self.grid[x][y]:
            self.grid[x][y] = False
            x, y = dest
            self.grid[x][y] = True
        else:
            raise Exception("The ball is not in the source position")
        
    def move_player(self, src: Tuple[int, int], dest: Tuple[int, int], player: int):
        x, y = src
        if self.grid[x][y].player is None:
            raise Exception("The player is not in the source position")
        else:
            self.grid[x][y].player = None
            x, y = dest
            self.grid[x][y].player = player

    @staticmethod
    def distance(src: Tuple[int, int], dest: Tuple[int, int]):
        xs, ys = src
        xd, yd = dest

        return math.sqrt((xs-xd)**2+(ys-yd)**2)

    def distance_goal_a(self, src: Tuple[int, int]):
        return min(Field.distance(d, src) for d in self.goal_a)

    def distance_goal_b(self, src: Tuple[int, int]):
        return min(Field.distance(d, src) for d in self.goal_b)
    
    def find_player(self, dorsal: int, team: str) -> Tuple[int, int]:
        for row in self.grid:
            for grid in row:
                if grid.player == dorsal and grid.team == team:
                    return grid.row, grid.col
        raise Exception(f"There is no player with the dorsal {dorsal} of the {team} team on the field")

    def neighbor_grids(self, src: Tuple[int, int], max_distance: double) -> List[Tuple[GridField, double]]:
        x, y = src
        grids: List[Tuple[GridField, double]] = []
        for row in self.grid:
            for grid in row:
                distance = self.distance((x, y), (grid.row, grid.col))
                if distance <= max_distance:
                    grids.append(grid, distance)
        return grids
    
    def contigous_grids(self, f: Tuple[int, int], s: Tuple[int, int]) -> bool:
        return abs(f[0] - s[0]) == 1 or abs(f[1] - s[1]) == 1
    
    def friendly_grid(self, team: str, g: Tuple[int, int]) -> bool:
        x, y = g
        return self.grid[x][y].team == team


    def __str__(self) -> str:
        field_str = ""
        for r in range(self.rows):
            for c in range(self.columns):
                field_str += str(self.grid[r][c])
            field_str += "\n"
        return field_str


class Game:
    def __init__(self, home: Tuple[str, List[int]], visitor: Tuple[str, List[int]]):
        self.home = home
        self.visitor = visitor
        self.field: Field = Field()
