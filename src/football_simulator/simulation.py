from football_tools.game import Game
from football_agent.team import HOME, Team
from typing import Generator


class FootballSimulation:
    def __init__(self, home: Team, away: Team) -> None:
        self.home: Team = home
        self.away: Team = away
        self.game: Game = Game(home.line_up, away.line_up)

    def simulate(self, actions: int = 180) -> Generator[str, None, None]:
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
            self.home.players[player_with_ball].play(self.game)
        else:
            self.away.players[player_with_ball].play(self.game)

        for l in self.game.field.grid:
            for n in l:
                if not n.ball:
                    if n.team == HOME:
                        self.home.players[n.player].play(self.game)
                    else:
                        self.away.players[n.player].play(self.game)
