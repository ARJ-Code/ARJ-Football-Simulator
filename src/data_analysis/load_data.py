import json


class SimulationAnalyzer:
    def __init__(self, file_path) -> None:
        self.name = file_path.split('/')[-1].split('.')[0]
        self.file_path = file_path
        self.load_data()
        self.games = []

    def load_data(self):
        data = {}
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        self.data = data

    def analyze(self):
        for game_data in self.data.values():
            self.analyze_game(game_data)

            home_data, away_data = self.analyze_game(game_data)
            self.games.append(GameDataAnalyzer(home_data, away_data))

    def analyze_game(self, game_data):
        home_data = TeamDataAnalyzer(game_data['home'])
        home_data.analyze()
        away_data = TeamDataAnalyzer(game_data['away'])
        away_data.analyze()

        return (home_data, away_data)


class GameDataAnalyzer:
    def __init__(self, home_data, away_data):
        self.home_data = home_data
        self.away_data = away_data


class TeamDataAnalyzer:
    def __init__(self, team_data):
        self.team_data = team_data

    def analyze(self):
        self.changes = self.team_data['statistics']['changes']
        self.goals = self.team_data['statistics']['goals']
        self.possession = self.team_data['statistics']['possession_instances']
        self.shots = self.team_data['statistics']['shots']
        self.passes = self.team_data['statistics']['passes_completed']
        self.fouls = self.team_data['statistics']['fouls']

        self.player_statistics = self.team_data['players_statistics']
