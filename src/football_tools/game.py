from typing import List, Tuple
import math
from numpy import double
from .data import HOME, AWAY, TeamData


class GridField:
    def __init__(self, row: int, col: int, player: int = -1, ball: bool = False, team: str = '') -> None:
        self.row: int = row
        self.col: int = col
        self.ball: bool = ball
        self.player: int = player
        self.team: str = team

    def is_empty(self) -> bool:
        return self.player == -1

    def __str__(self) -> str:
        if self.player == - 1:
            return '\033[32m**  \033[0m'
        return f'\033{"[34m"if self.team==HOME else"[31m"}{f"0"  if self.player < 10 else ""}{self.player}\033[0m{"⚽" if self.ball else "  "}'

    def __eq__(self, __value: object) -> bool:
        return self.row == __value.row and self.col == __value.col


class Field:
    def __init__(self, rows: int = 20, columns: int = 11):
        self.rows = rows
        self.columns = columns
        self.grid: List[List[GridField]] = [
            [GridField(r, c) for c in range(columns)] for r in range(rows)]
        self.goal_a = [(0, columns // 2-1), (0, columns // 2),
                       (0, columns // 2 + 1)]
        self.goal_h = [(rows - 1, columns // 2 - 1),
                       (rows - 1, columns // 2), (rows - 1, columns // 2 + 1)]

    def conf_line_ups(self, line_up_h: List[Tuple[int, int, int]], line_up_a: List[Tuple[int, int, int]]):
        for d, r, c in line_up_h:
            self.grid[r][c].player = d
            self.grid[r][c].team = HOME
        for d, r, c in line_up_a:
            self.grid[r][c].player = d
            self.grid[r][c].team = AWAY

        _, r, c = line_up_a[-1]
        self.grid[r][c].ball = True

    def move_ball(self, src: Tuple[int, int], dest: Tuple[int, int]):
        x, y = src
        if self.grid[x][y].ball:
            self.grid[x][y].ball = False
            x, y = dest
            self.grid[x][y].ball = True
        else:
            raise Exception("The ball is not in the source position")

    def move_player(self, src: Tuple[int, int], dest: Tuple[int, int]):
        x, y = src
        if self.grid[x][y].player == -1:
            raise Exception("The player is not in teh source position")
        else:
            team = self.grid[x][y].team
            player = self.grid[x][y].player
            self.grid[x][y].player = -1
            self.grid[x][y].team = ''
            x, y = dest
            self.grid[x][y].player = player
            self.grid[x][y].team = team

    @staticmethod
    def distance(src: Tuple[int, int], dest: Tuple[int, int]):
        xs, ys = src
        xd, yd = dest

        return math.sqrt((xs-xd)**2+(ys-yd)**2)

    def distance_goal_h(self, src: Tuple[int, int]):
        return min(Field.distance(d, src) for d in self.goal_h)

    def distance_goal_a(self, src: Tuple[int, int]):
        return min(Field.distance(d, src) for d in self.goal_a)

    def find_player(self, dorsal: int, team: str) -> GridField:
        for row in self.grid:
            for grid in row:
                if grid.player == dorsal and grid.team == team:
                    return grid
        raise Exception(
            f"There is no player with the dorsal {dorsal} of the {team} team on the field")

    def neighbor_grids(self, src: GridField, max_distance: double) -> List[GridField]:
        x, y = (src.row, src.col)
        grids: List[GridField] = []
        for row in self.grid:
            for grid in row:
                distance = self.distance((x, y), (grid.row, grid.col))
                if distance <= max_distance:
                    grids.append(grid)
        return grids

    def self_goal(self, team: str) -> List[Tuple[int, int]]:
        if team == HOME:
            return self.goal_h
        else:
            return self.goal_a

    def enemy_goal(self, team: str) -> List[Tuple[int, int]]:
        if team == HOME:
            return self.goal_a
        else:
            return self.goal_h

    def __str__(self) -> str:
        field_str = ""
        for r in range(self.rows):
            for c in range(self.columns):
                field_str += str(self.grid[r][c])+' '
            field_str += "\n"
        return field_str


class Game:
    def __init__(self, home: TeamData, away: TeamData):
        self.field: Field = Field()
        self.home: TeamData = home
        self.away: TeamData = away
        self.field.conf_line_ups(home.line_up, away.line_up)
