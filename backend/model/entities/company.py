from group import Group

class Company(Group):
    def __init__(self, id : str, name : str, cnpj : str):
        super().__init__(id, name)
        self.__cnpj = cnpj
        self.__departmentIDs = []

    def addDepartment(self, departmentID : str):
        self.__departmentIDs.append(departmentID)

    def removeDepartment(self, departmentID : str):
        self.__departmentIDs.remove(departmentID)

    @property
    def departmentIDs(self):
        return self.__departmentIDs

    @property
    def cnpj(self):
        return self.__cnpj