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

            field_str = str(self.game.field)
            statistics = self.game_statistics()

            yield field_str+'\n'+statistics

    def game_statistics(self) -> str:
        nh = self.home.name
        na = self.away.name
        gh = self.game.home.statistics.goals
        ga = self.game.away.statistics.goals
        yh = self.game.home.statistics.yellow_cards
        ya = self.game.away.statistics.yellow_cards
        rh = self.game.home.statistics.red_cards
        ra = self.game.away.statistics.red_cards

        def get_spaces(n):
            return ' '*(n)

        def get_num(n):
            if n < 10:
                return ' '+str(n)
            return str(n)

        len_s = len(nh)+len(na)

        return f"""
{nh}{get_spaces(52-len_s)}{na}
⚽ {get_num(gh)}{get_spaces(42)}{get_num(ga)} ⚽
🟨 {get_num(yh)}{get_spaces(42)}{get_num(ya)} 🟨
🟥 {get_num(rh)}{get_spaces(42)}{get_num(ra)} 🟥
                """

    def instance_time(self):
        player_with_ball = -1
        team = ''

        for l in self.game.field.grid:
            for n in l:
                if n.ball:
                    player_with_ball = n.player
                    team = n.team

        if team == HOME:
            self.dispatch.dispatch(
                self.home.players[player_with_ball].play(self.game))
        if team == AWAY:
            self.dispatch.dispatch(
                self.away.players[player_with_ball].play(self.game))

        mask = set()

        for l in self.game.field.grid:
            for n in l:
                if (n.player, n.team) in mask:
                    continue
                if not n.ball:
                    mask.add((n.player, n.team))
                    if n.team == HOME:
                        self.dispatch.dispatch(
                            self.home.players[n.player].play(self.game))
                    if n.team == AWAY:
                        self.dispatch.dispatch(
                            self.away.players[n.player].play(self.game))
