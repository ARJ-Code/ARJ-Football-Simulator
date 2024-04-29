import json

class SimulationAnalyzer:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.load_data()
        
    def load_data(self):
        data = {}
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        self.data = data

    def analyze(self):
        for game_data in self.data.values():
            self.analyze_game(game_data)

            home_data, away_data = self.analyze_game(game_data)
            game_data_analyzer = GameDataAnalyzer(home_data, away_data)

    def analyze_game(self, game_data):
        home_data = TeamDataAnalyzer(game_data['home'])
        home_data.analyze()
        away_data = TeamDataAnalyzer(game_data['away'])
        away_data.analyze()

        return (home_data, away_data)

    def plot(self):
        pass

    def save(self):
        pass

class GameDataAnalyzer:
    def __init__(self, home_data, away_data):
        self.home_data = home_data
        self.away_data = away_data

    def analyze(self):
        

class TeamDataAnalyzer:
    def __init__(self, team_data):
        self.team_data = team_data

    def analyze(self):
        self.changes = self.team_data['changes']
        self.goals = self.team_data['goals']
        self.possession = self.team_data['possession_instances']
        self.shots = self.team_data['shots']
        self.passes = self.team_data['passes_completed']
        self.fouls = self.team_data['fouls']

        self.max_goals = self.most_goals_player()
        self.max_passes = self.most_passes_player()
        self.max_fouls = self.most_fouls_player()
        self.max_shots = self.most_shoots_player()

    def most_goals_player(self):
        max_goals = -1
        player = None
        for p in self.team_data['players_statistics'].keys():
            player_goals = self.team_data['players_statistics'][p]['goals']
            if player_goals > max_goals:
                max_goals = player_goals
                player = p

        return (player, max_goals)
    
    def most_passes_player(self):
        max_passes = -1
        player = None
        for p in self.team_data['players_statistics'].keys():
            player_passes = self.team_data['players_statistics'][p]['passes']
            if player_passes > max_passes:
                max_passes = player_passes
                player = p

        return (player, max_passes)
    
    def most_fouls_player(self):
        max_fouls = -1
        player = None
        for p in self.team_data['players_statistics'].keys():
            player_fouls = self.team_data['players_statistics'][p]['fouls']
            if player_fouls > max_fouls:
                max_fouls = player_fouls
                player = p

        return (player, max_fouls)
    
    def most_shoots_player(self):
        max_shoots = -1
        player = None
        for p in self.team_data['players_statistics'].keys():
            player_shoots = self.team_data['players_statistics'][p]['shots']
            if player_shoots > max_shoots:
                max_shoots = player_shoots
                player = p

        return (player, max_shoots)