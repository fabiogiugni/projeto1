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
from .BaseModels.RPECreate import RPECreate
from .BaseModels.KPICreate import KPICreate
from .BaseModels.ObjectiveCreate import ObjectiveCreate
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
    user = DB.getPersonByEmail(email)
    if user == None:
        raise HTTPException(
            status_code=404, 
            detail=f"Usuário não encontrado"
        )
    return {"data", user}

@app.post("/login")
async def login(team : Login):
   user = DB.getPersonByEmail(Login.email)

   if user.verifyPassword(Login.password):
      return {"status": True} # Senha correta usuario logado
   else:
      return {"status" : False}
   
@app.get("/user_by_id/{id}")
async def get_user_by_email(id : str):
    user = DB.getPersonByID(id)
    if user == None:
        raise HTTPException(
            status_code=404, 
            detail=f"Usuário não encontrado"
        )
    else:
        return {"data", user}

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

@app.put("/user_role/{id}/{role}")
async def change_role(id :str, role : str):
    user = DB.getPersonByID(id)

    if user == None:
        raise HTTPException(
            status_code=404, 
            detail=f"Usuário não encontrado"
        )
    else:
        user.role = role
        DB.updateItem(user)
        return {"message": "Cargo mudado com sucesso"}




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
async def create_RPE(rpe : RPECreate):
    date = datetime.now()

    new_rpe = RPE(rpe.description, rpe.responsibleID, date)
    print(f"Id do rpe: {new_rpe.id}")
    DB.addItem(new_rpe)

    return {"message": "RPE criado com sucesso!", "id": new_rpe.id}

@app.post("/objective")
async def create_obective(objective : ObjectiveCreate):
    date = datetime.now()

    rpe = DB.getRPEByID(objective.RPEID)
    if rpe == None:
       raise HTTPException(
            status_code=404, 
            detail=f"RPE nao encontrado"
        )
    else:
        new_objective = Objective(objective.description, objective.responsibleID, date)
        rpe.addObjective(new_objective)
        DB.updateItem(rpe)

        print(f"Id do objective: {new_objective.id}")
        DB.addItem(new_objective)

        return {"message": "Objetivo criado com sucesso!", "id": new_objective.id}

@app.post("/kr")
async def create_kr(kr : KRCreate):
    date = datetime.now()

    objective = DB.getObjectiveByID(kr.objectiveID)

    new_kr = KR(kr.description, kr.responsibleID, date)
    new_kr.goal = kr.goal
    objective.addKr(new_kr)
    DB.updateItem(objective)

    print(f"Id do objective: {new_kr.id}")
    DB.addItem(new_kr)

    return {"message": "KR criado com sucesso!", "id": new_kr.id}

@app.post("/kpi")
async def create_kpi(kpi : KPICreate):
    date = datetime.now()

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

@app.put("/company_rpe/{rpe_id}/{company_id}")
async def add_company_rpe(rpe_id : str, company_id : str):
   rpe = DB.getRPEByID(rpe_id)
   if rpe == None:
        raise HTTPException(status_code=404, detail="RPE não encontrado")
   company = DB.getCompanyByID(company_id)
   if company == None:
        raise HTTPException(status_code=404, detail="Empresa não encontrado")
   
   company.addRPE(rpe.id)

   DB.updateItem(rpe)
   DB.updateItem(company)

   return {"message" : "RPE Adcionado com sucesso"}

@app.put("/department_rpe/{rpe_id}/{department_id}")
async def add_company_rpe(rpe_id : str, department_id : str):
   rpe = DB.getRPEByID(rpe_id)
   if rpe == None:
        raise HTTPException(status_code=404, detail="RPE não encontrado")
   department = DB.getDepartmentByID(department_id)
   if department == None:
        raise HTTPException(status_code=404, detail="Deprtamento não encontrado")
   
   department.addRPE(rpe.id)
   print("<<TESTE>>", department.RPEIDs)

   DB.updateItem(rpe)
   DB.updateItem(department)

   return {"message" : "RPE Adcionado com sucesso"}

@app.put("/team_rpe/{rpe_id}/{team_id}")
async def add_company_rpe(rpe_id : str, team_id : str):
   rpe = DB.getRPEByID(rpe_id)
   if rpe == None:
        raise HTTPException(status_code=404, detail="RPE não encontrado")
   team = DB.getTeamByID(team_id)
   if team == None:
        raise HTTPException(status_code=404, detail="Equipe não encontrado")
   
   team.addRPE(rpe.id)

   DB.updateItem(rpe)
   DB.updateItem(team)

   return {"message" : "RPE Adcionado com sucesso"}


