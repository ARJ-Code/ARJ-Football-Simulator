from typing import List
from abc import ABC, abstractmethod
from random import choice
from .actions import Action
from football_tools.data import HOME
from football_tools.line_up import *
from football_tools.game import Game
from football_tools.player_data import PlayerData


class ManagerStrategy(ABC):
    @abstractmethod
    def get_line_up(self, players: List[PlayerData], team: str) -> LineUp:
        pass

    @abstractmethod
    def action(self, game: Game) -> Action:
        pass


class RandomStrategy(ManagerStrategy):
    def get_line_up(self, players: List[PlayerData], team: str) -> LineUp:
        possible_line_ups: List[LineUp] = [Home343(), Home433(), Home442(), Home532(
        )] if team == HOME else [Away343(), Away433(), Away442(), Away532()]

        line_up = choice(possible_line_ups)

        set_players = set(players)
        aux = {}

        for k in line_up.line_up.keys():
            player = choice(list(set_players))
            aux[k] = player
            set_players.remove(player)

        line_up.conf_players(aux)

        return line_up

    def action(self, game: Game) -> Action:
        return super().action(game)
