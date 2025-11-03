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
    print("Inicializando banco...")
    db = Database()


    print("\nCriando empresa...")
    company = Company(name="TechCorp", cnpj="00.111.222/0001-55")
    db.addItem(company)


    print("Criando diretor...")
    director = Director(name="Ana Silva", cpf="12345678900", companyID=company.id,
    departmentID="", teamID="", email="ana@corp.com", password="123",
    responsibleIds=[])
    db.addItem(director)
    db.addDirectorToCompany(company.id, director.id)


    print("Criando departamento...")
    dept = Department(name="Pesquisa e Desenvolvimento", directorID=director.id, companyID=company.id)
    db.addItem(dept)
    company.addDepartment(dept.id, db)


    print("Criando gerente...")
    manager = Manager(name="Carlos Pereira", cpf="98765432100", companyID=company.id,
    departmentID=dept.id, teamID="", email="carlos@corp.com", password="abc",
    responsibleIds=[])
    db.addItem(manager)


    print("Criando time...")
    team = Team(name="Time Alpha", managerID=manager.id, departmentID=dept.id)
    db.addItem(team)
    dept.addTeam(team.id, db)


    # Atualiza teamID do gerente
    manager.teamID = team.id
    db.updateItem(manager)


    print("Adicionando funcionário ao time...")
    emp = Person(name="João Oliveira", cpf="11122233344", companyID=company.id,
    departmentID=dept.id, teamID=team.id, email="joao@corp.com", password="senha")
    db.addItem(emp)
    team.addEmployee(emp.id, db)


    print("Criando RPE...")
    rpe = RPE(description="Meta trimestral do time", responsibleID=manager.id, date="2025-01-10")
    db.addItem(rpe)
    team.addRPE(rpe.id, db)


    print("Criando objetivo...")
    obj = Objective(description="Melhorar performance", responsibleID=manager.id, date="2025-02-01")
    db.addItem(obj)
    db.addObjectiveToRpe(obj.id, rpe.id)


    print("Criando KPI e coletando dados...")
    kpi = KPI(description="Velocidade média de entrega", responsibleID=manager.id, date="2025-03-01")
    db.addItem(kpi)
    db.addKpiToObjective(obj.id, kpi.id)
    kpi.addData(42.5, db)


    print("Criando KR...")
    kr = KR(description="Entregar 90% das tarefas planejadas", responsibleID=manager.id, date="2025-03-01", goal=90.0)
    db.addItem(kr)
    db.addKpiToObjective(obj.id, kr.id)
    kr.addData(75.0, db)


    print("\n--- Estrutura Completa ---")
    full = rpe.getData(db)
    print(full)


    print("\nFim do teste.")




if __name__ == "__main__":
    main()