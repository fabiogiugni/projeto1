from group import Group

class Company(Group):

    def __init__(self, name: str, cnpj: str, id: str = None, RPEIDs: list[str] = None, departmentIDs: list[str] = None, directorsIDs: list[str] = None):
        # Repassa id, name e RPEIDs para o Group
        super().__init__(name,id,RPEIDs)
        self.__cnpj = cnpj
        self.__departmentIDs = departmentIDs if departmentIDs is not None else []
        self.__directorsIDs = directorsIDs if directorsIDs is not None else []

    def addDepartment(self, departmentID : str):
        self.__departmentIDs.append(departmentID)

    def removeDepartment(self, departmentID : str):
        self.__departmentIDs.remove(departmentID)

    @property
    def directorsIDs(self):
        return self.__directorsIDs

    @property
    def departmentIDs(self):
        return self.__departmentIDs

    @property
    def cnpj(self):
        return self.__cnpj