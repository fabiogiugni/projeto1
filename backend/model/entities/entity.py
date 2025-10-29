import uuid

class Entity:

    def __init__(self):
        self._id = uuid.uuid4()

    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id