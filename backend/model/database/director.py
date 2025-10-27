from person import Person
from database import Database
from rpe import RPE

class Director(Person):

    def __init__(self, responsibleIds: list[str], **kwargs):
        super().__init__(**kwargs)
        self.__responsibleIDs = responsibleIds

    def createItem(self, item, db: Database):
        db.addItem(item)

    def getDepartment(self, db: Database):
        return db.getDepartmentByID(self.departmentID)
    

