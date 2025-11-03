from .entity import Entity
from typing import TYPE_CHECKING
# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

class Person(Entity):
    name: str
    cpf: str
    companyID: int
    departmentID: int
    teamID: int
    email: str
    password: str

    def __init__(self, name:str, cpf:str, companyID: str, departmentID: str, teamID: str, email: str, password: str, id:str = None):
        super().__init__(id)
        self._name = name
        self._cpf = cpf
        self._role = "Employee"
        self._companyID = companyID
        self._departmentID = departmentID
        self._teamID = teamID
        self.__email = email
        self.__password = password
    
    @property
    def name(self):
        return self._name
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def role(self):
        return self._role

    @property
    def companyID(self):
        return self._companyID
    
    @property
    def departmentID(self):
        return self._departmentID
    
    @property
    def teamID(self):
        return self._teamID
    
    @property
    def email(self):
        return self.__email
    
    @property
    def password(self):
        return self.__password
    
    #Fazer todas operações sobre dado na própria classe, apenas busca e atualiza coisas no bd

    @role.setter
    def role(self, role: str, db: 'Database'):
        """Setter para o cargo"""
        if not isinstance(role, str):
            raise TypeError("O nome deve ser uma string.")
        self._role = role
        db.updateItem(self)

    @teamID.setter
    def teamID(self, teamID: str, db: 'Database'):
        """Setter para o teamID"""
        if not isinstance(teamID, str):
            raise TypeError("O nome deve ser uma string.")
        self._teamID = teamID
        db.updateItem(self)

    def verifyPassword(self, password :str):
        if password == self.__password:
            return True
        else:
            return False
    
    def getRPEs(self, filter: str, db: 'Database'):
        """
        Retorna as RPEs associadas a uma Company, Department ou Team cujo nome corresponda ao filtro.
        """
        # 1) Tentamos Company
        company = db.getCompanyByName(filter)
        if company is not None:
            rpes = []
            for rpe_id in company.RPEIDs:
                rpe = db.getRPEByID(rpe_id)
                if rpe:
                    rpes.append(rpe)
            return rpes

        # 2) Tentamos Department
        department = db.getDepartmentByName(filter)
        if department is not None:
            rpes = []
            for rpe_id in department.rpeIds:
                rpe = db.getRPEByID(rpe_id)
                if rpe:
                    rpes.append(rpe)
            return rpes

        # 3) Tentamos Team
        team = db.getTeamByName(filter)
        if team is not None:
            rpes = []
            for rpe_id in team.rpesIDs:
                rpe = db.getRPEByID(rpe_id)
                if rpe:
                    rpes.append(rpe)
            return rpes

        # 4) Nenhum match
        print(f"[AVISO] Nenhuma Company, Department ou Team encontrado com nome '{filter}'.")
        return []
