from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from model.entities.person import Person
from model.entities.director import Director
from model.entities.manager import Manager

from model.entities.company import Company
from model.entities.department import Department
from model.entities.team import Team

from model.database.database import Database

from .BaseModels.CompanyCreate import CompanyCreate
from .BaseModels.DepartmentCreate import DepartmentCreate
from .BaseModels.TeamCreate import TeamCreate
from .BaseModels.UserCreate import UserCreate

from .BaseModels.Login import Login

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


@app.get("/")
async def read_root():
    return {"message": "Backend Python funcionando!"}


# =====================
#         User
# =====================
@app.get("/user_by_email/{email}")
async def get_user_by_email(email : str):
  return {"data", DB.getPersonByEmail(email)}

@app.post("/login")
async def login(team : Login):
   user = DB.getPersonByEmail(Login.email)

   if user.verifyPassword(Login.password):
      return {"status": True} # Senha correta usuario logado
   else:
      return {"status" : False}

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


# =====================
#         RPE
# =====================

# get RPE by ID
@app.get("/RPE/{id}")
async def get_RPE(id : str):
  return { "data" : DB.getRPEByID(id) }

#get user RPE by id level (team, department, company)
@app.get("/user_RPE/{user_id}/{level}")
async def get_user_rpes(user_id: str, level: str):
    VALID_LEVELS = {"team", "department", "company"}
    
    if level not in VALID_LEVELS:
        raise HTTPException(
            status_code=400, 
            detail=f"Level deve ser um dos: {', '.join(VALID_LEVELS)}"
        )
    
    user = DB.getPersonByID(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    RPE = user.getRPE(level, DB)
    return {"data": RPE}

# =====================
#         Company
# =====================

# get company using cnpj
@app.get("/company/{cnpj}")
async def get_company(cnpj : str):
  return DB.getCompanyByCnpj(cnpj)

@app.post("/company")
async def create_company(company : CompanyCreate):
  new_company = Company(company.name, "123.123.123/45")
  print(f"Id da company: {new_company.id}")
  DB.addItem(new_company)
  return {"message": "Empresa criado com sucesso!"}

# =====================
#      Department
# =====================
@app.get("/get_department/{id}")
async def get_RPE(id : str):
  return {"data" : DB.getDepartmentByID(id)}

@app.post("/department")
async def create_department(department : DepartmentCreate):
  new_department = Department(department.name)
  new_department.companyID = department.companyID
  DB.addItem(new_department)
  return {"message": "Departamento criado com sucesso!"}

# =====================
#         Team
# =====================
@app.get("/get_team/{id}")
async def get_RPE(id : str):
  return {"data" : DB.getDepartmentByID(id)}

@app.post("/team")
async def create_team(team : TeamCreate):
  new_team = Team(team.name)
  new_team.departmentID = team.departmentID
  DB.addItem(new_team)
  return {"message": "Time criado com sucesso!"}

