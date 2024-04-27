from abc import ABC
from typing import Dict

from .player_data import PlayerData

# strategy
OFFENSIVE = 'OFFENSIVE'
DEFENSIVE = 'DEFENSIVE'
NORMAL = 'NORMAL'

# player function
DEFENSE = 'DEFENSE'
MIDFIELD = 'MIDFIELD'
ATTACK = 'ATTACK'
GOALKEEPER = 'GOALKEEPER'


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
            player_data.defending = player_data.o_defending - 5
            player_data.dribbling = player_data.o_dribbling - 5
            player_data.mentality_interceptions = player_data.o_mentality_interceptions - 5
            player_data.mentality_vision = player_data.o_mentality_vision - 5
            player_data.movement_reactions = player_data.o_movement_reactions - 5
            player_data.skill_ball_control = player_data.o_skill_ball_control - 5
            player_data.passing = player_data.o_passing - 5
            player_data.pace = player_data.o_pace - 5
            player_data.skill_ball_control = player_data.o_skill_ball_control - 5
            player_data.shooting = player_data.o_shooting - 5
            player_data.overall = player_data.o_overall - 5


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
            'GK': LineUpGrid(18, 5, 'GK', GOALKEEPER),
            'RB': LineUpGrid(15, 8, 'RB', DEFENSE),
            'LCB': LineUpGrid(15, 4, 'CB1', DEFENSE),
            'RCB': LineUpGrid(15, 6, 'CB2', DEFENSE),
            'LB': LineUpGrid(15, 2, 'LB', DEFENSE),
            'CDM': LineUpGrid(12, 5, 'CDM', MIDFIELD),
            'RCM': LineUpGrid(10, 7, 'RCM', MIDFIELD),
            'LCM': LineUpGrid(10, 3, 'LCM', MIDFIELD),
            'RW': LineUpGrid(6, 8, 'RW', ATTACK),
            'ST': LineUpGrid(6, 5, 'ST', ATTACK),
            'LW': LineUpGrid(6, 2, 'LW', ATTACK)
        }


class Away433(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(1, 5, 'GK', GOALKEEPER),
            'RB': LineUpGrid(4, 2, 'RB', DEFENSE),
            'RCB': LineUpGrid(4, 4, 'RCB', DEFENSE),
            'LCB': LineUpGrid(4, 6, 'LCB', DEFENSE),
            'LB': LineUpGrid(4, 8, 'LB', DEFENSE),
            'CDM': LineUpGrid(7, 5, 'CDM', MIDFIELD),
            'LCM': LineUpGrid(9, 7, 'LCM', MIDFIELD),
            'RCM': LineUpGrid(9, 3, 'RCM', MIDFIELD),
            'RW': LineUpGrid(13, 8, 'RW', ATTACK),
            'ST': LineUpGrid(13, 5, 'ST', ATTACK),
            'LW': LineUpGrid(13, 2, 'LW', ATTACK)
        }


class Home442(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(18, 5, 'GK', GOALKEEPER),
            'RB': LineUpGrid(15, 8, 'RB', DEFENSE),
            'LCB': LineUpGrid(15, 4, 'LCB', DEFENSE),
            'RCB': LineUpGrid(15, 6, 'RCB', DEFENSE),
            'LB': LineUpGrid(15, 2, 'LB', DEFENSE),
            'RM': LineUpGrid(10, 8, 'RM', MIDFIELD),
            'RCM': LineUpGrid(11, 6, 'RCM', MIDFIELD),
            'LCM': LineUpGrid(11, 4, 'LCM', MIDFIELD),
            'LM': LineUpGrid(10, 2, 'LM', MIDFIELD),
            'ST1': LineUpGrid(6, 4, 'ST1', ATTACK),
            'ST2': LineUpGrid(6, 6, 'ST2', ATTACK)
        }


