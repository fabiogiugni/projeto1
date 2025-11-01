from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from pydantic import BaseModel

from model.entities.person import Person
from model.entities.director import Director
from model.entities.manager import Manager

from model.entities.company import Company
from model.entities.department import Department
from model.entities.team import Team

from model.database.database import Database
  
class UserCreate(BaseModel):
    name: str
    cpf: str
    companyID: int
    departmentID: int
    teamID: int
    email: str
    password: str

class CompanyCreate(BaseModel):
    name: str
    cnpj: str

class TeamCreate(BaseModel):
    name: str
    departmentID : str

class DepartmentCreate(BaseModel):
    name: str
    companyID : str

app = FastAPI(title="Backend API")

# Configurar CORS para permitir requisições do React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL do React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB = Database("teste.db")

class CompanyCreate(BaseModel):
    name: str
    cnpj: str


@app.get("/")
async def read_root():
    return {"message": "Backend Python funcionando!"}

@app.get("/RPE/{id}")
async def get_RPE(id : str):
  return DB.getByID(id)

@app.get("/company/")
async def get_company(id : str):
  return DB.getCompanyByID(id)
  

@app.post("/user")
async def create_user(user: UserCreate):
    id = 1  # mudar depois
    new_user = Person(
        user.name,
        user.cpf,
        user.companyID,
        user.departmentID,
        user.teamID,
        user.email,
        user.password
    )
    DB.addItem(new_user)
    return {"message": "Usuário criado com sucesso!"}

@app.post("/company")
async def create_company(company : CompanyCreate):
  new_company = Company(company.name, "123.123.123/45")
  print(f"Id da company: {new_company.id}")
  DB.addItem(new_company)
  return {"message": "Empresa criado com sucesso!"}

@app.post("/department")
async def create_department(department : DepartmentCreate):
  new_department = Department(department.name)
  new_department.companyID = department.companyID
  DB.addItem(new_department)
  return {"message": "Departamento criado com sucesso!"}

@app.post("/team")
async def create_team(team : TeamCreate):
  new_team = Team(team.name)
  new_team.departmentID = team.departmentID
  DB.addItem(new_team)
  return {"message": "Time criado com sucesso!"}
  

def main():
  print("🚀 Iniciando servidor FastAPI...")
  print("🛑 Use Ctrl+C para parar o servidor\n")

  #uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
  main()