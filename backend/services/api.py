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

from model.entities.rpe import RPE
from model.entities.kr import KR
from model.entities.kpi import KPI
from model.entities.objective import Objective

from model.database.database import Database

from .BaseModels.CompanyCreate import CompanyCreate
from .BaseModels.DepartmentCreate import DepartmentCreate
from .BaseModels.TeamCreate import TeamCreate
from .BaseModels.UserCreate import UserCreate
from .BaseModels.Login import Login
from .BaseModels.DataCreate import DataCreate
from .BaseModels.KRCreate import KRCreate
from .BaseModels.DataAdd import DataAdd
from .BaseModels.KRUpdate import KRUpdate

from datetime import datetime

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

# create RPE
@app.post("/RPE")
async def create_RPE(rpe : DataCreate):
    date = datetime.strptime(rpe.date, "%Y-%m-%d")

    new_rpe = RPE(rpe.description, rpe.responsibleID, date)
    print(f"Id do rpe: {new_rpe.id}")
    DB.addItem(new_rpe)

    return {"message": "RPE criado com sucesso!", "id": new_rpe.id}

@app.post("/objective")
async def create_obective(objective : DataCreate):
    date = datetime.strptime(objective.date, "%Y-%m-%d")

    rpe = DB.getRPEByID(objective.RPEId)

    new_objective = Objective(objective.description, objective.responsibleID, date)
    rpe.addObjective(new_objective)
    DB.updateItem(rpe)

    print(f"Id do objective: {new_objective.id}")
    DB.addItem(new_objective)

    return {"message": "Objetivo criado com sucesso!", "id": new_objective.id}

@app.post("/kr")
async def create_obective(kr : KRCreate):
    date = datetime.strptime(kr.date, "%Y-%m-%d")

    objective = DB.getObjectiveByID(kr.objectiveID)

    new_kr = KR(kr.description, kr.responsibleID, date)
    new_kr.goal = kr.goal
    objective.addKr(new_kr)
    DB.updateItem(objective)

    print(f"Id do objective: {new_kr.id}")
    DB.addItem(new_kr)

    return {"message": "KR criado com sucesso!", "id": new_kr.id}

@app.post("/kpi")
async def create_obective(kpi : DataCreate):
    date = datetime.strptime(kpi.date, "%Y-%m-%d")

    objective = DB.getObjectiveByID(kpi.objectiveID)

    new_kpi = KPI(kpi.description, kpi.responsibleID, date)
    objective.addKpi(new_kpi)
    DB.updateItem(objective)

    print(f"Id do objective: {new_kpi.id}")
    DB.addItem(new_kpi)

    return {"message": "KPI criado com sucesso!", "id": new_kpi.id}

@app.put("/kr_goal/{id}")
async def change_kr_goal(id : str, kr_data : KRUpdate):
   kr = DB.getKRByID(id)
   if kr == None:
      raise HTTPException(status_code=404, detail="KR não encontrado")
   else:
   
    kr.goal = kr_data.goal

    DB.updateItem(kr)

    return {"message" : "kr atualizado com sucesso"}

@app.put("/kr_data/{id}")
async def change_kr_goal(id : str, kr_data : DataAdd):
   kr = DB.getKRByID(id)
   if kr == None:
      raise HTTPException(status_code=404, detail="KR não encontrado")
   else:
    kr.addData(kr_data.data)
    DB.updateItem(kr)

   return {"message" : "kr atualizado com sucesso"}

@app.put("/kpi_data/{id}")
async def change_kpi_goal(id : str, kpi_data : DataAdd):
    kpi = DB.getKPIByID(id)
    if kpi == None:
        raise HTTPException(status_code=404, detail="KPI não encontrado")
   
    kpi.addData(kpi_data.data)
    DB.updateItem(kpi)

    return {"message" : "kpi atualizado com sucesso"}

# =====================
#         Company
# =====================

# get company using cnpj
@app.get("/company/{cnpj}")
async def get_company(cnpj : str):
  return DB.getCompanyByCnpj(cnpj)

@app.post("/company")
async def create_company(company : CompanyCreate):
  new_company = Company(company.name, company.cnpj)
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


# Deleta Item qualquer

@app.delete("/delete/{id}")
async def delete_rpe(id : str):
    if DB.deleteItembyID(id) == False:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    else:
        return {"message" : "item deletado com sucesso"}


