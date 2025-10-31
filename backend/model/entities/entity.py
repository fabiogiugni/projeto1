import uuid

class Entity:

    def __init__(self, id=None):
        self._id = str(id) if id is not None else uuid.uuid4()

    @property
    def id(self):
        return self._id