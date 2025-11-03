from .kpi import KPI
from typing import TYPE_CHECKING, Any, Dict

# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

class KR(KPI):
    
    def __init__(self, description: str, responsibleID: str, date: str, objectiveID: str, id:str = None, data: list[float] = None, goal: float = None):
        super().__init__(description, responsibleID, date, objectiveID, id, data)
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

    def getData(self, db: 'Database') -> Dict[str, Any]:
        """Retorna os dados deste KR (incluindo a meta)."""
        # 1. Pega o dicionário do pai (KPI), que já inclui
        #    id, desc, collectedData, lastValue.
        data_dict = super().getData(db)
        
        # 2. Adiciona/Atualiza campos específicos do KR
        data_dict.update({
            "type": "KR", # Sobrescreve o 'type' do KPI
            "goal": self.goal
        })
        return data_dict