import sqlite3
from typing import Optional

from entity import Entity
from person import Person
from employee import Employee
from manager import Manager
from director import Director
from company import Company
from department import Department
from team import Team
from rpe import RPE
from objective import Objective
from kpi import KPI
from kr import KR


class Database:

    def __init__(self, db_path: str = 'database/database.db'):
        
        self.__db = sqlite3.connect(db_path)
        
        self.__db.execute("PRAGMA foreign_keys = ON;")

        self.__db.executescript('''
        
            CREATE TABLE IF NOT EXISTS company (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                cnpj TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS department (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                companyID TEXT, 
                directorID TEXT,
                FOREIGN KEY(companyID) REFERENCES company(id) ON DELETE CASCADE,
                FOREIGN KEY(directorID) REFERENCES person(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS team (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                departmentID TEXT,
                managerID TEXT,
                FOREIGN KEY(departmentID) REFERENCES department(id) ON DELETE CASCADE,
                FOREIGN KEY(managerID) REFERENCES person(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS person (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                cpf TEXT UNIQUE,
                companyID TEXT,
                departmentID TEXT,
                role TEXT,
                email TEXT,
                password TEXT,
                FOREIGN KEY(companyID) REFERENCES company(id) ON DELETE SET NULL,
                FOREIGN KEY(departmentID) REFERENCES department(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS rpe (
                id TEXT PRIMARY KEY,
                description TEXT,
                responsibleID TEXT,
                date TEXT,
                FOREIGN KEY(responsibleID) REFERENCES person(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS objective (
                id TEXT PRIMARY KEY,
                description TEXT,
                rpeID TEXT,
                responsibleID TEXT,
                date TEXT,
                FOREIGN KEY(rpeID) REFERENCES rpe(id) ON DELETE CASCADE,
                FOREIGN KEY(responsibleID) REFERENCES person(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS kpi (
                id TEXT PRIMARY KEY,
                description TEXT,
                responsibleID TEXT,
                date TEXT,
                data TEXT,
                goal FLOAT,
                FOREIGN KEY(responsibleID) REFERENCES person(id) ON DELETE SET NULL
            );

            --- TABELAS DE JUNÇÃO (Muitos-para-Muitos) ---

            CREATE TABLE IF NOT EXISTS team_members (
                teamID TEXT NOT NULL,
                personID TEXT NOT NULL,
                PRIMARY KEY (teamID, personID),
                FOREIGN KEY(teamID) REFERENCES team(id) ON DELETE CASCADE,
                FOREIGN KEY(personID) REFERENCES person(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS person_responsibles (
                personID TEXT NOT NULL,
                responsibleID TEXT NOT NULL,
                PRIMARY KEY (personID, responsibleID),
                FOREIGN KEY(personID) REFERENCES person(id) ON DELETE CASCADE,
                FOREIGN KEY(responsibleID) REFERENCES person(id) ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS company_directors (
                companyID TEXT NOT NULL,
                personID TEXT NOT NULL,
                PRIMARY KEY (companyID, personID),
                FOREIGN KEY(companyID) REFERENCES company(id) ON DELETE CASCADE,
                FOREIGN KEY(personID) REFERENCES person(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS company_rpes (
                companyID TEXT NOT NULL,
                rpeID TEXT NOT NULL,
                PRIMARY KEY (companyID, rpeID),
                FOREIGN KEY(companyID) REFERENCES company(id) ON DELETE CASCADE,
                FOREIGN KEY(rpeID) REFERENCES rpe(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS department_rpes (
                departmentID TEXT NOT NULL,
                rpeID TEXT NOT NULL,
                PRIMARY KEY (departmentID, rpeID),
                FOREIGN KEY(departmentID) REFERENCES department(id) ON DELETE CASCADE,
                FOREIGN KEY(rpeID) REFERENCES rpe(id) ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS team_rpes (
                teamID TEXT NOT NULL,
                rpeID TEXT NOT NULL,
                PRIMARY KEY (teamID, rpeID),
                FOREIGN KEY(teamID) REFERENCES team(id) ON DELETE CASCADE,
                FOREIGN KEY(rpeID) REFERENCES rpe(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS objective_kpis (
                objectiveID TEXT NOT NULL,
                kpiID TEXT NOT NULL,
                PRIMARY KEY (objectiveID, kpiID),
                FOREIGN KEY(objectiveID) REFERENCES objective(id) ON DELETE CASCADE,
                FOREIGN KEY(kpiID) REFERENCES kpi(id) ON DELETE CASCADE
            );
            ''')
        self.__saveData()
        print("LOG: Banco de dados inicializado com schema relacional.")

    def __saveData(self):
        """Salva (commita) as alterações pendentes."""
        self.__db.commit()

    def __del__(self):
        """ Garante que a conexão com o banco seja fechada. """
        if self.__db:
            self.__db.close()
            print("LOG: Conexão com o banco de dados fechada.")

    
    def deleteItem(self, item: Entity) -> Optional[int]:
        """
        Remove um item do banco de dados.
        O banco de dados cuidará automaticamente da limpeza de referências
        (graças a 'ON DELETE CASCADE' e 'ON DELETE SET NULL').
        """
        
        tableName = None
        if isinstance(item, Person): tableName = "person"
        elif isinstance(item, Company): tableName = "company"
        elif isinstance(item, Department): tableName = "department"
        elif isinstance(item, Team): tableName = "team"
        elif isinstance(item, RPE): tableName = "rpe"
        elif isinstance(item, Objective): tableName = "objective"
        elif isinstance(item, KPI): tableName = "kpi"
        else:
            print(f"[ERRO] Não é possível deletar tipo desconhecido: {type(item)}")
            return None # Retorna None em caso de falha

        if not hasattr(item, 'id') or not item.id:
             print(f"[ERRO] Item {type(item)} não possui um ID válido para deleção.")
             return None

        try:
            with self.__db:
                cursor = self.__db.cursor()
                query = f"DELETE FROM {tableName} WHERE id = ?"
                cursor.execute(query, (item.id,))
                
                if cursor.rowcount == 0:
                    print(f"[AVISO] Nenhum registro encontrado em '{tableName}' com o ID {item.id}.")
                    return 1 # Retorna 1 se nada foi deletado
                else:
                    print(f"Item de '{tableName}' com ID {item.id} removido com sucesso.")
                    print("   [Limpeza] O banco de dados limpou as referências automaticamente.")
            return 0 # Retorna 0 para sucesso

        except sqlite3.Error as e:
            print(f"Erro ao deletar item de '{tableName}' (ROLLBACK executado): {e}")
            return None

    # --- MÉTODOS DE RELAÇÃO UM-PARA-MUITOS (Assign/Unassign) ---
    
    def _assign_foreign_key(self, table: str, fk_column: str, fk_id: str, primary_id: str) -> bool:
        """Função auxiliar genérica para definir um FK (relação 1-N)."""
        try:
            with self.__db:
                query = f"UPDATE {table} SET {fk_column} = ? WHERE id = ?"
                cursor = self.__db.execute(query, (fk_id, primary_id))
                if cursor.rowcount == 0:
                    print(f"Aviso: Nenhum registro encontrado em '{table}' com ID {primary_id}.")
                    return False
            print(f"'{table}.{fk_column}' atualizado para {fk_id} onde id = {primary_id}.")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao atribuir FK em '{table}': {e}")
            return False

    def _unassign_foreign_key(self, table: str, fk_column: str, primary_id: str) -> bool:
        """Função auxiliar genérica para limpar um FK (relação 1-N)."""
        return self._assign_foreign_key(table, fk_column, None, primary_id)

    # Relações de Department
    def assignDepartmentToCompany(self, department_id: str, company_id: str):
        return self._assign_foreign_key("department", "companyID", company_id, department_id)

    def assignDirectorToDepartment(self, director_id: str, department_id: str):
        return self._assign_foreign_key("department", "directorID", director_id, department_id)

    # Relações de Team
    def assignTeamToDepartment(self, team_id: str, department_id: str):
        return self._assign_foreign_key("team", "departmentID", department_id, team_id)

    def assignManagerToTeam(self, manager_id: str, team_id: str):
        return self._assign_foreign_key("team", "managerID", manager_id, team_id)

    # Relações de Person
    def assignPersonToCompany(self, person_id: str, company_id: str):
        return self._assign_foreign_key("person", "companyID", company_id, person_id)

    def assignPersonToDepartment(self, person_id: str, department_id: str):
        return self._assign_foreign_key("person", "departmentID", department_id, person_id)

    # Relações de RPE
    def assignResponsibleToRPE(self, responsible_id: str, rpe_id: str):
        return self._assign_foreign_key("rpe", "responsibleID", responsible_id, rpe_id)

    # Relações de Objective
    def assignObjectiveToRPE(self, objective_id: str, rpe_id: str):
        return self._assign_foreign_key("objective", "rpeID", rpe_id, objective_id)
        
    def assignResponsibleToObjective(self, responsible_id: str, objective_id: str):
        return self._assign_foreign_key("objective", "responsibleID", responsible_id, objective_id)

    # Relações de KPI
    def assignResponsibleToKPI(self, responsible_id: str, kpi_id: str):
        return self._assign_foreign_key("kpi", "responsibleID", responsible_id, kpi_id)


    # --- MÉTODOS DE RELAÇÃO MUITOS-PARA-MUITOS (Junction Tables) ---

    def _add_junction(self, table: str, col1_name: str, col1_id: str, col2_name: str, col2_id: str) -> bool:
        """Função auxiliar genérica para inserir em tabela de junção (N-N)."""
        try:
            with self.__db:
                query = f"INSERT INTO {table} ({col1_name}, {col2_name}) VALUES (?, ?)"
                self.__db.execute(query, (col1_id, col2_id))
            print(f"Relação adicionada em '{table}' ({col1_id}, {col2_id}).")
            return True
        except sqlite3.IntegrityError:
            print(f"Erro de Integridade: Relação ({col1_id}, {col2_id}) já existe em '{table}' ou IDs não existem.")
            return False
        except sqlite3.Error as e:
            print(f"Erro de DB ao adicionar em '{table}': {e}")
            return False

    def _delete_junction(self, table: str, col1_name: str, col1_id: str, col2_name: str, col2_id: str) -> bool:
        """Função auxiliar genérica para deletar de tabela de junção (N-N)."""
        try:
            with self.__db:
                query = f"DELETE FROM {table} WHERE {col1_name} = ? AND {col2_name} = ?"
                cursor = self.__db.execute(query, (col1_id, col2_id))
                if cursor.rowcount == 0:
                    print(f"Aviso: Relação ({col1_id}, {col2_id}) não encontrada em '{table}'.")
                else:
                    print(f"Relação removida de '{table}' ({col1_id}, {col2_id}).")
            return True
        except sqlite3.Error as e:
            print(f"Erro de DB ao deletar de '{table}': {e}")
            return False

    # team_members (Team <-> Person)
    def addTeamMember(self, team_id: str, person_id: str) -> bool:
        return self._add_junction("team_members", "teamID", team_id, "personID", person_id)

    def deleteTeamMember(self, team_id: str, person_id: str) -> bool:
        return self._delete_junction("team_members", "teamID", team_id, "personID", person_id)

    # person_responsibles (Person <-> Person)
    def addResponsibleToPerson(self, person_id: str, responsible_id: str) -> bool:
        return self._add_junction("person_responsibles", "personID", person_id, "responsibleID", responsible_id)

    def deleteResponsibleFromPerson(self, person_id: str, responsible_id: str) -> bool:
        return self._delete_junction("person_responsibles", "personID", person_id, "responsibleID", responsible_id)

    # company_directors (Company <-> Person)
    def addDirectorToCompany(self, company_id: str, person_id: str) -> bool:
        return self._add_junction("company_directors", "companyID", company_id, "personID", person_id)

    def deleteDirectorFromCompany(self, company_id: str, person_id: str) -> bool:
        return self._delete_junction("company_directors", "companyID", company_id, "personID", person_id)

    # company_rpes (Company <-> RPE)
    def addRpeToCompany(self, company_id: str, rpe_id: str) -> bool:
        return self._add_junction("company_rpes", "companyID", company_id, "rpeID", rpe_id)

    def deleteRpeFromCompany(self, company_id: str, rpe_id: str) -> bool:
        return self._delete_junction("company_rpes", "companyID", company_id, "rpeID", rpe_id)
        
    # department_rpes (Department <-> RPE)
    def addRpeToDepartment(self, department_id: str, rpe_id: str) -> bool:
        return self._add_junction("department_rpes", "departmentID", department_id, "rpeID", rpe_id)

    def deleteRpeFromDepartment(self, department_id: str, rpe_id: str) -> bool:
        return self._delete_junction("department_rpes", "departmentID", department_id, "rpeID", rpe_id)
        
    # team_rpes (Team <-> RPE)
    def addRpeToTeam(self, team_id: str, rpe_id: str) -> bool:
        return self._add_junction("team_rpes", "teamID", team_id, "rpeID", rpe_id)

    def deleteRpeFromTeam(self, team_id: str, rpe_id: str) -> bool:
        return self._delete_junction("team_rpes", "teamID", team_id, "rpeID", rpe_id)

    # objective_kpis (Objective <-> KPI)
    def addKpiToObjective(self, objective_id: str, kpi_id: str) -> bool:
        return self._add_junction("objective_kpis", "objectiveID", objective_id, "kpiID", kpi_id)

    def deleteKpiFromObjective(self, objective_id: str, kpi_id: str) -> bool:
        return self._delete_junction("objective_kpis", "objectiveID", objective_id, "kpiID", kpi_id)
    
    def updateItem(self, item: Entity) -> int:
        """
        Atualiza os campos diretos de um item no banco de dados.
        NOTA: Este método NÃO atualiza as relações (listas como employeeIds,
        rpeIds, etc.). Use os métodos add/delete (ex: addTeamMember) 
        para gerenciar relações.
        """
        
        query = ""
        params = ()

        try:
            # --- Bloco Person ---
            if isinstance(item, Person):
                query = """UPDATE person 
                           SET name = ?, cpf = ?, companyID = ?, departmentID = ?, 
                               role = ?, email = ?, password = ?
                           WHERE id = ?"""
                params = (item.name, item.cpf, item.companyID, item.departmentID,
                          item.role, item.email, item.password, 
                          item.id) # ID por último

            # --- Bloco Company ---
            elif isinstance(item, Company):
                query = """UPDATE company
                           SET name = ?, cnpj = ?
                           WHERE id = ?"""
                params = (item.name, item.cnpj, item.id)

            # --- Bloco Department ---
            elif isinstance(item, Department):
                query = """UPDATE department
                           SET name = ?, companyID = ?, directorID = ?
                           WHERE id = ?"""
                params = (item.name, item.companyID, item.directorID, item.id)
            
            # --- Bloco Team ---
            elif isinstance(item, Team):
                query = """UPDATE team
                           SET name = ?, departmentID = ?, managerID = ?
                           WHERE id = ?"""
                params = (item.name, item.departmentID, item.managerID, item.id)

            # --- Bloco RPE ---
            elif isinstance(item, RPE):
                query = """UPDATE rpe
                           SET description = ?, responsibleID = ?, date = ?
                           WHERE id = ?"""
                params = (item.description, item.responsibleID, item.date, item.id)

            # --- Bloco Objective ---
            elif isinstance(item, Objective):
                query = """UPDATE objective
                           SET description = ?, rpeID = ?, responsibleID = ?, date = ?
                           WHERE id = ?"""
                params = (item.description, item.rpeID, item.responsibleID, item.date, item.id)

            # --- Bloco KPI ---
            elif isinstance(item, KPI):
                # O campo 'data' ainda pode ser um JSON, se for um vetor
                dataText = json.dumps(item.data) 
                query = """UPDATE kpi
                           SET description = ?, responsibleID = ?, date = ?, data = ?, goal = ?
                           WHERE id = ?"""
                params = (item.description, item.responsibleID, item.date, dataText, item.goal,
                          item.id)
            
            # --- Bloco Else ---
            else:
                print(f"[ERRO] Tipo de item desconhecido para atualização: {type(item)}")
                return 1

            # Executa a query dentro de uma transação
            with self.__db:
                cursor = self.__db.execute(query, params)
                if cursor.rowcount == 0:
                     print(f"[AVISO] Nenhum {type(item).__name__} atualizado (ID: {item.id}). ID não encontrado.")
                     return 1
            
            print(f"{type(item).__name__} (ID: {item.id}) atualizado com sucesso.")
            return 0 # Sucesso

        except sqlite3.Error as e:
            print(f"Erro ao atualizar {type(item).__name__} (ID: {item.id}): {e}")
            return 1 # Falha
        
        # --- NOVO MÉTODO AUXILIAR PARA PESSOAS ---
    
    def _build_person_from_row(self, cursor: sqlite3.Cursor, row: sqlite3.Row) -> Optional[Person]:
        """
        Constrói um objeto Person/Manager/Director a partir de uma linha do banco.
        Esta função auxiliar é usada por getPersonByID e getPersonByEmail.
        """
        if not row:
            return None
            
        params = dict(row)
        personID = params["id"]
        role = params.get("role")
        
        # Hidratação: Busca IDs de responsabilidade se for Manager ou Director
        if role == "Manager" or role == "Director":
            cursor.execute("SELECT responsibleID FROM person_responsibles WHERE personID = ?", (personID,))
            id_rows = cursor.fetchall()
            params["responsibleIds"] = [r["responsibleID"] for r in id_rows]
            
        # Factory: Constrói o objeto da classe correta
        try:
            if role == "Manager":
                return Manager(**params)
            elif role == "Director":
                return Director(**params)
            else:
                # Limpa o kwarg se a classe Person não o esperar
                if "responsibleIds" in params:
                    del params["responsibleIds"]
                return Person(**params)
        except TypeError as e:
            print(f"[ERRO] Falha ao construir objeto Person/Manager. Verifique os construtores.")
            print(f"   Erro: {e}")
            print(f"   Parâmetros: {params}")
            return None

