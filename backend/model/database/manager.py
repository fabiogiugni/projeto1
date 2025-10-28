from person import Person
from database import Database

class Manager(Person):

    def __init__(self, responsibleIds: list[str], **kwargs):
        super().__init__(**kwargs)
        self.__responsibleIDs = responsibleIds

    def removeTeamEmployee(self, employeeID: str, db : Database):
        db.deleteTeamMember(self.teamID,employeeID)

    def addTeamEmployee(self, employeeID: str, db : Database):
        db.addTeamMember(self.teamID, employeeID)

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