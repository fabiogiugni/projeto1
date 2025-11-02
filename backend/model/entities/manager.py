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

    def createObjective(self, obj: Objective, rpeID: str, db: 'Database'):
        if db.isRPETeamOrDepartmentLevel(rpeID):
            db.addItem(obj)
            db.addObjectiveToRpe(obj.id,rpeID)
        else:
            print("Erro ao adicionar objetivo: nível de acesso inválido.")

    def deleteObjective(self, obj: Objective, rpeID: str, db: 'Database'):
        if db.isRPETeamOrDepartmentLevel(rpeID):
            db.cleanupDataRelationships(obj.id, obj.__class__.__name__)
            db.deleteItemByObject(obj)
        else:
            print("Erro ao adicionar objetivo: nível de acesso inválido.")     
    
    def createKPI(self, kpi: KPI, objectiveID: str, db: 'Database'):
        if db.isObjectiveTeamOrDepartmentLevel(objectiveID):
            db.addItem(kpi)
            db.addKpiToObjective(objectiveID,kpi.id)
        else:
            print("Erro ao adicionar KPI: nível de acesso inválido.")

    def deleteKPI(self, kpi: KPI, objectiveID: str, db: 'Database'):
        if db.isObjectiveTeamOrDepartmentLevel(objectiveID):
            db.cleanupDataRelationships(kpi.id)
            db.deleteItemByObject(kpi)
        else:
            print("Erro ao adicionar objetivo: nível de acesso inválido.")

    def createKR(self, kr: KR, objectiveID: str, db: 'Database'):
        if db.isObjectiveTeamOrDepartmentLevel(objectiveID):
            db.addItem(kr)
            db.addKpiToObjective(objectiveID,kr.id)
        else:
            print("Erro ao adicionar KR: nível de acesso inválido.")
    
    def deleteKR(self, kr: KR, objectiveID: str, db: 'Database'):
        if db.isObjectiveTeamOrDepartmentLevel(objectiveID):
            db.cleanupDataRelationships(kr.id)
            db.deleteItemByObject(kr)
        else:
            print("Erro ao adicionar objetivo: nível de acesso inválido.")

    def collectIndicator(self, kpi: KPI, db: 'Database'):
        if(kpi.responsibleID == self.id):
            db.updateItem(kpi)
        else:
            print("Erro ao coletar dado: nível de acesso inválido.")

    def addResponsibleRpeId(self, rpdID: str, db: 'Database') -> None:
        self.__responsibleIDs.append(rpdID)
        db.updateItem(self)

    def deleteResponsibleRpeId(self, rpdID: str, db: 'Database') -> None:
        self.__responsibleIDs.remove(rpdID)
        db.updateItem(self)