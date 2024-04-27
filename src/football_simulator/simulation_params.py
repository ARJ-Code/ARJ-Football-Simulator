from typing import Tuple
from football_agent.manager_line_up_strategy import ManagerLineUpStrategy
from football_agent.manager_action_strategy import ManagerActionStrategy


class SimulationParams:
    def __init__(self, names: Tuple[str, str], managers_line_up: Tuple[ManagerLineUpStrategy,  ManagerLineUpStrategy], managers_action_strategy: ManagerActionStrategy) -> None:
        self.names: Tuple[str, str] = names
        self.managers_line_up: Tuple[ManagerLineUpStrategy,
                                     ManagerLineUpStrategy] = managers_line_up
        self.managers_action: Tuple[ManagerActionStrategy,
                                    ManagerActionStrategy] = managers_action_strategy
