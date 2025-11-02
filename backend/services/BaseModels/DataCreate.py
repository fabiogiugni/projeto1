from pydantic import BaseModel


class DataCreate(BaseModel):
    description: str
    responsibleID : str
    date: str # 