from typing import List, Dict
from .player_data import PlayerData
from football_agent.team import Team


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
        self.team_name: str = team
        self.goals: int = 0
        self.possession_instances: int = 0
        self.shots: int = 0
        self.fouls: int = 0
        self.passes_completed: int = 0
        self.yellow_cards: int = 0
        self.red_cards: int = 0
        self.lineup: List[str] = []


class GameData:
    def __init__(self, home: Team, away: Team) -> None:
        self.home = home
        self.away = away
        self.home_statistics = StatisticsTeam(home.name)
        self.away_statistics = StatisticsTeam(away.name)
        self.home_players_statistics: Dict[int, StatisticsPLayer] = {}
        self.away_players_statistics: Dict[int, StatisticsPLayer] = {}
        self.home_players_data: Dict[int, PlayerData] = {}
        self.away_players_data: Dict[int, PlayerData] = {}

        for player in home.players:
            self.home_players_statistics[player.dorsal] = StatisticsPLayer()
            self.home_players_data[player.dorsal] = player
        for player in away.players:
            self.away_players_statistics[player.dorsal] = StatisticsPLayer()
            self.away_players_data[player.dorsal] = player
