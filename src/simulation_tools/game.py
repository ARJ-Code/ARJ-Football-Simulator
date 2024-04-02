from typing import List
from simulation_tools.field import Field

class StatisticsPLayer:
    def __init__(self, player):
        self.player = player
        self.goals = 0
        self.passes = 0
        self.shots = 0
        self.saves = 0
        self.fouls = 0
        self.red_cards = 0
        self.yellow_cards = 0
        self.minutes_played = 0

    
class StatisticsTeam:
    def __init__(self, team):
        self.team_name: team
        self.goals: 0
        self.possession: 50
        self.shots: 0
        self.fouls: 0
        self.passes_completed: 0
        self.yellow_cards: 0
        self.red_cards: 0
        self.lineup: List[str]

class Game:
    def __init__(self, players_A, players_B, board, initial_score = tuple(0,0), max_rounds=360):
        self.players_B = players_B
        self.players_A = players_A
        self.field = Field()
        self.score = initial_score
        self.max_rounds = max_rounds
        self.rounds = 0
        self.statistics_A = StatisticsTeam("A")
        self.statistics_B = StatisticsTeam("B")
        

    def place_players(self):
        pass
        # for player in self.players_A:
        #     self.field.place_player(player.data["short_name"], 3, 5)
        # for player in self.players_B:
        #     self.field.place_player(player.data["short_name"], 7, 5)

    def simulate(self):
        pass
        # while self.rounds < self.max_rounds:
        #     for player in self.players_A:
        #         play = player.play(self.field, )

        #     for player in self.players_B:
        #         player.play(self.field)    
        #     self.rounds += 1
        # return self.board.get_winner()

    def make_play(self, play):
        pass
    
    def make_coach_decision():
        pass
