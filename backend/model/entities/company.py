from .group import Group

class Company(Group):

    def __init__(self, name: str, cnpj: str, id: str = None, rpeIds: list[str] = None, departmentsIds: list[str] = None, directorsIds: list[str] = None):
        # Repassa id, name e rpeIds para o Group
        super().__init__(name,id,rpeIds)
        self.__cnpj = cnpj
        self.__departmentsIds = departmentsIds if departmentsIds is not None else []
        self.__directorsIds = directorsIds if directorsIds is not None else []

    def addDepartment(self, departmentID : str):
        self.__departmentsIds.append(departmentID)

    def removeDepartment(self, departmentID : str):
        self.__departmentsIds.remove(departmentID)

    @property
    def directorsIds(self):
        return self.__directorsIds

    @property
    def departmentIDs(self):
        return self.__departmentsIds

    @property
    def cnpj(self):
        return self.__cnpj