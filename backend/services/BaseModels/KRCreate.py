from pydantic import BaseModel


class KRCreate(BaseModel):
    description: str
    responsibleID : str
    goal : float
    objectiveID: str