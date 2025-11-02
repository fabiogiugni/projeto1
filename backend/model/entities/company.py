from .group import Group

class Company(Group):

    def __init__(self, name: str, cnpj: str, id: str = None, RPEIDs: list[str] = None, departmentsIDs: list[str] = None, directorsIDs: list[str] = None):
        # Repassa id, name e rpeIds para o Group
        super().__init__(name,id,RPEIDs)
        self.__cnpj = cnpj
        self.__departmentsIds = departmentsIDs if departmentsIDs is not None else []
        self.__directorsIds = directorsIDs if directorsIDs is not None else []

    def addDepartment(self, departmentID : str):
        self.__departmentsIds.append(departmentID)

    def removeDepartment(self, departmentID : str):
        self.__departmentsIds.remove(departmentID)

    @property
    def directorsIDs(self):
        return self.__directorsIds

    @property
    def departmentIDs(self):
        return self.__departmentsIds

    @property
    def cnpj(self):
        return self.__cnpj