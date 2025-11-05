from .person import Person
from .department import Department
from .team import Team
from .rpe import RPE
from .objective import Objective
from .kr import KR
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
    
    def createDepartment(self, department: Department, db: 'Database'):
        db.addItem(department)
        
    def deleteDepartment(self, department: Department, db: 'Database'):
        db.deleteItemByObject(department)

    def createTeam(self, team: Team, db: 'Database'):
        db.addItem(team)

    def deleteTeam(self, team: Team, db: 'Database'):
        db.deleteItemByObject(team)

    def createUser(self, person: Person, db: 'Database'):
        db.addItem(person)

    def deleteUser(self, person: Person, db: 'Database'):
        db.deleteItemByObject(person)
    
    def createRPE(self, rpe: RPE, groupLevel: str, db: 'Database'):
        person = db.getPersonByID(rpe.responsibleID)
        if groupLevel == "Company":
            db.addItem(rpe)
            db.addRpeToCompany(person.companyID,rpe.id)
        elif groupLevel == "Department":
            db.addItem(rpe)
            db.addRpeToDepartment(person.departmentID,rpe.id)
        elif groupLevel == "Team":
            db.addItem(rpe)
            db.addRpeToTeam(person.teamID,rpe.id)
        else:
            print("Group level inválido.")
    
    def deleteRPE(self, rpe: RPE, db: 'Database'):
        db.deleteItemByObject(rpe)

    def getDepartment(self, db: 'Database'):
        return db.getDepartmentByID(self.departmentID)
    
    def changeTeamManager(self, teamID : str, personID: str, db: 'Database'):
        db.changeTeamManager(teamID, personID)
    
    def changeDepartmentDirector(self, departmentID : str, personID: str, db: 'Database'):
        db.changeDepartmentDirector(departmentID, personID)
    
    def createObjective(self, obj: Objective, db: 'Database'):
        db.addItem(obj)

    def deleteObjective(self, obj: Objective, db: 'Database'):
        db.deleteItemByObject(obj)     
    
    def createKPI(self, kpi: KPI, db: 'Database'):
        db.addItem(kpi)

    def deleteKPI(self, kpi: KPI, db: 'Database'):
        db.deleteItemByObject(kpi)

    def createKR(self, kr: KR, db: 'Database'):
        db.addItem(kr)
    
    def deleteKR(self, kr: KR, db: 'Database'):
        db.deleteItemByObject(kr)

    def collectIndicator(self, kpi: KPI, db: 'Database'):
        db.updateItem(kpi)

    def addResponsibleRpeId(self, rpdID: str, db: 'Database') -> None:
        self.__responsibleIDs.append(rpdID)
        db.updateItem(self)

    def deleteResponsibleRpeId(self, rpdID: str, db: 'Database') -> None:
        self.__responsibleIDs.remove(rpdID)
        db.updateItem(self)