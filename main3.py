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
    db = Database("backend/model/database/database.db")

    # Empresa
    company = Company(name="TechNova Global", cnpj="11.222.333/0001-99")
    db.addItem(company)

    # Diretora
    director = Director(
        name="Mariana Duarte", cpf="001",
        companyID=company.id, departmentID=None, teamID=None,
        email="mariana@technova.com", password="123", responsibleIds=[]
    )
    director.createUser(director, db)
    db.addDirectorToCompany(company.id, director.id)

    # Estrutura organizacional
    estrutura = {
        "Marketing": [
            "Brand Awareness",
            "Social Media & Engajamento"
        ],
        "Operações": [
            "Excelência Operacional",
            "Controle de Qualidade"
        ],
        "Inovação": [
            "Pesquisa Aplicada",
            "Laboratório de Protótipo"
        ],
        "Vendas": [
            "Inside Sales",
            "Grandes Contas"
        ]
    }

    # Banco de nomes realistas
    nomes_managers = [
        "Lucas Ferreira", "Paula Ramos", "Thiago Moreira", "Fernanda Nunes",
        "Rafael Cardoso", "Juliana Prado", "Marcelo Antunes", "Carolina Azevedo"
    ]

    nomes_employees = [
        "Bruno Costa", "Larissa Ribeiro", "Eduardo Martins", "Patrícia Leal",
        "Gabriel Mendes", "Amanda Farias", "Daniel Araújo", "Camila Lopes",
        "Fábio Nogueira", "Ana Beatriz Rocha", "Carlos Eduardo Lima", "Marina Teles",
        "Roberto Quinteiro", "Júlia Almeida", "Vinícius Vieira", "Sabrina Campos"
    ]

    cpf = 2000  # contador simples pra gerar CPFs únicos

    emp_index = 0
    manager_index = 0

    for dept_name, teams in estrutura.items():

        dept = Department(name=dept_name, directorID=director.id, companyID=company.id)
        db.addItem(dept)

        for team_name in teams:
            team = Team(name=team_name, managerID=None, departmentID=dept.id)
            db.addItem(team)

            # Cria gerente com nome real
            manager_name = nomes_managers[manager_index]
            manager_index += 1

            manager = Manager(
                name=manager_name, cpf=str(cpf),
                companyID=company.id, departmentID=dept.id,
                email=f"{manager_name.lower().replace(' ', '.')}@technova.com",
                password="123", responsibleIds=[]
            )
            cpf += 1

            director.createUser(manager, db)
            db.assignPersonToTeam(manager.id, team.id)

            # Cria 2 funcionários com nomes reais
            for _ in range(2):
                emp_name = nomes_employees[emp_index]
                emp_index += 1

                employee = Person(
                    name=emp_name, cpf=str(cpf),
                    companyID=company.id, departmentID=dept.id, teamID=team.id,
                    email=f"{emp_name.lower().replace(' ', '.')}@technova.com",
                    password="abc"
                )
                cpf += 1

                director.createUser(employee, db)


            # Criar RPE do departamento
        rpe_dept = RPE(
            description=f"Planejamento Anual - {dept.name}",
            responsibleID=director.id,
            date="2025-01-10"
        )
        db.addItem(rpe_dept)
        db.addRpeToDepartment(dept.id, rpe_dept.id)

        # Criar RPE por time (com gerente já definido)
        for team_name in teams:
            team = db.getTeamByName(team_name)
            manager = db.getPersonByID(team.managerID)

            rpe_team = RPE(
                description=f"Metas Operacionais - {team.name}",
                responsibleID=manager.id,
                date="2025-01-12"
            )
            db.addItem(rpe_team)
            db.addRpeToTeam(team.id, rpe_team.id)




    # Criar OKR estratégico de empresa
    rpe = RPE("Planejamento Estratégico 2025", director.id, "2025-01-01")
    director.createRPE(rpe, "Company", db)

    obj = Objective("Expandir presença no mercado nacional", director.id, "2025-02-01", rpe.id)
    director.createObjective(obj, db)

    kpi = KPI("Novos Clientes por Trimestre", director.id, "2025-03-01", obj.id)
    director.createKPI(kpi, db)

    kr = KR(
        description="Atingir 5.000 leads qualificados",
        responsibleID=kpi.responsibleID,
        date="2025-03-15",
        objectiveID = obj.id
    )
    director.createKR(kr, db)

    print("\n=== ✅ Banco de dados populado com nomes reais ===")

if __name__ == "__main__":
    main()
