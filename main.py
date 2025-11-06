from backend.model.database.database import Database
from backend.model.entities.company import Company
from backend.model.entities.department import Department
from backend.model.entities.team import Team

def main():
    # Cria o banco do zero (se já existir, use outro nome ou delete o arquivo antes)
    db = Database("backend/model/database/test_getteam.db")

    # 1) Cria empresa
    company = Company(name="TesteCorp", cnpj="00.000.000/0001-00")
    db.addItem(company)

    # 2) Cria departamento
    dept = Department(name="Desenvolvimento", directorID=None, companyID=company.id)
    db.addItem(dept)

    # 3) Cria time
    team = Team(name="Time de Backend", managerID=None, departmentID=dept.id)
    db.addItem(team)

    print("\n✅ Dados inseridos.")

    # === TESTE getTeamByName ===
    print("\n=== Testando getTeamByName ===")
    result = db.getTeamByName("Time de Backend")

    if result:
        print(f"✅ Team encontrado:")
        print(f"   ID: {result.id}")
        print(f"   Nome: {result.name}")
        print(f"   DepartmentID: {result.departmentID}")
        print(f"   ManagerID: {result.managerID}")
    else:
        print("❌ Team não encontrado.")

    del db

if __name__ == "__main__":
    main()
