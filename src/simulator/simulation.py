from simulation_tools.game import Game, Team


class FootballSimulation:
    def __init__(self, home: Team, visitor: Team) -> None:
        self.home = home
        self.visitor = visitor
        self.game = Game(home, visitor)

    # def simulate(self, actions: int = 180):
    #     for _ in range(actions):
    #         for player in self.home