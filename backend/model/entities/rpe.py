from .data import Data
from typing import TYPE_CHECKING

# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

class RPE(Data):

    def __init__(self, description: str, responsibleID: str, date :str, id:str = None):
        super().__init__(description, responsibleID, date, id)

    def getData(self, db: 'Database'):
        data = super().getData(db)

        # Busca filhos no banco
        objective_ids = db.getObjectivesByRPE(self.id)

        data["objectives"] = [
            db.getObjectiveByID(obj_id).getData(db)
            for obj_id in objective_ids
            if db.getObjectiveByID(obj_id)
        ]

        return data
