from pydantic import BaseModel


class KRCreate(BaseModel):
    description: str
    responsibleID : str
    date: str # 
    goal : float