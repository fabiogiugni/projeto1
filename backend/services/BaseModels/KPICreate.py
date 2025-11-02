from pydantic import BaseModel


class KPICreate(BaseModel):
    description: str
    responsibleID : str
    ObjectiveId: str