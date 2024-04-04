from typing import List

from simulation_tools.team import Team


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
    def __init__(self, home: Team, visitor: Team) -> None:
        self.home = home
        self.visitor = visitor
        self.home_statistics = StatisticsTeam(home.name)
        self.visitor_statistics = StatisticsTeam(visitor.name)
        self.home_players_statistics: {int, StatisticsPLayer} = {}
        self.visitor_players_statistics: {int, StatisticsPLayer} = {}

        for player in home.players:
            self.home_players_statistics[player.dorsal] = StatisticsPLayer()
        for player in visitor.players:
            self.visitor_players_statistics[player.dorsal] = StatisticsPLayer()