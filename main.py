from backend.model.database.database import Database

from backend.model.entities.company import Company
from backend.model.entities.department import Department
from backend.model.entities.team import Team
from backend.model.entities.person import Person
from backend.model.entities.manager import Manager
from backend.model.entities.director import Director
from backend.model.entities.rpe import RPE
from backend.model.entities.objective import Objective
from backend.model.entities.kpi import KPI
from backend.model.entities.kr import KR


def main():
    print("=== Iniciando Banco ===")
    db = Database()

    # --- COMPANY ---
    company = Company(name="TechCorp", cnpj="00.111.222/0001-55")
    db.addItem(company)

    # --- DIRECTOR ---
    director = Director(
        name="Ana Silva",
        cpf="12345678900",
        companyID=company.id,
        departmentID=None,
        teamID=None,
        email="ana@corp.com",
        password="123",
        responsibleIds=[]
    )
    db.addItem(director)
    db.addDirectorToCompany(company.id, director.id)

    # --- DEPARTMENT ---
    dept = Department(name="Pesquisa e Desenvolvimento", directorID=director.id, companyID=company.id)
    db.addItem(dept)
    company.addDepartment(dept.id, db)
    db.assignPersonToDepartment(director.id, director.departmentID)

    # --- MANAGER ---
    manager = Manager(
        name="Carlos Pereira",
        cpf="98765432100",
        companyID=company.id,
        departmentID=dept.id,
        teamID=None,
        email="carlos@corp.com",
        password="abc",
        responsibleIds=[]
    )
    db.addItem(manager)

    # --- TEAM ---
    team = Team(name="Time Alpha", managerID=manager.id, departmentID=dept.id)
    db.addItem(team)
    dept.addTeam(team.id, db)
    db.updateItem(manager)

    # --- EMPLOYEE ---
    emp = Person(
        name="João Oliveira",
        cpf="11122233344",
        companyID=company.id,
        departmentID=dept.id,
        teamID=team.id,
        email="joao@corp.com",
        password="senha"
    )
    db.addItem(emp)
    team.addEmployee(emp.id, db)

    print("\n=== Testando Roles ===")

    print("\n[Director] criando RPE...")
    rpe = RPE(description="Meta do trimestre", responsibleID=director.id, date="2025-01-10")
    db.addItem(rpe)
    team.addRPE(rpe.id, db)

    print("[Manager] criando Objective...")
    obj = Objective(description="Melhorar processo", responsibleID=manager.id, date="2025-02-01", rpeID=rpe.id)
    manager.createObjective(obj, db)

    print("[Manager] criando KPI...")
    kpi = KPI(description="Velocidade média", responsibleID=manager.id, date="2025-03-01", objectiveID=obj.id)
    manager.createKPI(kpi, db)
    kpi.addData(40.0, db)
    kpi.addData(50.2, db)

    print("[Manager] criando KR...")
    kr = KR(description="Entrega de metas", responsibleID=manager.id, date="2025-03-05", objectiveID=obj.id, goal=90.0)
    manager.createKR(kr, db)
    kr.addData(75.0, db)

    print("\n[Employee] listando RPEs do time...")
    rpes_emp = emp.getData("Team", team.id, "RPE", db)
    for r in rpes_emp:
        print(" -", r.description)

    print("\n[Manager] coletando KPI (com permissão)...")
    manager.collectIndicator(kpi, db)

    print("\n=== Estrutura Completa do RPE ===")
    print(rpe.getData(db))

    print("\n=== Fim do Teste ===")


if __name__ == "__main__":
    main()
