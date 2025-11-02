from .data import Data
from typing import TYPE_CHECKING, Any, Dict, List

# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

class Objective(Data):

    def __init__(self, description: str, responsibleID: str, date: str, id:str = None, kpiIds: list[str] = None, krIds: list[str] = None):
        super().__init__(description, responsibleID, date, id)
        self.__kpiIds = kpiIds if kpiIds is not None else []
        self.__krIds = krIds if krIds is not None else []
    
    def addKpi(self, kpiID: str, db: 'Database'):
        self.__kpiIds.append(kpiID)
        db.updateItem(self)

    def deleteKpi(self, kpiID: str, db: 'Database'):
        self.__kpiIds.remove(kpiID)
        db.updateItem(self)

    def addKr(self, krID: str, db: 'Database'):
        self.__krIds.append(krID)
        db.updateItem(self)

    def deleteKr(self, krID: str, db: 'Database'):
        self.__krIds.remove(krID)
        db.updateItem(self)
        

    def getData(self, db: 'Database') -> Dict[str, Any]:
        """
        Retorna os dados do Objetivo e, recursivamente, 
        os dados de seus KPIs e KRs filhos.
        """
        # 1. Pega o dicionário base (id, desc, etc.)
        data_dict = super().getData(db)

        # 2. Processa KPIs filhos
        kpi_data_list: List[Dict[str, Any]] = []
        for kpi_id in self.__kpiIds:
            kpi_obj = db.getKPIByID(kpi_id) # Requer DB
            if kpi_obj:
                kpi_data_list.append(kpi_obj.getData(db)) # Chamada recursiva
        
        # 3. Processa KRs filhos
        kr_data_list: List[Dict[str, Any]] = []
        for kr_id in self.__krIds:
            kr_obj = db.getKRByID(kr_id) # Requer DB
            if kr_obj:
                kr_data_list.append(kr_obj.getData(db)) # Chamada recursiva

        # 4. Adiciona as listas ao dicionário principal
        data_dict.update({
            "kpis": kpi_data_list,
            "krs": kr_data_list
        })
        return data_dict