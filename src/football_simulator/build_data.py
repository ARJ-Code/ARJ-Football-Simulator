import pandas as pd
from typing import List
from football_tools.data import PlayerData

df = pd.read_csv('data/players_22.csv')


def get_data(team: str) -> List[PlayerData]:
    data = df[df['club_name'] == team]
    return [PlayerData(p) for _, p in data.iterrows()]
