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

class Director(Person):

    def __init__(self, responsibleIds: list[str], **kwargs):
        super().__init__(**kwargs)
        self.__responsibleIDs = responsibleIds
        self._role = "Director"

    def createUser(self, person: Person, db: 'Database'):
        db.addItem(person)
        db.assignPersonToCompany(person.id,person.companyID)
        db.assignPersonToDepartment(person.id,person.departmentID)
        db.assignPersonToTeam(person.id,person.teamID)

    def deleteUser(self, person: Person, db: 'Database'):
        db.deleteItemByObject(person)
        db.unassignPersonToCompany(person.id)
        db.unassignPersonToDepartment(person.id)
        db.unassignPersonToTeam(person.id)

    def getDepartment(self, db: 'Database'):
        return db.getDepartmentByID(self.departmentID)
    
    def changeTeamManager(self, teamID : str, personID: str, db: 'Database'):
        db.changeTeamManager(teamID, personID)
    
    def changeDepartmentDirector(self, departmentID : str, personID: str, db: 'Database'):
        db.changeDepartmentDirector(departmentID, personID)
    
    def createObjective(self, obj: Objective, rpeID: str, db: 'Database'):
        db.addItem(obj)
        db.addObjectiveToRpe(obj.id,rpeID)

    def deleteObjective(self, obj: Objective, db: 'Database'):
        db.cleanupDataRelationships(obj.id, obj.__class__.__name__)
        db.deleteItemByObject(obj)
    
    def createKPI(self, kpi: KPI, objectiveID: str, db: 'Database'):
        db.addItem(kpi)
        db.addKpiToObjective(objectiveID,kpi.id)

    def deleteKPI(self, kpi: KPI, db: 'Database'):
        db.cleanupDataRelationships(kpi.id)
        db.deleteItemByObject(kpi)

    def createKR(self, kr: KR, objectiveID: str, db: 'Database'):
        db.addItem(kr)
        db.addKpiToObjective(objectiveID,kr.id)
    
    def deleteKR(self, kr:KR, db: 'Database'):
        db.cleanupDataRelationships(kr.id)
        db.deleteItemByObject(kr)

    def collectIndicator(self, kpi: KPI, db: 'Database'):
        db.updateItem(kpi)

    def addResponsibleRpeId(self, rpdID: str, db: 'Database') -> None:
        self.__responsibleIDs.append(rpdID)
        db.updateItem(self)

    def deleteResponsibleRpeId(self, rpdID: str, db: 'Database') -> None:
        self.__responsibleIDs.remove(rpdID)
        db.updateItem(self)