from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime

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

app = FastAPI(title="Backend API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Libera todas as origens (frontend incluso)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB = Database("database.db")

@app.get("/")
async def read_root():
    return {"message": "Backend Python funcionando!"}


# =====================
#         USER
# =====================
@app.get("/user_by_email/{email}")
async def get_user_by_email(email: str):
    if not email:
        raise HTTPException(status_code=400, detail="Email é obrigatório")
    user = DB.getPersonByEmail(email)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"data": user}


@app.post("/login")
async def login(data: Login):
    if not data.email or not data.password:
        raise HTTPException(status_code=400, detail="Email e senha são obrigatórios")

    user = DB.getPersonByEmail(data.email)
    if user and user.verifyPassword(data.password):
        return {"status": True, "message": user}
    return {"status": False, "message": "Email ou senha incorretos"}
   
@app.get("/user_by_id/{id}")
async def get_user_by_id(id : str):
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
    required = [user.name, user.cpf, user.email, user.password]
    if not all(required):
        raise HTTPException(status_code=400, detail="Campos obrigatórios ausentes")

    new_user = Person(
        user.name, user.cpf, user.companyID,
        user.departmentID, user.teamID, user.email, user.password
    )
    DB.addItem(new_user)
    return {"message": "Usuário criado com sucesso!"}

@app.get("/getAllCompanies")
async def getAllCompanies():
    companies = DB.getCompanyByID("c972a771-0718-4c75-bddf-dfa605b7b93d")
    return {"data": companies}


