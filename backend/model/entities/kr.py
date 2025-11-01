from .kpi import KPI
from datetime import datetime

class KR(KPI):
    
    def __init__(self, description: str, responsibleID: str, date: str, id:str = None, data: list[float] = None, goal: float = None):
        super().__init__(description, responsibleID, date, id, data)
        self.__goal = goal if goal is not None else 0

    @property
    def goal(self):
        return self.__goal
    
    @goal.setter
    def goal(self, goal: float):
        """Setter para goal"""
        if not isinstance(goal, float):
            raise TypeError("O 'goal' (meta) deve ser um float.")
        self.__goal = goal