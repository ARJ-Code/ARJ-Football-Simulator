from football_agent.player_strategy import FootballStrategy, MinimaxStrategy, PlayerStrategy, RandomStrategy
from .gemini import query
from pandas import DataFrame
from typing import Tuple
from football_agent.manager_line_up_strategy import ManagerLineUpStrategy, LineUpRandomStrategy, LineUpSimulateStrategy
from football_agent.manager_action_strategy import ManagerActionStrategy, ActionRandomStrategy, ActionSimulateStrategy, ActionMiniMaxStrategy

from football_simulator.simulation_params import SimulationParams


def conf_game_llm(user_prompt: str, df: DataFrame) -> SimulationParams | None:
    try:
        league = league_prompt(user_prompt, df)
        names = teams_prompt(user_prompt, league, df)
        managers_line_up = managers_line_up_prompt(user_prompt)
        managers_action = managers_action_prompt(user_prompt)
        players_action = players_action_prompt(user_prompt)
        return SimulationParams(names, managers_line_up, managers_action, players_action)
    except:
        return None


def league_prompt(user_prompt: str, df: DataFrame) -> str:
    league_names = df['league_name'].unique()
    league_names = [i for i in league_names if isinstance(i, str)]

    prompt =\
        """
Tengo la siguiente lista de ligas y esta query definida por el usuario, del texto introducido por el usuario dime 
de que liga el usuario desea simular el juego de futbol. El siguiente formato por ejemplo: Spain Primera Division
"""
    team = query(prompt+'\n'+'\n'.join(league_names)+'\n'+user_prompt)

    if not team in league_names:
        print(team)
        raise Exception()

    return team


def teams_prompt(user_prompt: str, league_name: str, df: DataFrame) -> Tuple[str, str]:
    team_names = df[df['league_name'] == league_name]['club_name'].to_list()
    prompt =\
        """
Tengo la siguiente lista de equipos y esta query definida por el usuario, del texto introducido por el usuario dime 
que equipo es el visitador y cual es el local, con el siguiente formato: FC Barcelona vs Real Madrid CF, el de la izquierda
es el local y el de la derecha el visitador
"""
    response = query(prompt+'\n'+'\n'.join(team_names[:20])+'\n'+user_prompt)

    try:
        home = response.split(' vs ')[0]
        away = response.split(' vs ')[1]

        if not home in team_names or not away in team_names:
            raise Exception()
        return home, away
    except:
        print(response)
        raise Exception()


def managers_line_up_prompt(user_prompt: str) -> Tuple[ManagerLineUpStrategy, ManagerLineUpStrategy]:
    prompt =\
        """
Tengo la siguiente lista de estrategias de escoger alineación para el manager de mi simulación de fútbol y esta query 
definida por el usuario, del texto introducido por el usuario dime que estrategia de escoger alineación es la que desea
el manager local y cual es la que desea el visitador, con el siguiente formato: random vs simulate la de la izquierda
es la estrategia del manager local y la de la derecha es la estrategia del manager visitador
"""

    strategies = {'random': LineUpRandomStrategy(
    ), 'simulate': LineUpSimulateStrategy()}

    response = query(prompt+'\n'+'\n'.join(strategies.keys())+'\n'+user_prompt)

    try:
        home = response.split(' vs ')[0]
        away = response.split(' vs ')[1]

        return strategies[home], strategies[away]
    except:
        return LineUpRandomStrategy(), LineUpRandomStrategy()


def managers_action_prompt(user_prompt: str) -> Tuple[ManagerActionStrategy, ManagerActionStrategy]:
    prompt =\
        """
Tengo la siguiente lista de estrategias de escoger las acciones durante el partido para el manager de mi simulación de fútbol 
y esta query definida por el usuario, del texto introducido por el usuario dime que estrategia de escoger alineación 
es la que desea el manager local y cual es la que desea el visitador, con el siguiente formato: random vs simulate la 
de la izquierda es la estrategia del manager local y la de la derecha es la estrategia del manager visitador
"""

    strategies = {'random': ActionSimulateStrategy(
    ), 'simulate': ActionSimulateStrategy(), 'minimax': ActionMiniMaxStrategy()}

    response = query(prompt+'\n'+'\n'.join(strategies.keys())+'\n'+user_prompt)

    try:
        home = response.split(' vs ')[0]
        away = response.split(' vs ')[1]

        return strategies[home], strategies[away]
    except:
        return ActionRandomStrategy(), ActionRandomStrategy()


def players_action_prompt(user_prompt: str) -> Tuple[PlayerStrategy, PlayerStrategy]:
    prompt =\
        """
Tengo la siguiente lista de estrategias de escoger las acciones durante el partido para los jugadores de mi simulación de fútbol 
y esta query definida por el usuario, del texto introducido por el usuario dime que estrategia de escoger acciones 
es la que desea el equipo local y cual es la que desea el visitador, con el siguiente formato: random vs minimax la 
de la izquierda es la estrategia del equipo local y la de la derecha es la estrategia del equipo visitador
"""

    strategies = {'random': RandomStrategy(
    ), 'heuristic': FootballStrategy(), 
    # 'minimax': MinimaxStrategy()
    }

    response = query(prompt+'\n'+'\n'.join(strategies.keys())+'\n'+user_prompt)

    try:
        home = response.split(' vs ')[0]
        away = response.split(' vs ')[1]

        return strategies[home], strategies[away]
    except:
        return FootballStrategy(), FootballStrategy()
