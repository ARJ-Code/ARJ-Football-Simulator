import pandas as pd
import json


def filter_atributes(json_data: str):
    data_list = json.loads(json_data)
    formatted_data = [{key: player[key] for key in selected_keys if key in player} for player in data_list]
    return json.dumps(formatted_data, indent=4)

selected_keys = ["short_name", "club_name", "player_positions", "overall", "pace", "shooting", "passing", "dribbling", "defending", "physic", "attacking_finishing", "mentality_vision", "power_stamina", "mentality_aggression", "mentality_interceptions", "movement_reactions"]    

df = pd.read_csv('C:/simulacion/ARJ-Football-Simulator/data/players_22.csv')

jugadores_fc_barcelona = df[df['club_name'] == 'FC Barcelona']

json_data = jugadores_fc_barcelona.to_json(orient='records')

with open('players_fc_barcelona.json', 'w') as file:
    file.write(filter_atributes(json_data))

jugadores_real_madrid = df[df['club_name'] == 'Real Madrid CF']

json_data = jugadores_real_madrid.to_json(orient='records')

with open('players_real_madrid.json', 'w') as file:
    file.write(filter_atributes(json_data))    





