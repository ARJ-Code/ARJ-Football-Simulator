from .football_agent import *
from typing import List, Tuple, Dict

A = 'A'
B = 'B'


class Team:
    def __init__(self, manager: Manager, players: List[Player]) -> None:
        self.manager: Manager = manager
        self.line_up: List[Tuple[int, int, int]] = []
        self.players: List[Player] = players
        self.dorsal_to_player: Dict[int, Player] = {}

        for p in players:
            self.dorsal_to_player[p.data.dorsal] = p

    def conf_line_up(self, line_up: List[Tuple[int, int, int]]):
        self.line_up = line_up


class GridFiled:
    def __init__(self, row: int, col: int, ball: bool = False, player: Player | None = None, team: str | None = None) -> None:
        self.row: int = row
        self.col: int = col
        self.ball: bool = ball
        self.player: Player | None = player
        self.is_empty: bool = player is None
        self.team: str | None = team

    def __str__(self) -> str:
        if self.player is None:
            return '   '
        return f'{f"0"  if self.player.dorsal<10 else ""}{self.player.dorsal}-{self.team}'


class Field:
    def __init__(self, rows: int = 20, columns: int = 13):
        self.rows = rows
        self.columns = columns
        self.grid: List[List[GridFiled]] = [
            [GridFiled(r, c, False) for r in range(columns)] for c in range(rows)]
        self.goal_A = [(0, columns // 2), (0, columns // 2 + 1)]
        self.goal_B = [(rows - 1, columns // 2), (rows - 1, columns // 2 - 1),
                       (rows - 1, columns // 2 + 2), (rows - 1, columns // 2 + 1)]

    def conf_teams(self, team_a: Team, team_b: Team):
        for d, r, c in team_a.line_up:
            self.grid[r][c].player = team_a.dorsal_to_player[d]
        for d, r, c in team_b.line_up:
            self.grid[r][c].player = team_a.dorsal_to_player[d]

    def move_ball(self, src: Tuple[int, int], dest: Tuple[int, int]):
        x, y = src
        if self.grid[x, y]:
            self.grid[x, y] = False
            x, y = dest
            self.grid[x, y] = True
        else:
            raise Exception("The ball is not in the source position")
        
    def move_player(self, src: Tuple[int, int], dest: Tuple[int, int], player: Player):
        x, y = src
        if self.grid[x, y].player is None:
            raise Exception("The player is not in teh source position")
        else:
            self.grid[x, y].player = None
            x, y = dest
            self.grid[x, y].player = player

    def __str__(self) -> str:
        field_str = ""
        for r in range(self.rows):
            for c in range(self.columns):
                field_str += str(self.grid[r][c])
            field_str += "\n"
        return field_str


class StatisticsPLayer:
    def __init__(self, dorsal: int, team: str):
        self.team: str = team
        self.dorsal: int = dorsal
        self.goals: int = 0
        self.passes: int = 0
        self.shots: int = 0
        self.saves: int = 0
        self.fouls: int = 0
        self.red_cards: int = 0
        self.yellow_cards: int = 0
        self.minutes_played: int = 0


class StatisticsTeam:
    def __init__(self, team: str):
        self.team_name: str = team
        self.goals: int = 0
        self.possession_instances: int = 0
        self.shots: int = 0
        self.fouls: int = 0
        self.passes_completed: int = 0
        self.yellow_cards: int = 0
        self.red_cards: int = 0
        self.lineup: List[str]


class Game:
    def __init__(self, team_a: Team, team_b: Team):
        self.team_a: Team = team_a
        self.team_b: Team = team_b
        self.field: Field = Field()
        self.statistics: Dict[int, StatisticsPLayer] = {}
        self.statistics_team_a: StatisticsTeam = StatisticsTeam(A)
        self.statistics_team_b: StatisticsTeam = StatisticsTeam(B)
        self.current_round: int = 0

        for p in team_a.players:
            self.statistics[p.data.dorsal] = StatisticsPLayer(p.data.dorsal)
