from .person import Person
from .rpe import RPE
from .objective import Objective
from .kr import KR
from .data import Data
from .kpi import KPI

class Manager(Person):

    def __init__(self, responsibleIds: list[str], **kwargs):
        super().__init__(**kwargs)
        self.__responsibleIDs = responsibleIds

    def removeTeamEmployee(self, employeeID: str, db ):
        db.deleteTeamMember(self.teamID,employeeID)

    def addTeamEmployee(self, employeeID: str, db ):
        db.addTeamMember(self.teamID, employeeID)

    def createObjective(self, obj: Objective, rpeID: str, db):
        if db.isRPETeamOrDepartmentLevel(rpeID):
            db.addItem(obj)
            db.addObjectiveToRpe(obj.id,rpeID)
        else:
            print("Erro ao adicionar objetivo: nível de acesso inválido.")
    
    def createKPI(self, kpi: KPI, objectiveID: str, db):
        if db.isObjectiveTeamOrDepartmentLevel(objectiveID):
            db.addItem(kpi)
            db.addKpiToObjective(objectiveID,kpi.id)
        else:
            print("Erro ao adicionar KPI: nível de acesso inválido.")

    def createKR(self, kr: KR, objectiveID: str, db):
        if db.isObjectiveTeamOrDepartmentLevel(objectiveID):
            db.addItem(kr)
            db.addKpiToObjective(objectiveID,kr.id)
        else:
            print("Erro ao adicionar KR: nível de acesso inválido.")
    
    def deleteData(self, data: Data,db ):
        if(data.responsibleID == self.id):
            db.deleteItemByObject(data)
        else:
            print("Erro ao deletar dado: nível de acesso inválido.")

    def collectIndicator(self, kpi: KPI, db ):
        if(kpi.responsibleID == self.id):
            db.updateItem(kpi)
        else:
            print("Erro ao coletar dado: nível de acesso inválido.")  