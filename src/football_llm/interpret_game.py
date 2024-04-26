from typing import List
from .llm import query


def interpret_game(history: List[str]) -> str:
    prompt =\
        """
Estoy simulando un partido de fútbol. Necesito que me interpretes de de forma el siguiente partido de fútbol
te voy a compartir la secuencia de instancias del juego. Cada casilla del campo puede ser de la siguiente manera
puede ser ** que indica que la casilla esta vacía, 23HB lo primero es el dorsal del jugador después H o A en dependencia
de si es el equipo local(H) o visitador(A) y luego una B indicando si tiene el balón ejemplo: 02H, 23A, 02HB, 10AB.
Abajo del campo están las estadísticas, a la izquierda el nombre del equipo local y a la derecha el nombre del equipo
visitante. Se están utilizando los datos del FIFA 22.
"""

    return query(prompt+'\n'.join(history[:1]))
