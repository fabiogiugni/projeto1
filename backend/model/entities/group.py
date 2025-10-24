
class Group:
    def __init__(self, id : str, name : str):
        self.__id = id
        self.__name = name
        self.__RPEIDs = []

    def addRPE(self, RPEID : str):
        self.__RPEIDs.append(RPEID)

    def deleteRPE(self, RPEID : str):
        self.__RPEIDs.remove(RPEID)

    @property
    def RPEIDs(self):
        return self.__RPEIDs

    @property
    def name(self):
        return self.__name
    
    @property
    def id(self):
        return self.__id