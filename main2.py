import os
import time

# --- Ajuste os imports para sua estrutura ---
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

# --- Configuração do Teste ---
DB_PATH = "backend/model/database/database.db"

def setup_database():
    """Garante um banco de dados limpo para cada execução."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    db = Database(DB_PATH)
    return db

def main():
    db = setup_database()
    print(f"=== 🏦 Banco de dados de teste '{DB_PATH}' inicializado ===\n")

    try:
        # --- Fase 1: Setup da Hierarquia ---
        print("--- Fase 1: Configurando Hierarquia (Company, Director, Dept, Manager, Team, Emp) ---")
        
        company = Company(name="TechCorp", cnpj="00.111.222/0001-55")
        db.addItem(company)

        # Criar Diretor
        director = Director(name="Ana Silva (Diretora)", cpf="123",
                            companyID=company.id, departmentID=None, teamID=None,
                            email="ana@corp.com", password="123", responsibleIds=[])
        director.createUser(director, db) # 
        db.addDirectorToCompany(company.id, director.id) # (Método do DB, assumindo que existe)

        # Criar Departamento e atribuir a Diretora
        dept = Department(name="P&D", directorID=director.id, companyID=company.id)
        db.addItem(dept)
        db.assignPersonToDepartment(director.id, dept.id) # (Método do DB, atualiza o 'departmentID' da Ana)
        # Recarregar 'director' do DB para obter o departmentID atualizado
        director = db.getPersonByID(director.id)
        assert director.departmentID == dept.id, "Falha ao associar Diretor ao Departamento"

        # Criar Gerente
        manager = Manager(name="Carlos Pereira (Gerente)", cpf="456",
                            companyID=company.id, departmentID=dept.id,
                            email="carlos@corp.com", password="abc", responsibleIds=[])
        director.createUser(manager, db) # 

        # Criar Time e atribuir o Gerente
        team = Team(name="Time Alpha", managerID=manager.id, departmentID=dept.id)
        db.addItem(team)
        db.assignPersonToTeam(manager.id, team.id) # (Método do DB, atualiza o 'teamID' do Carlos)
        # Recarregar 'manager' do DB
        manager = db.getPersonByID(manager.id)
        assert manager.teamID == team.id, "Falha ao associar Gerente ao Time"

        # Criar Funcionário
        emp = Person(name="João Oliveira (Dev)", cpf="789",
                       companyID=company.id, departmentID=dept.id, teamID=team.id,
                       email="joao@corp.com", password="senha")
        director.createUser(emp, db) # 
        
        print("Hierarquia criada com sucesso!\n")

        # --- Fase 2: Testando Ações do Director (Permissão Total) ---
        print("--- Fase 2: Testando Ações do Director ---")
        
        # Criar RPEs em todos os níveis
        rpe_company = RPE(description="RPE Nível Companhia", responsibleID=director.id, date="2025-01-01")
        director.createRPE(rpe_company, "Company", db) # 
        
        rpe_dept = RPE(description="RPE Nível Departamento", responsibleID=director.id, date="2025-01-05")
        director.createRPE(rpe_dept, "Department", db) # 
        
        rpe_team = RPE(description="RPE Nível Time", responsibleID=manager.id, date="2025-01-10")
        director.createRPE(rpe_team, "Team", db) # 
        
        assert db.getRPEByID(rpe_company.id) is not None, "Diretor falhou em criar RPE Company"
        assert db.getRPEByID(rpe_dept.id) is not None, "Diretor falhou em criar RPE Dept"
        assert db.getRPEByID(rpe_team.id) is not None, "Diretor falhou em criar RPE Team"
        print("... OK! createRPE (Todos os níveis)")

        # Criar hierarquia de dados (Obj, KPI, KR)
        obj_company = Objective(description="Obj da Companhia", responsibleID=director.id, date="2025-02-01", rpeID=rpe_company.id)
        director.createObjective(obj_company, db) # 
        assert db.getObjectiveByID(obj_company.id) is not None

        kpi_company = KPI(description="KPI da Companhia", responsibleID=director.id, date="2025-02-15", objectiveID=obj_company.id)
        director.createKPI(kpi_company, db) # 
        assert db.getKPIByID(kpi_company.id) is not None
        print("... OK! createObjective, createKPI")

        # Testar coleta de indicador
        director.collectIndicator(kpi_company,50, db) # 
        kpi_fetched = db.getKPIByID(kpi_company.id)
        assert kpi_fetched.getLastData() == 50.0, "Diretor falhou em coletar indicador"
        print("... OK! collectIndicator")

        # Testar gerenciamento de hierarquia
        director.changeTeamManager(team.id, emp.id, db) # 
        team_fetched = db.getTeamByID(team.id)
        assert team_fetched.managerID == emp.id, "Diretor falhou em mudar manager do time"
        
        director.changeDepartmentDirector(dept.id, manager.id, db) # 
        dept_fetched = db.getDepartmentByID(dept.id)
        assert dept_fetched.directorID == manager.id, "Diretor falhou em mudar diretor do dept"
        print("... OK! changeTeamManager, changeDepartmentDirector")

        # Reverter para o estado original para próximos testes
        director.changeTeamManager(team.id, manager.id, db)
        director.changeDepartmentDirector(dept.id, director.id, db)

        # --- Fase 3: Testando Ações do Manager (Permissões Limitadas) ---
        print("\n--- Fase 3: Testando Ações do Manager ---")
        
        # Teste 3.1: Ações PERMITIDAS
        print("... Testando ações PERMITIDAS (Nível Time/Dept)...")
        
        # Gerenciar time
        manager.addTeamEmployee(emp.id, db) #  (Isso deve reatribuir o teamID do emp)
        emp_fetched = db.getPersonByID(emp.id)
        assert emp_fetched.teamID == team.id
        
        manager.removeTeamEmployee(emp.id, db) #  (Isso deve setar teamID para None)
        emp_fetched = db.getPersonByID(emp.id)
        assert emp_fetched.teamID is None
        print("... OK! addTeamEmployee, removeTeamEmployee")
        
        # Re-adicionar funcionário para testes futuros
        manager.addTeamEmployee(emp.id, db)

        # Criar Objective (Nível Time)
        obj_team = Objective(description="Obj do Time", responsibleID=manager.id, date="2025-03-01", rpeID=rpe_team.id)
        manager.createObjective(obj_team, db) # 
        assert db.getObjectiveByID(obj_team.id) is not None, "Manager falhou em criar Objective de Time (Permitido)"
        print("... OK! createObjective (Nível Time)")

        # Criar KPI (Nível Time)
        kpi_team = KPI(description="KPI do Time", responsibleID=manager.id, date="2025-03-05", objectiveID=obj_team.id)
        manager.createKPI(kpi_team, db) # 
        assert db.getKPIByID(kpi_team.id) is not None, "Manager falhou em criar KPI de Time (Permitido)"
        print("... OK! createKPI (Nível Time)")

        # Coletar indicador (Permitido, pois ele é o responsável)
        manager.collectIndicator(kpi_team,100.0, db) # 
        kpi_team_fetched = db.getKPIByID(kpi_team.id)
        assert kpi_team_fetched.getLastData() == 100.0
        print("... OK! collectIndicator (Próprio KPI)")

        # Teste 3.2: Ações BLOQUEADAS
        print("... Testando ações BLOQUEADAS (Nível Companhia)...")
        
        # Tentar criar Objective (Nível Companhia)
        obj_company_fail = Objective(description="Obj. Falho", responsibleID=manager.id, date="2025-04-01", rpeID=rpe_company.id)
        manager.createObjective(obj_company_fail, db) # 
        assert db.getObjectiveByID(obj_company_fail.id) is None, "ERRO: Manager criou Objective de Companhia (Deveria falhar)"
        print("... OK! createObjective (Nível Companhia bloqueado)")

        # Tentar criar KPI (Nível Companhia)
        kpi_company_fail = KPI(description="KPI Falho", responsibleID=manager.id, date="2025-04-01", objectiveID=obj_company.id)
        manager.createKPI(kpi_company_fail, db) # 
        assert db.getKPIByID(kpi_company_fail.id) is None, "ERRO: Manager criou KPI de Companhia (Deveria falhar)"
        print("... OK! createKPI (Nível Companhia bloqueado)")
        
        # Tentar coletar indicador (Bloqueado, pois o Diretor é o responsável)
        print("chegou")
        manager.collectIndicator(kpi_company, 999.0 ,db) # 
        kpi_fetched_fail = db.getKPIByID(kpi_company.id)
        assert kpi_fetched_fail.getLastData() != 999.0, "ERRO: Manager coletou indicador de outro responsável"
        assert kpi_fetched_fail.getLastData() == 50.0 # (Valor antigo, do diretor)
        print("... OK! collectIndicator (KPI de outro Resp. bloqueado)")

        # --- Fase 4: Testando Ações da Pessoa ---
        print("\n--- Fase 4: Testando Ações da Pessoa ---")
        
        # Teste 4.1: Verificação de Senha
        assert emp.verifyPassword("senha") == True, "verifyPassword falhou (sucesso)" # 
        assert emp.verifyPassword("errado") == False, "verifyPassword falhou (falha)" # 
        print("... OK! verifyPassword")

        # Teste 4.2: Busca de Dados
        # (Assumindo que db.getDataByEntity existe)
        dados_time = emp.getData("Team", team.id, "RPE", db) # 
        assert len(dados_time) > 0, "getData (Team) falhou"
        assert dados_time[0].id == rpe_team.id
        
        dados_dept = emp.getData("Department", dept.id, "RPE", db) # 
        assert len(dados_dept) > 0, "getData (Dept) falhou"
        assert dados_dept[0].id == rpe_dept.id

        dados_comp = emp.getData("Company", company.id, "RPE", db) # 
        assert len(dados_comp) > 0, "getData (Company) falhou"
        assert dados_comp[0].id == rpe_company.id
        print("... OK! getData")

                # --- EXTENSÃO DO TESTE: Criar 3 novos departamentos, com 2 times cada e 2 pessoas cada ---
        print("--- Criando estrutura adicional de Departamentos, Times e Pessoas ---")

        for i in range(1, 4):  # Dept 2, 3 e 4
            dept_new = Department(name=f"Departamento {i}", directorID=director.id, companyID=company.id)
            db.addItem(dept_new)
            db.assignPersonToDepartment(director.id, dept_new.id)

            for t in range(1, 3):  # 2 times por departamento
                team_new = Team(name=f"Time {i}.{t}", managerID=None, departmentID=dept_new.id)
                db.addItem(team_new)

                # Criar gerente para o time
                manager_new = Manager(
                    name=f"Gerente {i}.{t}", cpf=f"900{i}{t}",
                    companyID=company.id, departmentID=dept_new.id,
                    email=f"gerente{i}{t}@corp.com", password="123", responsibleIds=[]
                )
                director.createUser(manager_new, db)
                db.assignPersonToTeam(manager_new.id, team_new.id)

                # Criar 2 funcionários no time
                for p in range(1, 3):
                    emp_new = Person(
                        name=f"Funcionario {i}.{t}.{p}", cpf=f"800{i}{t}{p}",
                        companyID=company.id, departmentID=dept_new.id, teamID=team_new.id,
                        email=f"func{i}{t}{p}@corp.com", password="abc"
                    )
                    director.createUser(emp_new, db)

        print("Estrutura adicional criada com sucesso!\n")

        
        print("\n=== ✅ Testes robustos concluídos com sucesso! ===")

    except AssertionError as e:
        print(f"\n=== ❌ TESTE FALHOU ❌ ===")
        print(f"Assert Falhou: {e}")
    except Exception as e:
        print(f"\n=== 💥 ERRO INESPERADO 💥 ===")
        print(f"Exceção: {e}")
    
    finally:
        # Garante que o DB de teste seja sempre limpo
        del db # Fecha a conexão
        print(f"\n=== 🧹 Banco de dados de teste '{DB_PATH}' limpo. ===")


if __name__ == "__main__":
    main()