from pydantic import BaseModel

class DepartmentCreate(BaseModel):
    name: str
    companyID : str
    directorID: str