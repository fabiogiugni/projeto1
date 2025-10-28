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

    def createObjective(self, obj: Objective, rpeID: str, db: Database):
        if db.isRPETeamOrDepartmentLevel(rpeID):
            db.addItem(obj)
            db.addObjectiveToRpe(obj.id,rpeID)
        else:
            print("Erro ao adicionar objetivo: nível de acesso inválido.")
    
    def createKPI(self, kpi: KPI, objectiveID: str, db: Database):
        if db.isObjectiveTeamOrDepartmentLevel(kpi.id):
            db.addItem(kpi)
            db.addKpiToObjective(kpi.id,objectiveID)
        else:
            print("Erro ao adicionar KPI: nível de acesso inválido.")

    def createKR(self, kr: KR, objectiveID: str, db: Database):
        if db.isObjectiveTeamOrDepartmentLevel(kr.id):
            db.addItem(kr)
            db.addKpiToObjective(kr.id,objectiveID)
        else:
            print("Erro ao adicionar KR: nível de acesso inválido.")
    
    def deleteData(self, data: Data,db : Database):
        if(data.responsibleID == self.id):
            db.deleteItem(data)
        else:
            print("Erro ao deletar dado: nível de acesso inválido.")

    def collectIndicator(self, kpi: KPI, db : Database):
        if(kpi.responsibleID == self.id):
            db.updateItem(kpi)
        else:
            print("Erro ao coletar dado: nível de acesso inválido.")  