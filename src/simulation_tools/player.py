from abc import ABC, abstractmethod

# class Player_Data():
#     short_name: str
#     club_name: str
#     player_positions: str
#     overall: int
#     pace: int
#     shooting: int
#     passing: int
#     dribbling: int
#     defending: int
#     physic: int
#     attacking_finishing: int
#     mentality_vision: int
#     power_stamina: int
#     mentality_aggression: int
#     mentality_interceptions: int
#     movement_reactions: int

class Playable(ABC):
    @abstractmethod
    def play(self):
        pass

class Player(Playable):
    def __init__(self, data):
        self.data = data

    def play(self, game_instance):
        print ("bola pa messi")   
     
    