@app.put("/user_role/{id}/{role}")
async def change_role(id: str, role: str):
    if not id or not role:
        raise HTTPException(status_code=400, detail="ID e cargo são obrigatórios")
    user = DB.getPersonByID(id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    user.role = role

    if user == None:
        raise HTTPException(
            status_code=404, 
            detail=f"Usuário não encontrado"
        )
    else:
        user.role = role
        DB.updateItem(user)
        return {"message": "Cargo mudado com sucesso"}


@app.put("/user_department/{id}/{idDepartment}")
async def change_user_department(id: str, idDepartment: str):
    DB.assignPersonToDepartment(id, idDepartment)

# =====================
#         RPE
# =====================
@app.post("/RPE")
async def create_RPE(rpe: RPECreate):
    if not rpe.description or not rpe.responsibleID:
        raise HTTPException(status_code=400, detail="Descrição e responsável são obrigatórios")

    date = datetime.now()
    new_rpe = RPE(rpe.description, rpe.responsibleID, date)
    DB.addItem(new_rpe)
    return {"message": "RPE criado com sucesso!", "id": new_rpe.id}


@app.get("/RPE/{id}")
async def get_RPE(id: str):
    if not id:
        raise HTTPException(status_code=400, detail="ID é obrigatório")
    rpe = DB.getRPEByID(id)
    if rpe is None:
        raise HTTPException(status_code=404, detail="RPE não encontrado")
    return {"data": rpe}


@app.put("/kr_goal/{id}")
async def change_kr_goal(id: str, kr_data: KRUpdate):
    if not id or kr_data.goal is None:
        raise HTTPException(status_code=400, detail="ID e novo goal são obrigatórios")

    kr = DB.getKRByID(id)
    if kr is None:
        raise HTTPException(status_code=404, detail="KR não encontrado")

    kr.goal = kr_data.goal
    DB.updateItem(kr)
    return {"message": "KR atualizado com sucesso"}


@app.put("/kr_data/{id}")
async def change_kr_data(id: str, kr_data: DataAdd):
    if not id or kr_data.data is None:
        raise HTTPException(status_code=400, detail="ID e dados são obrigatórios")

    kr = DB.getKRByID(id)
    if kr is None:
        raise HTTPException(status_code=404, detail="KR não encontrado")

    kr.addData(kr_data.data)
    DB.updateItem(kr)
    return {"message": "KR atualizado com sucesso"}


# =====================
#         COMPANY
# =====================
@app.post("/company")
async def create_company(company: CompanyCreate):
    if not company.name or not company.cnpj:
        raise HTTPException(status_code=400, detail="Nome e CNPJ são obrigatórios")

    new_company = Company(company.name, company.cnpj)
    DB.addItem(new_company)
    return {"message": "Empresa criada com sucesso!"}


@app.get("/company/{cnpj}")
async def get_company(cnpj: str):
    if not cnpj:
        raise HTTPException(status_code=400, detail="CNPJ é obrigatório")
    company = DB.getCompanyByCnpj(cnpj)
    if company is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return {"data": company}


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
#      DEPARTMENT
# =====================
@app.post("/department")
async def create_department(department: DepartmentCreate):
    if not department.name or not department.companyID:
        raise HTTPException(status_code=400, detail="Nome e companyID são obrigatórios")

    new_department = Department(department.name, department.companyID)
    DB.addItem(new_department)
    return {"message": "Departamento criado com sucesso!"}

@app.get("/department/{id}")
async def get_department_by_id(id:str):
    department = DB.getDepartmentByID(id)
    print(department)
    if(department == None):
        raise HTTPException(status_code=404, detail="Departamento não encontrado")
    else: return({"data": department})


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

@app.get("/getAllDepartments") 
async def getDepartmentsByCompanyID():
    departaments = DB.getDepartmentsByCompanyID("c972a771-0718-4c75-bddf-dfa605b7b93d")
    
    return {"data": departaments}

@app.get("/getAllEmployees") 
async def getPersonsByCompanyID():
    users = DB.getPersonsByCompanyID("c972a771-0718-4c75-bddf-dfa605b7b93d")
    
    return {"data": users}
    
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
#         TEAM
# =====================
@app.get("/getAllTeams")
async def get_teams():
    teams = DB.getTeams()
    
    return {"data": teams}

@app.post("/team")
async def create_team(team: TeamCreate):
    if not team.name or not team.departmentID:
        raise HTTPException(status_code=400, detail="Nome e departmentID são obrigatórios")

    new_team = Team(team.name, team.departmentID)
    DB.addItem(new_team)
    return {"message": "Time criado com sucesso!"}

@app.get("/team_users/{id}")
async def get_team_users(id : str):
    team = DB.getTeamByID(id)

    if team == None:
        raise HTTPException(status_code=404, detail="Equipe não encontrado")
    users = DB.getPersonsByTeamID(team.id)


    return {"data" : users}

# =====================
#      DELETE ENDPOINTS
# =====================

@app.delete("/company/{id}")
async def delete_company(id: str):
    """Deleta uma empresa pelo ID"""
    company = DB.getCompanyByID(id)
    if company is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    DB.deleteItemByObject(company)
    return {"message": "Empresa deletada com sucesso"}

@app.delete("/department/{id}")
async def delete_department(id: str):
    """Deleta um departamento pelo ID"""
    department = DB.getDepartmentByID(id)
    if department is None:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")
    
    DB.deleteItemByObject(department)
    return {"message": "Departamento deletado com sucesso"}

@app.delete("/team/{id}")
async def delete_team(id: str):
    """Deleta um time pelo ID"""
    team = DB.getTeamByID(id)
    if team is None:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    
    DB.deleteItemByObject(team)
    return {"message": "Time deletado com sucesso"}

@app.delete("/user/{id}")
async def delete_user(id: str):
    """Deleta um usuário pelo ID"""
    user = DB.getPersonByID(id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    DB.deleteItemByObject(user)
    return {"message": "Usuário deletado com sucesso"}

@app.delete("/rpe/{id}")
async def delete_rpe(id: str):
    """Deleta um RPE pelo ID"""
    rpe = DB.getRPEByID(id)
    if rpe is None:
        raise HTTPException(status_code=404, detail="RPE não encontrado")
    
    DB.deleteItemByObject(rpe)
    return {"message": "RPE deletado com sucesso"}

@app.delete("/objective/{id}")
async def delete_objective(id: str):
    """Deleta um objetivo pelo ID"""
    objective = DB.getObjectiveByID(id)
    if objective is None:
        raise HTTPException(status_code=404, detail="Objetivo não encontrado")
    
    DB.deleteItemByObject(objective)
    return {"message": "Objetivo deletado com sucesso"}

@app.delete("/kpi/{id}")
async def delete_kpi(id: str):
    """Deleta um KPI pelo ID"""
    kpi = DB.getKPIByID(id)
    if kpi is None:
        raise HTTPException(status_code=404, detail="KPI não encontrado")
    
    DB.deleteItemByObject(kpi)
    return {"message": "KPI deletado com sucesso"}

@app.delete("/kr/{id}")
async def delete_kr(id: str):
    """Deleta um KR pelo ID"""
    kr = DB.getKRByID(id)
    if kr is None:
        raise HTTPException(status_code=404, detail="KR não encontrado")
    
    DB.deleteItemByObject(kr)
    return {"message": "KR deletado com sucesso"}



@app.get("/data/{group_type}/{group_id}/{data_type}")
async def get_data_by_entity(group_type: str, group_id: str, data_type: str):
    """
    Retorna RPE / Objective / KPI / KR filtrado por Company, Department ou Team.
    group_type: "company" | "department" | "team"
    data_type: "rpe" | "objective" | "kpi" | "kr"
    """

    if not (group_type and group_id and data_type):
        raise HTTPException(status_code=400, detail="Parâmetros obrigatórios ausentes")

    group_type_normalized = group_type.capitalize()

    data_type_normalized = data_type.upper()

    try:
        result = DB.getDataByEntity(
            group_type_normalized,
            group_id,
            data_type_normalized
        )
        return {"data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

