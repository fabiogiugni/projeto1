from group import Group

class Company(Group):
    def __init__(self, id : int, name : str, cnpj : str):
        super(id, name)
        self.__cnpj = cnpj
        self.__departmentIDs = []

    def addDepartment(self, departmentID : int):
        self.__departmentIDs.append(departmentID)