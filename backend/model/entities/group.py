from .entity import Entity

class Group(Entity):

    def __init__(self, name: str, id: str = None, RPEIDs: list[str] = None):
        super().__init__(id)
        self._name = name
        self._RPEIDs = RPEIDs if RPEIDs is not None else []

    def addRPE(self, RPEID : str):
        self._RPEIDs.append(RPEID)

    def deleteRPE(self, RPEID : str):
        self._RPEIDs.remove(RPEID)

    @property
    def RPEIDs(self):
        return self._RPEIDs

    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id