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
    
    def getRPEs(self, entity_type: str, entity_id: str, db: 'Database'):
        """
        Busca RPEs associados a qualquer Team, Department ou Company,
        independente de ser o da própria pessoa.
        """
        return db.getRPEsByEntity(entity_type, entity_id)