# =====================
#         Company
# =====================

# get company using cnpj
@app.get("/company/{cnpj}")
async def get_company(cnpj : str):
  company = DB.getCompanyByCnpj(cnpj)
  return {"data" : company}
  #return {"id": company.id, "name" : company.name, "cnpj": company.cnpj, "departments" : company.departmentIDs, "directors": company.directorsIds}

@app.post("/company")
async def create_company(company : CompanyCreate):
  new_company = Company(company.name, company.cnpj)
  print(f"Id da company: {new_company.id}")
  DB.addItem(new_company)
  return {"message": "Empresa criado com sucesso!"}

@app.get("/department_users/{id}")
async def get_department_users(id : str):
    dep = DB.getDepartmentByID(id)

    if dep == None:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")
    usersIDS = []
    usersIDS.append(dep.directorID())

    for team_id in dep.teamIds:
        team = DB.getTeamByID(team_id)
        if team.managerID not in usersIDS:
            usersIDS.append(team.managerID)
        
        for employee_id in team.employeeIds:
            if employee_id not in usersIDS:
                usersIDS.append(DB.getPersonByID(employee_id))
    users = []
    for user in users:
        users.append(user)

    return {"data" : users}

@app.get("/company_departments/{id}")
async def get_company_departments(id : str):
    company = DB.getCompanyByID(id)

    if company == None:
        raise HTTPException(status_code=404, detail="Empresa não encontrado")
    departmentsIDS = company.departmentIds
    departments = []

    for department_id in departmentsIDS:
        departments.append(DB.getTeamByID(department_id))

    return {"data" : departments}

# =====================
#      Department
# =====================
@app.get("/department/{id}")
async def get_department(id : str):
  return {"data" : DB.getDepartmentByID(id)}

@app.post("/department")
async def create_department(department : DepartmentCreate):
  new_department = Department(department.name, companyID=department.companyID)

  DB.addItem(new_department)
  return {"message": "Departamento criado com sucesso!"}

@app.get("/department_users/{id}")
async def get_department_users(id : str):
    dep = DB.getDepartmentByID(id)

    if dep == None:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")
    usersIDS = []
    usersIDS.append(dep.directorID())

    for team_id in dep.teamIds:
        team = DB.getTeamByID(team_id)
        if team.managerID not in usersIDS:
            usersIDS.append(team.managerID)
        
        for employee_id in team.employeeIds:
            if employee_id not in usersIDS:
                usersIDS.append(DB.getPersonByID(employee_id))
    users = []
    for user in users:
        users.append(user)

    return {"data" : users}

@app.get("/department_teams/{id}")
async def get_department_teams(id : str):
    dep = DB.getDepartmentByID(id)

    if dep == None:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")
    teamsIDS = dep.teamIds
    teams = []

    for team_id in teamsIDS:
        teams.append(DB.getTeamByID(team_id))
    

    return {"data" : teams}


# =====================
#         Team
# =====================
@app.get("/team/{id}")
async def get_RPE(id : str):
    return {"data" : DB.getDepartmentByID(id)}

@app.post("/team")
async def create_team(team : TeamCreate):
    new_team = Team(team.name, departmentID=team.departmentID)
    DB.addItem(new_team)
    return {"message": "Time criado com sucesso!"}

@app.get("team_users/{id}")
async def get_team_users(id : str):
    team = DB.getTeamByID(id)

    if team == None:
        raise HTTPException(status_code=404, detail="Equipe não encontrado")
    users = [DB.getPersonByID(team.managerID)]

    for user_id in team.employeeIds:
        users.append(DB.getPersonByID(user_id))

    return {"data" : users}


# Deleta Item qualquer

@app.delete("/delete/{id}")
async def delete_rpe(id : str):
    if DB.deleteItembyID(id) == False:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    else:
        return {"message" : "item deletado com sucesso"}

@app.put("/add_team_user/{team_id}/{user_id}")
async def add_user_to_team(team_id : str, user_id : str):
    team = DB.getTeamByID(team_id)
    user = DB.getPersonByID(user_id)
    if team == None:
        raise HTTPException(
            status_code=400,
            detail=f"Equipe não encontrado"
        )
    elif user == None:
        raise HTTPException(
            status_code=400, 
            detail=f"Usuário não encontrado"
        )
    else:
        user.teamID(team_id)
        team.addEmployee(user)

        DB.updateItem(user)
        DB.updateItem(team)

        return {"message", "Membro adicionado na equipe"}

