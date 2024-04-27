from .llm import query
from pandas import DataFrame
from typing import Tuple
from football_simulator.simulation_params import SimulationParams


def conf_game_llm(user_prompt: str, df: DataFrame) -> SimulationParams | None:
    try:
        league = league_prompt(user_prompt, df)
        home, away = teams_prompt(user_prompt, league, df)
        return SimulationParams(home, away)
    except:
        return None


def league_prompt(user_prompt: str, df: DataFrame) -> str:
    league_names = df['league_name'].unique()
    league_names = [i for i in league_names if isinstance(i, str)]

    prompt =\
        """
Tengo la siguiente lista de ligas y esta query definida por el usuario del texto introducido por el usuario dime 
de que liga el usuario desea simular el juego de futbol. El siguiente formato por ejemplo: Spain Primera Division
"""
    team = query(prompt+'\n'+'\n'.join(league_names)+'\n'+user_prompt)

    if not team in league_names:
        raise Exception()

    return team


def teams_prompt(user_prompt: str, league_name: str, df: DataFrame) -> Tuple[str, str]:
    team_names = df[df['league_name'] == league_name]['club_name'].to_list()
    prompt =\
        """
Tengo la siguiente lista de equipos y esta query definida por el usuario del texto introducido por el usuario dime 
que equipo es el visitador y cual es el local, con el siguiente formato: FC Barcelona vs Real Madrid CF, el de la izquierda
es el local y el de la derecha el visitador
"""
    response = query(prompt+'\n'+'\n'.join(team_names[:20])+'\n'+user_prompt)
    home = response.split(' vs ')[0]
    away = response.split(' vs ')[1]

    if not home in team_names or not away in team_names:
        raise Exception()

    return home, away
