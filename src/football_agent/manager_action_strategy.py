from abc import ABC, abstractmethod
from .simulator_agent import SimulatorAgent


class ManagerActionStrategy(ABC):
    @abstractmethod
    def action(simulator: SimulatorAgent):
        pass
