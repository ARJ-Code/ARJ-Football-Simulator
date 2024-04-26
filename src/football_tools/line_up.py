from abc import ABC
from typing import Dict, List
from .player_data import PlayerData

# strategy
OFFENSIVE = 'OFFENSIVE'
DEFENSIVE = 'DEFENSIVE'
NORMAL = 'NORMAL'

# player function
DEFENSE = 'DEFENSE'
MIDFIELD = 'MIDFIELD'
ATTACK = 'ATTACK'


class LineUpGrid:
    def __init__(self, row: int, col: int, position: str, player_function: str) -> None:
        self.row: int = row
        self.col: int = col
        self.player: int = -1
        self.position: str = position
        self.conf: str = NORMAL
        self.player_function: str = player_function

    def conf_player(self, player: PlayerData):
        self._set_statistics(player, player.club_position == self.position)
        self.player: int = player.dorsal

    def set_statistics(self, player_data: PlayerData) -> None:
        self._set_statistics(
            player_data, player_data.club_position in self.position)

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
            player_data.overall -= 5


class LineUp(ABC):
    def __init__(self) -> None:
        self.line_up: Dict[str, LineUpGrid] = {}

    def conf_players(self, players: Dict[str, PlayerData]) -> None:
        for k, v in players.items():
            self.line_up[k].conf_player(v)

    def get_player_position(self, player: int) -> LineUpGrid | None:
        for _, v in self.line_up.items():
            if v.player == player:
                return v

        return None
    
    def get_player_function(self, player: int) -> str:
        line_up_position = self.get_player_position(player)
        return line_up_position.player_function


class Home433(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(18, 5, 'GK'),
            'RB': LineUpGrid(15, 8, 'RB'),
            'LCB': LineUpGrid(15, 4, 'CB1'),
            'RCB': LineUpGrid(15, 6, 'CB2'),
            'LB': LineUpGrid(15, 2, 'LB'),
            'CDM': LineUpGrid(12, 5, 'CDM'),
            'RCM': LineUpGrid(10, 7, 'RCM'),
            'LCM': LineUpGrid(10, 3, 'LCM'),
            'RW': LineUpGrid(6, 8, 'RW'),
            'ST': LineUpGrid(6, 5, 'ST'),
            'LW': LineUpGrid(6, 2, 'LW')
        }


class Away433(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(1, 5, 'GK'),
            'RB': LineUpGrid(4, 2, 'RB'),
            'RCB': LineUpGrid(4, 4, 'RCB'),
            'LCB': LineUpGrid(4, 6, 'LCB'),
            'LB': LineUpGrid(4, 8, 'LB'),
            'CDM': LineUpGrid(7, 5, 'CDM'),
            'LCM': LineUpGrid(9, 7, 'LCM'),
            'RCM': LineUpGrid(9, 3, 'RCM'),
            'RW': LineUpGrid(13, 8, 'RW'),
            'ST': LineUpGrid(13, 5, 'ST'),
            'LW': LineUpGrid(13, 2, 'LW')
        }


class Home442(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(18, 5, 'GK'),
            'RB': LineUpGrid(15, 8, 'RB'),
            'LCB': LineUpGrid(15, 4, 'LCB'),
            'RCB': LineUpGrid(15, 6, 'RCB'),
            'LB': LineUpGrid(15, 2, 'LB'),
            'RM': LineUpGrid(10, 8, 'RM'),
            'RCM': LineUpGrid(11, 6, 'RCM'),
            'LCM': LineUpGrid(11, 4, 'LCM'),
            'LM': LineUpGrid(10, 2, 'LM'),
            'ST1': LineUpGrid(6, 4, 'ST1'),
            'ST2': LineUpGrid(6, 6, 'ST2')
        }


class Away442(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(1, 5, 'GK'),
            'RB': LineUpGrid(4, 2, 'RB'),
            'RCB': LineUpGrid(4, 4, 'RCB'),
            'LCB': LineUpGrid(4, 6, 'LCB'),
            'LB': LineUpGrid(4, 8, 'LB'),
            'RM': LineUpGrid(9, 8, 'RM'),
            'RCM': LineUpGrid(8, 4, 'RCM'),
            'LCM': LineUpGrid(8, 6, 'LCM'),
            'LM': LineUpGrid(9, 2, 'LM'),
            'ST1': LineUpGrid(13, 6, 'ST1'),
            'ST2': LineUpGrid(13, 4, 'ST2')
        }


class Home343(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(18, 5, 'GK'),
            'LCB': LineUpGrid(15, 3, 'LCB'),
            'CB': LineUpGrid(15, 5, 'CB'),
            'RCB': LineUpGrid(15, 7, 'RCB'),
            'RM': LineUpGrid(10, 8, 'RM'),
            'RCM': LineUpGrid(11, 6, 'RCM'),
            'LCM': LineUpGrid(11, 4, 'LCM'),
            'LM': LineUpGrid(10, 2, 'LM'),
            'RW': LineUpGrid(6, 8, 'RW'),
            'ST': LineUpGrid(6, 5, 'ST'),
            'LW': LineUpGrid(6, 2, 'LW')
        }


class Away343(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(1, 5, 'GK'),
            'RCB': LineUpGrid(4, 3, 'RCB'),
            'CB': LineUpGrid(4, 5, 'CB'),
            'LCB': LineUpGrid(4, 7, 'LCB'),
            'RM': LineUpGrid(9, 8, 'RM'),
            'LCM': LineUpGrid(8, 6, 'LCM'),
            'RCM': LineUpGrid(8, 4, 'RCM'),
            'LM': LineUpGrid(9, 2, 'LM'),
            'RW': LineUpGrid(13, 8, 'RW'),
            'ST': LineUpGrid(13, 5, 'ST'),
            'LW': LineUpGrid(13, 2, 'LW')
        }


class Home532(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(18, 5, 'GK'),
            'RB': LineUpGrid(14, 9, 'RB'),
            'LCB': LineUpGrid(15, 3, 'LCB'),
            'CB': LineUpGrid(15, 5, 'CB'),
            'RCB': LineUpGrid(15, 7, 'RCB'),
            'LB': LineUpGrid(14, 1, 'LB'),
            'CDM': LineUpGrid(12, 5, 'CDM'),
            'RCM': LineUpGrid(10, 7, 'RCM'),
            'LCM': LineUpGrid(10, 3, 'LCM'),
            'ST1': LineUpGrid(6, 4, 'ST1'),
            'ST2': LineUpGrid(6, 6, 'ST2')
        }


class Away532(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(1, 5, 'GK'),
            'RB': LineUpGrid(5, 1, 'RB'),
            'RCB': LineUpGrid(4, 3, 'RCB'),
            'CB': LineUpGrid(4, 5, 'CB'),
            'LCB': LineUpGrid(4, 7, 'LCB'),
            'LB': LineUpGrid(5, 9, 'LB'),
            'CDM': LineUpGrid(7, 5, 'CDM'),
            'LCM': LineUpGrid(9, 7, 'LCM'),
            'RCM': LineUpGrid(9, 3, 'RCM'),
            'ST1': LineUpGrid(13, 6, 'ST1'),
            'ST2': LineUpGrid(13, 4, 'ST2')
        }


class ProveLineUp(LineUp):
    def __init__(self) -> None:
        super().__init__()


class ProveLineUpGrid(LineUpGrid):
    def __init__(self, player: int, row: int, col: int) -> None:
        super().__init__(row, col, '')
        self.player: int = player

    def _set_statistics(self, player_data: PlayerData) -> None:
        return super()._set_statistics(player_data)
