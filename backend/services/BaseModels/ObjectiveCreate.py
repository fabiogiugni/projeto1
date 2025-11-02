from pydantic import BaseModel


class ObjectiveCreate(BaseModel):
    description: str
    responsibleID : str
    RPEID: str