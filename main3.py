import os

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

DB_PATH = "backend/model/database/database.db"

def setup_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    return Database(DB_PATH)

def main():
    db = setup_database()
    print(f"\n=== 🏦 Banco inicializado: {DB_PATH} ===\n")

    try:
        print("--- Fase 1: Criando Empresa e Hierarquia ---")

        company = Company(name="TechCorp", cnpj="00.111.222/0001-55")
        db.addItem(company)

        director = Director(name="Ana Silva (Diretora)", cpf="123",
                            companyID=company.id, departmentID=None, teamID=None,
                            email="ana@corp.com", password="123", responsibleIds=[])
        director.createUser(director, db)
        db.addDirectorToCompany(company.id, director.id)

        dept = Department(name="P&D", directorID=director.id, companyID=company.id)
        db.addItem(dept)
        db.assignPersonToDepartment(director.id, dept.id)

        # 3 Gerentes
        managers = []
        for nome, cpf in [("Carlos", "456"), ("Bianca", "457"), ("Roberto", "458")]:
            m = Manager(name=nome, cpf=cpf, companyID=company.id, departmentID=dept.id,
                        email=f"{nome.lower()}@corp.com", password="123", responsibleIds=[])
            director.createUser(m, db)
            managers.append(m)

        # 3 Times (1 por gerente)
        teams = []
        for i, m in enumerate(managers):
            t = Team(name=f"Time {i+1}", managerID=m.id, departmentID=dept.id)
            db.addItem(t)
            db.assignPersonToTeam(m.id, t.id)
            teams.append(t)

        # 6 Funcionários (2 por time)
        employees = []
        for i, t in enumerate(teams):
            for n in range(2):
                emp = Person(name=f"Dev_{i}_{n}", cpf=f"99{i}{n}",
                             companyID=company.id, departmentID=dept.id, teamID=t.id,
                             email=f"dev_{i}_{n}@corp.com", password="pwd")
                director.createUser(emp, db)
                employees.append(emp)

        print("✅ Hierarquia robusta criada!\n")

        print("--- Fase 2: Diretor cria dados em todos níveis ---")

        rpe_company = RPE("RPE Global", director.id, "2025-01-01")
        director.createRPE(rpe_company, "Company", db)

        rpe_dept = RPE("RPE P&D", director.id, "2025-01-05")
        director.createRPE(rpe_dept, "Department", db)

        rpe_teams = []
        for t in teams:
            r = RPE(f"RPE {t.name}", t.managerID, "2025-01-10")
            director.createRPE(r, "Team", db)
            rpe_teams.append(r)

        print("✅ Diretor criou todos RPEs")

        obj_global = Objective("Objetivo Global", director.id, "2025-02-01", rpe_company.id)
        director.createObjective(obj_global, db)

        kpi_global = KPI("KPI Global", director.id, "2025-02-10", obj_global.id)
        director.createKPI(kpi_global, db)
        kpi_global.addData(20, db)
        director.collectIndicator(kpi_global, db)

        print("✅ Diretor criou Objective e KPI Global\n")

        print("--- Fase 3: Testando Managers (Somente seu Time) ---")

        for m, t, rpe in zip(managers, teams, rpe_teams):
            obj_t = Objective(f"Objetivo {t.name}", m.id, "2025-03-01", rpe.id)
            m.createObjective(obj_t, db)
            assert db.getObjectiveByID(obj_t.id) is not None

            kpi_t = KPI(f"KPI {t.name}", m.id, "2025-03-05", obj_t.id)
            m.createKPI(kpi_t, db)
            kpi_t.addData(80, db)
            m.collectIndicator(kpi_t, db)

        print("✅ Managers criaram dados somente para seus times\n")

        print("--- Fase 4: Teste de Restrições ---")

        obj_illegal = Objective("Objetivo Ilegal", managers[0].id, "2025-03-10", rpe_company.id)
        managers[0].createObjective(obj_illegal, db)
        assert db.getObjectiveByID(obj_illegal.id) is None

        print("✅ Bloqueio de permissões funcionando!")

        print("\n=== ✅ Teste robusto concluído sem falhas! ===")

    except AssertionError as e:
        print(f"\n❌ ASSERT FALHOU: {e}")
    except Exception as e:
        print(f"\n💥 ERRO INESPERADO: {e}")

if __name__ == "__main__":
    main()
