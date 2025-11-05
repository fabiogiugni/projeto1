from .entity import Entity
from typing import TYPE_CHECKING
# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

class Person(Entity):

    def __init__(self, name, cpf, companyID, departmentID=None, role: str = "Employee", teamID=None, email="", password="", id=None):
        super().__init__(id)
        self._name = name
        self._cpf = cpf
        self._role = role
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
    def role(self, role: str):
        """Setter para o cargo"""
        if not isinstance(role, str):
            raise TypeError("O nome deve ser uma string.")
        self._role = role

    @teamID.setter
    def teamID(self, teamID: str):
        """Setter para o teamID"""
        if not isinstance(teamID, str):
            raise TypeError("O nome deve ser uma string.")
        self._teamID = teamID

    def verifyPassword(self, password :str):
        if password == self.__password:
            return True
        else:
            return False
    
    def getData(self, group_type: str, group_id: str, data_type: str, db: 'Database'):
        """
        Retorna dados (RPE / Objective / KPI / KR) associados a Company, Department ou Team.
        """
        return db.getDataByEntity(group_type, group_id, data_type)
        