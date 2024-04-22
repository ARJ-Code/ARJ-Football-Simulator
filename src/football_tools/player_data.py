from pandas import DataFrame

class PlayerData():
    def __init__(self, df: DataFrame):
        self.short_name: str = df['short_name']
        self.club_name: str = df['club_name']
        self.club_position: str = df['club_position']
        self.player_positions: str = df['player_positions'].split(', ')
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
        self.o_club_position: str = df['club_position']
        self.o_player_positions: str = df['player_positions'].split(', ')
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
