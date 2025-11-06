from .person import Person
from .rpe import RPE
from .objective import Objective
from .kr import KR
from .data import Data
from .kpi import KPI
from typing import TYPE_CHECKING

# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

class Manager(Person):

    def __init__(self, responsibleIds: list[str], **kwargs):
        super().__init__(**kwargs)
        self.__responsibleIDs = responsibleIds
        self._role = "Manager"

    def removeTeamEmployee(self, employeeID: str, db: 'Database'):
        db.unassignPersonToTeam(employeeID)

    def addTeamEmployee(self, employeeID: str, db: 'Database'):
        db.assignPersonToTeam(employeeID, self.teamID)

    def createObjective(self, obj: Objective, db: 'Database'):
        if db.isRPETeamOrDepartmentLevel(obj.rpeID):
            db.addItem(obj)
        else:
            print("Erro ao adicionar objetivo: nível de acesso inválido.")

    def deleteObjective(self, obj: Objective, db: 'Database'):
        if db.isRPETeamOrDepartmentLevel(obj.rpeID):
            db.deleteItemByObject(obj)
        else:
            print("Erro ao deletar objetivo: nível de acesso inválido.")     
    
    def createKPI(self, kpi: KPI, db: 'Database'):
        if db.isObjectiveTeamOrDepartmentLevel(kpi.objectiveID):
            db.addItem(kpi)
        else:
            print("Erro ao adicionar KPI: nível de acesso inválido.")

    def deleteKPI(self, kpi: KPI, db: 'Database'):
        if db.isObjectiveTeamOrDepartmentLevel(kpi.objectiveID):
            db.deleteItemByObject(kpi)
        else:
            print("Erro ao deletar KPI: nível de acesso inválido.")

    def createKR(self, kr: KR, db: 'Database'):
        if db.isObjectiveTeamOrDepartmentLevel(kr.objectiveID):
            db.addItem(kr)
        else:
            print("Erro ao adicionar KR: nível de acesso inválido.")
    
    def deleteKR(self, kr: KR, objectiveID: str, db: 'Database'):
        if db.isObjectiveTeamOrDepartmentLevel(objectiveID):
            db.deleteItemByObject(kr)
        else:
            print("Erro ao deletar KR: nível de acesso inválido.")

    def collectIndicator(self, kpi: KPI, novo_dado: float, db: 'Database'):
        if kpi.responsibleID == self.id:
            kpi.addData(novo_dado)
            db.updateItem(kpi)
        else:
            print("Erro ao coletar dado: nível de acesso inválido.")

    def addResponsibleRpeId(self, rpdID: str, db: 'Database') -> None:
        self.__responsibleIDs.append(rpdID)
        db.updateItem(self)

    def deleteResponsibleRpeId(self, rpdID: str, db: 'Database') -> None:
        self.__responsibleIDs.remove(rpdID)
        db.updateItem(self)