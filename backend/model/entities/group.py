
class Group:
    def __init__(self, id : int, name : str):
        self.__id = id
        self.__name = name
        self.__RPEIDs = []

    def addRPE(self, RPEID : int):
        self.__RPEIDs.append(RPEID)

    @property
    def name(self):
        return self.__name
    
    @property
    def id(self):
        return self.__id