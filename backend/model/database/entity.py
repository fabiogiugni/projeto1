import uuid

class Entity:

    def __init__(self):
        self.__id = uuid.uuid4()

    @property
    def id(self):
        return self.__id