# --- MÉTODOS DE BUSCA "GET" ---

    def getPersonByID(self, personID: str) -> Optional[Person]:
        """
        Retorna um objeto Person (ou Manager/Director) pelo ID, 
        hidratando as listas de IDs a partir das tabelas de junção.
        """
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM person WHERE id = ?", (personID,))
            row = cursor.fetchone()
            
            if not row:
                print(f"[AVISO] Nenhuma pessoa encontrada com o ID {personID}.")
                return None
                
            return self._build_person_from_row(cursor, row)

        except sqlite3.Error as e:
            print(f"Erro ao buscar pessoa (ID: {personID}): {e}")
            return None

    def getPersonByEmail(self, email: str) -> Optional[Person]:
        """
        Retorna um objeto Person (ou Manager/Director) pelo Email.
        """
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM person WHERE email = ?", (email,))
            row = cursor.fetchone()
            
            if not row:
                print(f"[AVISO] Nenhuma pessoa encontrada com o Email {email}.")
                return None
                
            return self._build_person_from_row(cursor, row)

        except sqlite3.Error as e:
            print(f"Erro ao buscar pessoa (Email: {email}): {e}")
            return None

    def getCompanyByID(self, companyID: str) -> Optional[Company]:
        """ Retorna um objeto Company pelo ID, hidratando suas listas de junção. """
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM company WHERE id = ?", (companyID,))
            row = cursor.fetchone()
            if not row: return None
            
            params = dict(row)
            
            # Hidratação 1: 'directorsIds' (N-N)
            cursor.execute("SELECT personID FROM company_directors WHERE companyID = ?", (companyID,))
            params["directorsIds"] = [r["personID"] for r in cursor.fetchall()]
            
            # Hidratação 2: 'rpeIds' (N-N)
            cursor.execute("SELECT rpeID FROM company_rpes WHERE companyID = ?", (companyID,))
            params["rpeIds"] = [r["rpeID"] for r in cursor.fetchall()]

            # Hidratação 3: 'departmentsIds' (1-N)
            cursor.execute("SELECT id FROM department WHERE companyID = ?", (companyID,))
            params["departmentsIds"] = [r["id"] for r in cursor.fetchall()]
            
            return Company(**params)
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar company (ID: {companyID}): {e}")
            return None

    def getDepartmentByID(self, departmentID: str) -> Optional[Department]:
        """ Retorna um objeto Department pelo ID, hidratando suas listas de junção. """
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM department WHERE id = ?", (departmentID,))
            row = cursor.fetchone()
            if not row: return None
            
            params = dict(row)
            
            # Hidratação 1: 'rpeIds' (N-N)
            cursor.execute("SELECT rpeID FROM department_rpes WHERE departmentID = ?", (departmentID,))
            params["rpeIds"] = [r["rpeID"] for r in cursor.fetchall()]

            # Hidratação 2: 'teamsIds' (1-N)
            cursor.execute("SELECT id FROM team WHERE departmentID = ?", (departmentID,))
            params["teamsIds"] = [r["id"] for r in cursor.fetchall()]
            
            return Department(**params)
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar department (ID: {departmentID}): {e}")
            return None

    def getTeamByID(self, teamID: str) -> Optional[Team]:
        """ Retorna um objeto Team pelo ID, hidratando suas listas de junção. """
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM team WHERE id = ?", (teamID,))
            row = cursor.fetchone()
            if not row: return None
            
            params = dict(row)
            
            # Hidratação 1: 'employeeIds' (N-N)
            cursor.execute("SELECT personID FROM team_members WHERE teamID = ?", (teamID,))
            params["employeeIds"] = [r["personID"] for r in cursor.fetchall()]
            
            # Hidratação 2: 'rpeIds' (N-N)
            cursor.execute("SELECT rpeID FROM team_rpes WHERE teamID = ?", (teamID,))
            params["rpeIds"] = [r["rpeID"] for r in cursor.fetchall()]
            
            return Team(**params)
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar time (ID: {teamID}): {e}")
            return None

    def getRPEByID(self, rpeID: str) -> Optional[RPE]:
        """ Retorna um objeto RPE pelo ID, hidratando suas listas de junção. """
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM rpe WHERE id = ?", (rpeID,))
            row = cursor.fetchone()
            if not row: return None
            
            params = dict(row)
            
            # Hidratação 1: 'objectivesIds' (1-N)
            cursor.execute("SELECT id FROM objective WHERE rpeID = ?", (rpeID,))
            params["objectivesIds"] = [r["id"] for r in cursor.fetchall()]
            
            return RPE(**params)
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar RPE (ID: {rpeID}): {e}")
            return None

    def getObjectiveByID(self, objectiveID: str) -> Optional[Objective]:
        """ Retorna um objeto Objective pelo ID, hidratando suas listas de junção. """
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM objective WHERE id = ?", (objectiveID,))
            row = cursor.fetchone()
            if not row: return None
            
            params = dict(row)
            
            # Hidratação 1: 'kpiIds' (N-N)
            cursor.execute("SELECT kpiID FROM objective_kpis WHERE objectiveID = ?", (objectiveID,))
            params["kpiIds"] = [r["kpiID"] for r in cursor.fetchall()]
            
            # NOTA: O schema anterior tinha 'krIds'. 
            # Se você tiver uma tabela 'kr' e 'objective_krs', adicione a 
            # hidratação para 'krIds' aqui, seguindo o mesmo padrão.
            # ex: params["krIds"] = ...
            
            return Objective(**params)
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar objective (ID: {objectiveID}): {e}")
            return None

    def getKPIByID(self, kpiID: str) -> Optional[KPI]:
        """ Retorna um objeto KPI pelo ID, desserializando o campo 'data'. """
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM kpi WHERE id = ?", (kpiID,))
            row = cursor.fetchone()
            if not row: return None
            
            params = dict(row)
            
            # Desserialização: O campo 'data' ainda era um JSON
            if params.get("data"):
                try:
                    params["data"] = json.loads(params["data"])
                except json.JSONDecodeError:
                    print(f"Aviso: Campo 'data' do KPI {kpiID} não é um JSON válido.")
                    params["data"] = [] # Ou None
            else:
                params["data"] = [] # Ou None
            
            return KPI(**params)
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar KPI (ID: {kpiID}): {e}")
            return None