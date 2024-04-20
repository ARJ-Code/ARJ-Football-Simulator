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

    def simulate(self, actions: int = 180) -> Generator[str, None, None]:
        simulator = Simulator(self.home, self.away, self.game)

        for i in range(actions):
            simulator.simulate_instance()

            field_str = str(self.game.field)
            statistics = self.game_statistics(i)

            yield field_str+'\n'+statistics

    def game_statistics(self, instance: int) -> str:
        nh = f'\033[34m{self.home.name}\033[0m'
        na = f'\033[31m{self.away.name}\033[0m'
        gh = self.game.home.statistics.goals
        ga = self.game.away.statistics.goals
        yh = self.game.home.statistics.yellow_cards
        ya = self.game.away.statistics.yellow_cards
        rh = self.game.home.statistics.red_cards
        ra = self.game.away.statistics.red_cards
        ph = self.game.home.statistics.possession_instances*100//(instance+1)
        pa = self.game.away.statistics.possession_instances*100//(instance+1)

        def get_spaces(n):
            return ' '*(n)

        def get_num(n):
            if n < 10:
                return '  '+str(n)
            if n < 100:
                return ' '+str(n)
            return str(n)

        len_s = len(nh)+len(na)-18

        return f"""
{nh}{get_spaces(52-len_s)}{na}
⚽ {get_num(gh)}{get_spaces(40)}{get_num(ga)} ⚽
⌛ {get_num(ph)}{get_spaces(40)}{get_num(pa)} ⌛
🟨 {get_num(yh)}{get_spaces(40)}{get_num(ya)} 🟨
🟥 {get_num(rh)}{get_spaces(40)}{get_num(ra)} 🟥

                """


class Simulator:
    def __init__(self, home: TeamAgent, away: TeamAgent, game: Game) -> None:
        self.home: TeamAgent = home
        self.away: TeamAgent = away
        self.game: Game = game
        self.dispatch = Dispatch()

    def simulate_instance(self, current_player: Tuple[int, str] = (-1, '')):
        player_with_ball = -1
        team = ''

        for l in self.game.field.grid:
            for n in l:
                if n.ball:
                    player_with_ball = n.player
                    team = n.team

        if team == HOME:
            self.game.home.statistics.possession_instances += 1
            if current_player[1] != HOME and current_player[0] != player_with_ball:
                self.dispatch.dispatch(
                    self.home.players[player_with_ball].play(self.game))
        if team == AWAY:
            self.game.away.statistics.possession_instances += 1
            if current_player[1] != AWAY and current_player[0] != player_with_ball:
                self.dispatch.dispatch(
                    self.away.players[player_with_ball].play(self.game))

        mask = set()

        for l in self.game.field.grid:
            for n in l:
                if (n.player, n.team) in mask:
                    continue
                if n.team == current_player[1] and n.player == current_player[0]:
                    continue
                if not n.ball:
                    mask.add((n.player, n.team))
                    if n.team == HOME:
                        self.dispatch.dispatch(
                            self.home.players[n.player].play(self.game))
                    if n.team == AWAY:
                        self.dispatch.dispatch(
                            self.away.players[n.player].play(self.game))

    def reset_instance(self):
        team = ''

        for l in self.game.field.grid:
            for n in l:
                if n.ball:
                    team = n.team

        if team == HOME:
            self.game.home.statistics.possession_instances -= 1
        if team == AWAY:
            self.game.away.statistics.possession_instances -= 1

        for _ in range(22):
            self.dispatch.reset(self.game)
