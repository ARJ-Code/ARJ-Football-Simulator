from football_agent.actions import Dispatch
from football_tools.game import Game
from football_tools.data import TeamData
from football_agent.team import HOME, AWAY, TeamAgent
from typing import Generator, Tuple


class FootballSimulation:
    def __init__(self, home: Tuple[TeamAgent, TeamData], away: Tuple[TeamAgent, TeamData]) -> None:
        self.home: TeamAgent = home[0]
        self.away: TeamAgent = away[0]
        self.game: Game = Game(home[1], away[1])
        self.dispatch = Dispatch()

    def simulate(self, actions: int = 180) -> Generator[str, None, None]:
        yield str(self.game.field)

        for _ in range(actions):
            self.instance_time()
            yield str(self.game.field)

    def instance_time(self):
        player_with_ball = -1
        team = ''

        for l in self.game.field.grid:
            for n in l:
                if n.ball:
                    player_with_ball = n.player
                    team = n.team

        if team == HOME:
            self.dispatch.dispatch(self.home.players[player_with_ball].play(self.game))
        if n.team == AWAY:
            self.dispatch.dispatch(self.away.players[player_with_ball].play(self.game))

        for l in self.game.field.grid:
            for n in l:
                if not n.ball:
                    if n.team == HOME:
                        self.dispatch.dispatch(self.home.players[n.player].play(self.game))
                    if n.team == AWAY:
                        self.dispatch.dispatch(self.away.players[n.player].play(self.game))
