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
    print("=== Inicializando Banco ===")
    db = Database()

    # --- Criar empresa ---
    company = Company(name="TechCorp", cnpj="00.111.222/0001-55")
    db.addItem(company)

    # --- Criar diretor ---
    director = Director(name="Ana Silva", cpf="12345678900",
                        companyID=company.id, departmentID=None, teamID=None,
                        email="ana@corp.com", password="123", responsibleIds=[])
    director.createUser(director, db)  # Director cadastra a si mesmo
    db.addDirectorToCompany(company.id, director.id)

    # --- Criar departamento ---
    dept = Department(name="P&D", directorID=director.id, companyID=company.id)
    db.addItem(dept)
    company.addDepartment(dept.id, db)

    # --- Criar manager ---
    manager = Manager(name="Carlos Pereira", cpf="98765432100",
                      companyID=company.id, departmentID=dept.id,
                      email="carlos@corp.com", password="abc", responsibleIds=[])
    director.createUser(manager, db)  # Director cadastra manager

    # --- Criar time ---
    team = Team(name="Time Alpha", managerID=manager.id, departmentID=dept.id)
    db.addItem(team)
    dept.addTeam(team.id, db)

    # --- Criar employee ---
    emp = Person(name="João Oliveira", cpf="11122233344",
                 companyID=company.id, departmentID=dept.id, teamID=team.id,
                 email="joao@corp.com", password="senha")
    director.createUser(emp, db)

    print("\n=== Testando métodos do Director ===")

    # --- Criar RPEs ---
    rpe_company = RPE(description="RPE Company", responsibleID=director.id, date="2025-01-01")
    director.createRPE(rpe_company, "Company", db)

    rpe_dept = RPE(description="RPE Department", responsibleID=manager.id, date="2025-01-05")
    director.createRPE(rpe_dept, "Department", db)

    rpe_team = RPE(description="RPE Team", responsibleID=manager.id, date="2025-01-10")
    director.createRPE(rpe_team, "Team", db)

    # --- Criar Objective/KPI/KR ---
    obj = Objective(description="Objetivo 1", responsibleID=manager.id, date="2025-02-01", rpeID=rpe_team.id)
    director.createObjective(obj, db)

    kpi = KPI(description="KPI 1", responsibleID=manager.id, date="2025-02-15", objectiveID=obj.id)
    director.createKPI(kpi, db)
    kpi.addData(42.0, db)

    kr = KR(description="KR 1", responsibleID=manager.id, date="2025-02-20", objectiveID=obj.id, goal=90.0)
    director.createKR(kr, db)
    kr.addData(75.0, db)

    # --- Coletar indicador ---
    director.collectIndicator(kpi, db)

    # --- Alterar gerentes e diretores ---
    print("\nAlterando manager do time...")
    director.changeTeamManager(team.id, emp.id, db)

    print("Alterando diretor do departamento...")
    director.changeDepartmentDirector(dept.id, manager.id, db)

    # --- Adicionar/remover RPE responsável ---
    director.addResponsibleRpeId(rpe_team.id, db)
    director.deleteResponsibleRpeId(rpe_team.id, db)

    # --- Deletar KR/KPI/Objective/RPE ---
    director.deleteKR(kr, obj.id, db)
    director.deleteKPI(kpi, db)
    director.deleteObjective(obj, db)
    director.deleteRPE(rpe_team, db)
    director.deleteRPE(rpe_dept, db)
    director.deleteRPE(rpe_company, db)

    # --- Deletar usuários ---
    director.deleteUser(emp, db)
    director.deleteUser(manager, db)

    print("\n=== Teste completo dos métodos do Director finalizado ===")

if __name__ == "__main__":
    main()
