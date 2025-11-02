from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    cpf: str
    companyID: int
    departmentID: int
    teamID: int
    email: str
    password: str