import json

from simulation_tools.field import Field
from simulation_tools.player import Player



with open('players_fc_barcelona.json') as file:
    json_data = json.load(file)

player_with_file_data = Player(json_data[6])
player_with_file_data.play()


field = Field(20, 12)  
field.place_player(Player(json_data[6]).data["short_name"], 3, 5)
field.place_player(Player(json_data[7]).data["short_name"], 7, 5)
field.place_player(Player(json_data[8]).data["short_name"], 8, 4)
field.print_field()
field.move_player(3, 5, 5, 5)
field.print_field()


