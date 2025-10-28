from person import Person
from database import Database
from rpe import RPE

class Director(Person):

    def __init__(self, responsibleIds: list[str], **kwargs):
        super().__init__(**kwargs)
        self.__responsibleIDs = responsibleIds

    def createItem(self, item, db: Database): #User, team, department...
        db.addItem(item)
    
    def deleteItem(self, item, db: Database): #User, team, department...
        db.deleteItem(item)

    def getDepartment(self, db: Database):
        return db.getDepartmentByID(self.departmentID)
    
    def changeTeamManager(self, teamID : str, personID: str, db : Database):
        db.changeTeamManager(teamID, personID)
    
    def changeDepartmentDirector(self, departmentID : str, personID: str, db : Database):
        db.changeTeamManager(departmentID, personID)
    
    def createObjective(obj: Objective, rpeID: str, db: Database):
        db.addItem(obj)
        db.addObjectiveToRpe(obj.id,rpeID)
    
    def createKPI(kpi: KPI, objectiveID: str, db: Database):
        db.addItem(kpi)
        db.addKpiToObjective(kpi.id,objectiveID)

    def createKR(kr: KR, objectiveID: str, db: Database):
        db.addItem(kr)
        db.addKpiToObjective(kr.id,objectiveID)
    
    def deleteData(data: Data,db : Database):
        db.deleteItem(data)

    def collectIndicator(kpi: KPI, db : Database):
        db.updateItem(kpi)