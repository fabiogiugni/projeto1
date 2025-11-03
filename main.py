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

    # Empresa
    company = Company(name="TechCorp", cnpj="00.111.222/0001-55")
    db.addItem(company)

    # Diretor
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

    # Departamento
    dept = Department(
        name="Pesquisa e Desenvolvimento",
        companyID=company.id,
        directorID=director.id
    )
    db.addItem(dept)

    # Gerente
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

    # Time
    team = Team(
        name="Time Alpha",
        departmentID=dept.id,
        managerID=manager.id
    )
    db.addItem(team)

    # Funcionário
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

    # RPE
    rpe = RPE(
        description="Meta trimestral do time",
        responsibleID=manager.id,
        date="2025-01-10"
    )
    db.addItem(rpe)

    # Objetivo (agora recebe rpeID diretamente)
    obj = Objective(
        description="Melhorar performance",
        responsibleID=manager.id,
        date="2025-02-01",
        rpeID=rpe.id
    )
    db.addItem(obj)

    # KPI (agora recebe objectiveID diretamente)
    kpi = KPI(
        description="Velocidade média de entrega",
        responsibleID=manager.id,
        date="2025-03-01",
        objectiveID=obj.id
    )
    db.addItem(kpi)
    kpi.addData(42.5, db)

    # KR (mesma lógica)
    kr = KR(
        description="Entregar 90% das tarefas planejadas",
        responsibleID=manager.id,
        date="2025-03-01",
        objectiveID=obj.id,
        goal=90.0,
        id=None,
        data=[]
    )
    # KR TAMBÉM É SALVO NA TABELA KPI
    kr._objectiveID = obj.id
    db.addItem(kr)
    kr.addData(75.0, db)

    print("\n--- Estrutura Completa ---")
    estrutura = rpe.getData(db)
    print(estrutura)

    print("\nFim do teste.")

if __name__ == "__main__":
    main()