class Away442(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(1, 5, 'GK', GOALKEEPER),
            'RB': LineUpGrid(4, 2, 'RB', DEFENSE),
            'RCB': LineUpGrid(4, 4, 'RCB', DEFENSE),
            'LCB': LineUpGrid(4, 6, 'LCB', DEFENSE),
            'LB': LineUpGrid(4, 8, 'LB', DEFENSE),
            'RM': LineUpGrid(9, 8, 'RM', MIDFIELD),
            'RCM': LineUpGrid(8, 4, 'RCM', MIDFIELD),
            'LCM': LineUpGrid(8, 6, 'LCM', MIDFIELD),
            'LM': LineUpGrid(9, 2, 'LM', MIDFIELD),
            'ST1': LineUpGrid(13, 6, 'ST1', ATTACK),
            'ST2': LineUpGrid(13, 4, 'ST2', ATTACK)
        }


class Home343(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(18, 5, 'GK', GOALKEEPER),
            'LCB': LineUpGrid(15, 3, 'LCB', DEFENSE),
            'CB': LineUpGrid(15, 5, 'CB', DEFENSE),
            'RCB': LineUpGrid(15, 7, 'RCB', DEFENSE),
            'RM': LineUpGrid(10, 8, 'RM', MIDFIELD),
            'RCM': LineUpGrid(11, 6, 'RCM', MIDFIELD),
            'LCM': LineUpGrid(11, 4, 'LCM', MIDFIELD),
            'LM': LineUpGrid(10, 2, 'LM', MIDFIELD),
            'RW': LineUpGrid(6, 8, 'RW', ATTACK),
            'ST': LineUpGrid(6, 5, 'ST', ATTACK),
            'LW': LineUpGrid(6, 2, 'LW', ATTACK)
        }


class Away343(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(1, 5, 'GK', GOALKEEPER),
            'RCB': LineUpGrid(4, 3, 'RCB', DEFENSE),
            'CB': LineUpGrid(4, 5, 'CB', DEFENSE),
            'LCB': LineUpGrid(4, 7, 'LCB', DEFENSE),
            'RM': LineUpGrid(9, 8, 'RM', MIDFIELD),
            'LCM': LineUpGrid(8, 6, 'LCM', MIDFIELD),
            'RCM': LineUpGrid(8, 4, 'RCM', MIDFIELD),
            'LM': LineUpGrid(9, 2, 'LM', MIDFIELD),
            'RW': LineUpGrid(13, 8, 'RW', ATTACK),
            'ST': LineUpGrid(13, 5, 'ST', ATTACK),
            'LW': LineUpGrid(13, 2, 'LW', ATTACK)
        }


class Home532(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(18, 5, 'GK', GOALKEEPER),
            'RB': LineUpGrid(14, 9, 'RB', DEFENSE),
            'LCB': LineUpGrid(15, 3, 'LCB', DEFENSE),
            'CB': LineUpGrid(15, 5, 'CB', DEFENSE),
            'RCB': LineUpGrid(15, 7, 'RCB', DEFENSE),
            'LB': LineUpGrid(14, 1, 'LB', DEFENSE),
            'CDM': LineUpGrid(12, 5, 'CDM', MIDFIELD),
            'RCM': LineUpGrid(10, 7, 'RCM', MIDFIELD),
            'LCM': LineUpGrid(10, 3, 'LCM', MIDFIELD),
            'ST1': LineUpGrid(6, 4, 'ST1', ATTACK),
            'ST2': LineUpGrid(6, 6, 'ST2', ATTACK)
        }


class Away532(LineUp):
    def __init__(self) -> None:
        super().__init__()
        self.line_up = {
            'GK': LineUpGrid(1, 5, 'GK', GOALKEEPER),
            'RB': LineUpGrid(5, 1, 'RB', DEFENSE),
            'RCB': LineUpGrid(4, 3, 'RCB', DEFENSE),
            'CB': LineUpGrid(4, 5, 'CB', DEFENSE),
            'LCB': LineUpGrid(4, 7, 'LCB', DEFENSE),
            'LB': LineUpGrid(5, 9, 'LB', DEFENSE),
            'CDM': LineUpGrid(7, 5, 'CDM', MIDFIELD),
            'LCM': LineUpGrid(9, 7, 'LCM', MIDFIELD),
            'RCM': LineUpGrid(9, 3, 'RCM', MIDFIELD),
            'ST1': LineUpGrid(13, 6, 'ST1', ATTACK),
            'ST2': LineUpGrid(13, 4, 'ST2', ATTACK)
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
