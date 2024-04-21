from abc import ABC, abstractmethod
from typing import Dict
from .player_data import PlayerData


class LineUp(ABC):
    def __init__(self) -> None:
        self.line_up: Dict[str, LineUpGrid] = {}

    def conf_players(self, players: Dict[str, PlayerData]) -> None:
        for k, v in players.items():
            self.line_up[k].conf_player(v)

    def change_line_up(self, line_up: 'LineUp', players: Dict[str, PlayerData]) -> None:
        self.line_up = line_up.line_up
        self.conf_players(players)


class LineUpGrid(ABC):
    def __init__(self, row: int, col: int) -> None:
        self.row: int = row
        self.col: int = col
        self.player: int = -1

    def conf_player(self, player: PlayerData):
        self._set_statistics(player)
        self.player: int = player.dorsal

    @abstractmethod
    def _set_statistics(self, player_data: PlayerData) -> None:
        pass


class ProveLineUp(LineUp):
    def __init__(self) -> None:
        super().__init__()


class ProveLineUpGrid(LineUpGrid):
    def __init__(self, player: int, row: int, col: int) -> None:
        super().__init__(row, col)
        self.player: int = player

    def _set_statistics(self, player_data: PlayerData) -> None:
        return super()._set_statistics(player_data)
