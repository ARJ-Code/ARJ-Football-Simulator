from abc import ABC, abstractmethod
from typing import Dict
from .player_data import PlayerData


class LineUpGrid(ABC):
    def __init__(self, row: int, col: int) -> None:
        self.row: int = row
        self.col: int = col
        self.player: int = -1

    def conf_player(self, position: str, player: PlayerData):
        in_position = False
        for p in player.o_player_positions:
            if p in position: 
                in_position = True
                break
        self._set_statistics(player, in_position)
        self.player: int = player.dorsal

    
    def _set_statistics(self, player_data: PlayerData, in_position: bool) -> None:
        if not in_position:
            player_data.defending -= 5
            player_data.dribbling -= 5
            player_data.mentality_interceptions -= 5
            player_data.mentality_vision -= 5
            player_data.movement_reactions -= 5
            player_data.skill_ball_control -= 5
            player_data.passing -= 5
            player_data.pace -= 5
            player_data.skill_ball_control -= 5
            player_data.shooting -= 5



class LineUp(ABC):
    def __init__(self) -> None:
        self.line_up: Dict[str, LineUpGrid] = {}

    def conf_players(self, players: Dict[str, PlayerData]) -> None:
        for k, v in players.items():
            self.line_up[k].conf_player(k, v)

    def get_player_position(self, player: int) -> LineUpGrid | None:
        for k, v in self.line_up.items():
            if v.player == player:
                return v

        return None

    def change_line_up(self, line_up: 'LineUp', players: Dict[str, PlayerData]) -> None:
        self.line_up = line_up.line_up
        self.conf_players(players)

class Home433(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(18, 5),
            'RB': LineUpGrid(15, 8),
            'CB1': LineUpGrid(15, 4),
            'CB2': LineUpGrid(15, 6),
            'LB': LineUpGrid(15, 2),
            'CDM': LineUpGrid(12, 5),
            'CM1': LineUpGrid(10, 7),
            'CM2': LineUpGrid(10, 3),
            'RW': LineUpGrid(6, 8),
            'ST': LineUpGrid(6, 5),
            'LW': LineUpGrid(6, 2)
        }

class Away433(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(1, 5),
            'RB': LineUpGrid(4, 2),
            'CB1': LineUpGrid(4, 4),
            'CB2': LineUpGrid(4, 6),
            'LB': LineUpGrid(4, 8),
            'CDM': LineUpGrid(7, 5),
            'CM1': LineUpGrid(9, 7),
            'CM2': LineUpGrid(9, 3),
            'RW': LineUpGrid(13, 8),
            'ST': LineUpGrid(13, 5),
            'LW': LineUpGrid(13, 2)
        }        
class Home442(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(18, 5),
            'RB': LineUpGrid(15, 8),
            'CB1': LineUpGrid(15, 4),
            'CB2': LineUpGrid(15, 6),
            'LB': LineUpGrid(15, 2),
            'RM': LineUpGrid(10, 8),
            'CM1': LineUpGrid(11, 6),
            'CM2': LineUpGrid(11, 4),
            'LM': LineUpGrid(10, 2),
            'ST1': LineUpGrid(6, 4),
            'ST2': LineUpGrid(6, 6)
        }
class Away442(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(1, 5),
            'RB': LineUpGrid(4, 2),
            'CB1': LineUpGrid(4, 4),
            'CB2': LineUpGrid(4, 6),
            'LB': LineUpGrid(4, 8),
            'RM': LineUpGrid(9, 8),
            'CM1': LineUpGrid(8, 4),
            'CM2': LineUpGrid(8, 6),
            'LM': LineUpGrid(9, 2),
            'ST1': LineUpGrid(13, 6),
            'ST2': LineUpGrid(13, 4)
        }    

class Home343(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(18, 5),
            'CB1': LineUpGrid(15, 3),
            'CB2': LineUpGrid(15, 5),
            'CB3': LineUpGrid(15, 7),
            'RM': LineUpGrid(10, 8),
            'CM1': LineUpGrid(11, 6),
            'CM2': LineUpGrid(11, 4),
            'LM': LineUpGrid(10, 2),
            'RW': LineUpGrid(6, 8),
            'ST': LineUpGrid(6, 5),
            'LW': LineUpGrid(6, 2)
        }  

class Away343(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(1, 5),
            'CB1': LineUpGrid(4, 3),
            'CB2': LineUpGrid(4, 5),
            'CB3': LineUpGrid(4, 7),
            'RM': LineUpGrid(9, 8),
            'CM1': LineUpGrid(8, 6),
            'CM2': LineUpGrid(8, 4),
            'LM': LineUpGrid(9, 2),
            'RW': LineUpGrid(13, 8),
            'ST': LineUpGrid(13, 5),
            'LW': LineUpGrid(13, 2)
        }

class Home532(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(18, 5),
            'RB': LineUpGrid(14, 9),
            'CB1': LineUpGrid(15, 3),
            'CB2': LineUpGrid(15, 5),
            'CB3': LineUpGrid(15, 7),
            'LB': LineUpGrid(14, 1),
            'CDM': LineUpGrid(12, 5),
            'CM1': LineUpGrid(10, 7),
            'CM2': LineUpGrid(10, 3),
            'ST1': LineUpGrid(6, 4),
            'ST2': LineUpGrid(6, 6)
        }        

class Away532(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(1, 5),
            'RB': LineUpGrid(5, 1),
            'CB1': LineUpGrid(4, 3),
            'CB2': LineUpGrid(4, 5),
            'CB3': LineUpGrid(4, 7),
            'LB': LineUpGrid(5, 9),
            'CDM': LineUpGrid(7, 5),
            'CM1': LineUpGrid(9, 7),
            'CM2': LineUpGrid(9, 3),
            'ST1': LineUpGrid(13, 6),
            'ST2': LineUpGrid(13, 4)
        }        

class ProveLineUp(LineUp):
    def __init__(self) -> None:
        super().__init__()


class ProveLineUpGrid(LineUpGrid):
    def __init__(self, player: int, row: int, col: int) -> None:
        super().__init__(row, col)
        self.player: int = player

    def _set_statistics(self, player_data: PlayerData) -> None:
        return super()._set_statistics(player_data)
