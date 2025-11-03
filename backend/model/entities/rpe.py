from .data import Data
from typing import TYPE_CHECKING, Any, Dict, List

# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

class RPE(Data):

    def __init__(self, description: str, responsibleID: str, date :str, id:str = None, objectiveIds: list[str] = None):
        super().__init__(description, responsibleID, date, id)
        self.__objectiveIds = objectiveIds if objectiveIds is not None else []
    
    def addObjective(self, objectiveID: str, db: 'Database'):
        self.__objectiveIds.append(objectiveID)
        db.updateItem(self)

    def deleteObjective(self, objectiveID: str, db: 'Database'):
        self.__objectiveIds.remove(objectiveID)
        db.updateItem(self)

    def getData(self, db: 'Database') -> Dict[str, Any]:
        """
        Retorna os dados do RPE e, recursivamente, 
        os dados de seus Objetivos filhos.
        """
        # 1. Pega o dicionário base (id, desc, etc.)
        data_dict = super().getData(db)

        # 2. Processa Objetivos filhos
        objective_data_list: List[Dict[str, Any]] = []
        for obj_id in self.__objectiveIds:
            obj = db.getObjectiveByID(obj_id) # Requer DB
            if obj:
                # A chamada recursiva acontece aqui
                objective_data_list.append(obj.getData(db)) 
        
        # 3. Adiciona a lista ao dicionário principal
        data_dict.update({
            "objectives": objective_data_list
        })
        return data_dict