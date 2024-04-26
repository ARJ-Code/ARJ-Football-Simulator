from .player_data import PlayerData
from .line_up import LineUp
from typing import List, Dict, Set, Tuple

AWAY = 'A'
HOME = 'H'


class StatisticsPLayer:
    def __init__(self):
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
        self.changes: int = 0
        self.team_name: str = team
        self.goals: int = 0
        self.possession_instances: int = 0
        self.shots: int = 0
        self.fouls: int = 0
        self.passes_completed: int = 0
        self.yellow_cards: int = 0
        self.red_cards: int = 0
        self.lineup: List[str] = []


class TeamData:
    def __init__(self, name: str, data: List[PlayerData]) -> None:
        self.name = name
        self.line_up: LineUp = None
        self.data: Dict[int, PlayerData] = {}
        self.statistics: StatisticsTeam = StatisticsTeam(name)
        self.players_statistics: Dict[int, StatisticsPLayer] = {}

        self.on_field: Set[int] = set([])
        self.on_bench: Set[int] = set([])
        self.unavailable: Set[int] = set([])

        self.change_history: List[Tuple[int]] = []

        for player in data:
            self.players_statistics[player.dorsal] = StatisticsPLayer()
            self.data[player.dorsal] = player

    def reset(self):
        self.statistics = StatisticsTeam(self.name)
        for player in self.data.keys():
            self.players_statistics[player] = StatisticsPLayer()
