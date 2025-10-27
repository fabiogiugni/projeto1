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