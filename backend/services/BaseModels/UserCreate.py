from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    cpf: str
    companyID: str
    departmentID: Optional[str] = None
    teamID: Optional[str] = None
    email: str
    password: str