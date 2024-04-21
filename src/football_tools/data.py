from typing import List, Dict, Tuple
from pandas import DataFrame
from typing import List,  Dict

AWAY = 'A'
HOME = 'H'


class PlayerData():
    def __init__(self, df: DataFrame):
        self.short_name: str = df['short_name']
        self.club_name: str = df['club_name']
        self.player_positions: str = df['player_positions']
        self.overall: int = df['overall']
        self.pace: int = df['pace']
        self.shooting: int = df['shooting']
        self.passing: int = df['passing']
        self.dribbling: int = df['dribbling']
        self.defending: int = df['defending']
        self.physic: int = df['physic']
        self.attacking_finishing: int = df['attacking_finishing']
        self.mentality_vision: int = df['mentality_vision']
        self.power_stamina: int = df['power_stamina']*2
        self.mentality_aggression: int = df['mentality_aggression']
        self.mentality_interceptions: int = df['mentality_interceptions']
        self.movement_reactions: int = df['movement_reactions']
        self.dorsal: int = df['club_jersey_number']
        self.goal_keep_diving: int = df['goalkeeping_diving']
        self.goal_keep_reflexes: int = df['goalkeeping_reflexes']
        self.skill_ball_control: int = df['skill_ball_control']

        self.o_short_name: str = df['short_name']
        self.o_club_name: str = df['club_name']
        self.o_player_positions: str = df['player_positions']
        self.o_overall: int = df['overall']
        self.o_pace: int = df['pace']
        self.o_shooting: int = df['shooting']
        self.o_passing: int = df['passing']
        self.o_dribbling: int = df['dribbling']
        self.o_defending: int = df['defending']
        self.o_physic: int = df['physic']
        self.o_attacking_finishing: int = df['attacking_finishing']
        self.o_mentality_vision: int = df['mentality_vision']
        self.o_power_stamina: int = df['power_stamina']*2
        self.o_mentality_aggression: int = df['mentality_aggression']
        self.o_mentality_interceptions: int = df['mentality_interceptions']
        self.o_movement_reactions: int = df['movement_reactions']
        self.o_dorsal: int = df['club_jersey_number']
        self.o_goal_keep_diving: int = df['goalkeeping_diving']
        self.o_goal_keep_reflexes: int = df['goalkeeping_reflexes']
        self.o_skill_ball_control: int = df['skill_ball_control']


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


class TeamData:
    def __init__(self, name: str, line_up: List[Tuple[int, int, int]], data: List[PlayerData]) -> None:
        self.name = name
        self.line_up: List[Tuple[int, int, int]] = line_up
        self.data: Dict[int, PlayerData] = {}
        self.statistics: StatisticsTeam = StatisticsTeam(name)
        self.players_statistics: Dict[int, StatisticsPLayer] = {}

        for player in data:
            self.players_statistics[player.dorsal] = StatisticsPLayer()
            self.data[player.dorsal] = player
