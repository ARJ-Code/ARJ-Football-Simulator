from pandas import DataFrame


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
        self.power_stamina: int = df['power_stamina']
        self.mentality_aggression: int = df['mentality_aggression']
        self.mentality_interceptions: int = df['mentality_interceptions']
        self.movement_reactions: int = df['movement_reactions']
        self.dorsal: int = df['club_jersey_number']
        self.goal_keep_diving: int = df['goal_keep_diving']
        self.goal_keep_reflexes: int = df['goal_keep_reflexes']
        self.skill_ball_control: int = df['skill_ball_control']
