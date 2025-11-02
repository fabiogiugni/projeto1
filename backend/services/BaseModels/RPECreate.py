from pydantic import BaseModel


class RPECreate(BaseModel):
    description: str
    responsibleID : str