import uuid

class Entity:

    def __init__(self):
        self.__id = uuid.uuid4()

    def __init__(self, id):
        self.__id = id

    @property
    def id(self):
        return self.__id