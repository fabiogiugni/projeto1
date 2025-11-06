from backend.model.database.database import Database

def test_relations():
    DB = Database("backend/model/database/database.db")  # ou o caminho real do seu DB

    # ====== CONFIGURE AQUI ======
    test_company_id = "220df9db-b89a-4af5-9815-b51b78f52934"
    test_department_id = "36441afd-c701-4676-ab6d-477a62b9d52d"
    test_team_id = "5b6c4528-27bc-441e-8316-9178804714f4"
    # ============================

    print("\n=== Testando Departamentos da Empresa ===")
    departments = DB.getDepartmentsByCompanyID(test_company_id)
    for dep in departments:
        print(f"- {dep.id} | {dep.name} | companyID={dep.companyID}")

    print("\n=== Testando Times do Departamento ===")
    teams = DB.getTeamsByDepartmentID(test_department_id)
    for team in teams:
        print(f"- {team.id} | {team.name} | departmentID={team.departmentID}")

    print("\n=== Testando Pessoas do Time ===")
    persons_team = DB.getPersonsByTeamID(test_team_id)
    for p in persons_team:
        print(f"- {p.id} | {p.name} | role={p.role} | teamID={p.teamID}")

    print("\n=== Testando Pessoas do Departamento ===")
    persons_department = DB.getPersonsByDepartmentID(test_department_id)
    for p in persons_department:
        print(f"- {p.id} | {p.name} | role={p.role} | departmentID={p.departmentID}, teamID={p.teamID}")

    print("\n=== Testando Pessoas da Empresa ===")
    persons_company = DB.getPersonsByCompanyID(test_company_id)
    for p in persons_company:
        print(f"- {p.id} | {p.name} | role={p.role} | companyID={p.companyID}, departmentID={p.departmentID}, teamID={p.teamID}")

    print("\n=== FIM DO TESTE ===")


if __name__ == "__main__":
    test_relations()
