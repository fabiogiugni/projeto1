from person import Person
from ..database.database import Database
from rpe import RPE

class Director(Person):

    def __init__(self, responsibleIds: list[str], **kwargs):
        super().__init__(**kwargs)
        self.__responsibleIDs = responsibleIds
        self._role = "Director"

    def createItem(self, item, db: Database): #User, team, department...
        db.addItem(item)
    
    def deleteItem(self, item, db: Database): #User, team, department...
        db.deleteItemByObject(item)

    def getDepartment(self, db: Database):
        return db.getDepartmentByID(self.departmentID)
    
    def changeTeamManager(self, teamID : str, personID: str, db : Database):
        db.changeTeamManager(teamID, personID)
    
    def changeDepartmentDirector(self, departmentID : str, personID: str, db : Database):
        db.changeDepartmentDirector(departmentID, personID)
    
    def createObjective(self, obj: Objective, rpeID: str, db: Database):
        db.addItem(obj)
        db.addObjectiveToRpe(obj.id,rpeID)
    
    def createKPI(self, kpi: KPI, objectiveID: str, db: Database):
        db.addItem(kpi)
        db.addKpiToObjective(objectiveID,kpi.id)

    def createKR(self, kr: KR, objectiveID: str, db: Database):
        db.addItem(kr)
        db.addKpiToObjective(objectiveID,kr.id)
    
    def deleteData(self, data: Data,db : Database):
        db.deleteItemByObject(data)

    def collectIndicator(self, kpi: KPI, db : Database):
        db.updateItem(kpi)