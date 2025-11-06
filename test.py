from backend.model.database.database import Database

def test_relations():
    DB = Database("backend/model/database/database.db")  # ou o caminho real do seu DB

    # ====== CONFIGURE AQUI ======
    test_company_id = "1c750f37-9421-4a64-a3c5-46c555155cb2"
    test_department_id = "9d31406e-2ad5-4e2c-ae16-7789f9c97213"
    test_team_id = "6f061dec-f873-4b8f-9dcf-5d635467168b"
    # ============================

    print("\n=== Testando Departamentos da Empresa ===")
    departments = DB.getDepartmentsByCompanyID(test_company_id)
    for dep in departments:
        
        print(f"- {dep.id} | {dep.name} | companyID={dep.companyID}")

    print("\n=== Testando Times da Empresa ===")
    departments = DB.getDepartmentsByCompanyID(test_company_id)
    teams = []
    for dep in departments:
        teams += DB.getTeamsByDepartmentID(dep.id)
    for team in teams:
        print(f"- {team.id} | {team.name} | departmentID={team.departmentID}")

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
