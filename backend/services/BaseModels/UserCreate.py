from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    cpf: str
    companyID: str
    departmentID: str
    teamID: str
    email: str
    password: str