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
        db.deleteItem()

    def getDepartment(self, db: Database):
        return db.getDepartmentByID(self.departmentID)
    
    def changeTeamManager(self, teamID : str, personID: str, db : Database):
        db.changeTeamManager(teamID, personID)
    
    def changeDepartmentDirector(self, departmentID : str, personID: str, db : Database):
        db.changeTeamManager(departmentID, personID)