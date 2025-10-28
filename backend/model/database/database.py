import sqlite3
import json
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
                responsibleID TEXT,
                date TEXT,
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
            
            CREATE TABLE IF NOT EXISTS rpe_objectives (
                rpeID TEXT NOT NULL,
                objectiveID TEXT NOT NULL,
                PRIMARY KEY (rpeID, objectiveID),
                FOREIGN KEY(rpeID) REFERENCES rpe(id) ON DELETE CASCADE,
                FOREIGN KEY(objectiveID) REFERENCES objective(id) ON DELETE CASCADE
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
    
    def deleteItem(self, id: str) -> bool:
        """
        Tenta deletar um item (entidade) do banco de dados usando seu ID.
        
        A deleção se baseia nas regras de integridade referencial (FOREIGN KEY ON DELETE CASCADE)
        para limpar as tabelas de junção e as entidades dependentes.
        
        Retorna True se pelo menos um item for deletado, False caso contrário.
        """
        
        # Lista de todas as tabelas que usam 'id' como PRIMARY KEY.
        # As tabelas de junção NÃO são incluídas, pois a exclusão é tratada
        # pelo ON DELETE CASCADE das tabelas principais.
        tables_to_check = [
            "company", "department", "team", 
            "person", "rpe", "objective", "kpi"
        ]
        
        total_deleted_rows = 0
        
        try:
            with self.__db: # Garante a atomicidade (commit/rollback)
                
                for table in tables_to_check:
                    query = f"DELETE FROM {table} WHERE id = ?"
                    cursor = self.__db.execute(query, (id,))
                    
                    if cursor.rowcount > 0:
                        # Se rowcount > 0, o item foi encontrado e deletado nessa tabela.
                        # O CASCADE do SQLite cuidará das tabelas dependentes (junção e outras).
                        print(f"Registro (ID: {id}) deletado com sucesso da tabela '{table}'.")
                        total_deleted_rows += cursor.rowcount
                        break # O ID só pode pertencer a uma tabela principal, então paramos.
                        
            if total_deleted_rows > 0:
                return True
            else:
                print(f"[AVISO] Nenhum item encontrado com o ID: {id} em nenhuma tabela principal.")
                return False

        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao deletar item com ID {id}: {e}")
            # Em caso de erro, o 'with self.__db:' já faz o rollback
            return False
    
    def addItem(self, item: Entity) -> Optional[int]:
        """
        Adiciona um novo item no banco de dados.
        NOTA: Este método só insere a entidade principal. 
        As relações (listas de IDs) devem ser adicionadas separadamente 
        após a inserção principal (e.g., usando métodos 'add...').
        """
        
        query = ""
        params = ()
        entity_name = type(item).__name__

        # Usa o 'with self.__db:' para garantir que o commit ou rollback ocorra
        try:
            with self.__db: 
                # --- Bloco Person ---
                if isinstance(item, Person):
                    
                    # Verificação de unicidade (opcional, mas recomendado)
                    if self.getPersonByID(item.id):
                        print(f"[ERRO] Pessoa com ID {item.id} já existe.")
                        return 1

                    query = """INSERT INTO person (
                               id, name, cpf, companyID, departmentID, role, email, password
                               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                    params = (item.id, item.name, item.cpf, 
                              item.companyID, item.departmentID, 
                              item.role, item.email, item.password)

                # --- Bloco Company ---
                elif isinstance(item, Company):
                    query = """INSERT INTO company (
                               id, name, cnpj
                               ) VALUES (?, ?, ?)"""
                    params = (item.id, item.name, item.cnpj)

                # --- Bloco Department ---
                elif isinstance(item, Department):
                    query = """INSERT INTO department (
                               id, name, companyID, directorID
                               ) VALUES (?, ?, ?, ?)"""
                    params = (item.id, item.name, item.companyID, item.directorID)

                # --- Bloco Team ---
                elif isinstance(item, Team):
                    query = """INSERT INTO team (
                               id, name, departmentID, managerID
                               ) VALUES (?, ?, ?, ?)"""
                    params = (item.id, item.name, item.departmentID, item.managerID)

                # --- Bloco RPE ---
                elif isinstance(item, RPE):
                    query = """INSERT INTO rpe (
                               id, description, responsibleID, date
                               ) VALUES (?, ?, ?, ?)"""
                    params = (item.id, item.description, item.responsibleID, item.date)

                # --- Bloco Objective ---
                elif isinstance(item, Objective):
                    query = """INSERT INTO objective (
                               id, description, responsibleID, date
                               ) VALUES (?, ?, ?, ?)"""
                    params = (item.id, item.description, item.responsibleID, item.date)

                # --- Bloco KPI (usado para KPI e KR, com 'goal' e 'data' opcionais) ---
                elif isinstance(item, KPI):
                    # O campo 'data' (vetor de floats) ainda precisa ser serializado
                    dataText = json.dumps(getattr(item, 'data', [])) 
                    # O campo 'goal' e 'current_value' são tratados. 
                    # Se não existirem no objeto KPI, use NULL (None em Python) ou 0.0
                    goal = getattr(item, 'goal', None)
                    
                    query = """INSERT INTO kpi (
                               id, description, responsibleID, date, data, goal,
                               ) VALUES (?, ?, ?, ?, ?, ?)"""
                    params = (item.id, item.description, item.responsibleID, item.date, 
                              dataText, goal)

                else:
                    print(f"[ERRO] Tipo de item desconhecido para inserção: {entity_name}")
                    return 1

                # Executa a inserção
                self.__db.execute(query, params)
                
                print(f"{entity_name} {item.id} inserido com sucesso.")

            # Retorno de sucesso
            return 0 

        except sqlite3.IntegrityError as e:
            # Captura erros de UNIQUE (como CNPJ ou CPF duplicado)
            print(f"[ERRO] Falha de Integridade ao adicionar {entity_name} (ID: {item.id}): {e}")
            return 1
        except sqlite3.Error as e:
            print(f"[ERRO] Erro SQL ao adicionar {entity_name} (ID: {item.id}): {e}")
            return 1

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

    #Relações de Objective
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

    # rpe_objectives (RPE <-> Objective)
    def addObjectiveToRpe(self, objective_id: str, rpe_id: str):
        return self._add_junction("rpe_objectives","rpeID",rpe_id, "objectiveID",objective_id)

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

            # --- Bloco KR ---
            elif isinstance(item, KR):
                dataText = json.dumps(item.data) 
                query = """UPDATE kpi
                           SET description = ?, responsibleID = ?, date = ?, data = ?, goal = ?
                           WHERE id = ?"""
                params = (item.description, item.responsibleID, item.date, dataText, item.goal,
                          item.id)

            # --- Bloco KPI ---
            elif isinstance(item, KPI):
                dataText = json.dumps(item.data) 
                query = """UPDATE kpi
                           SET description = ?, responsibleID = ?, date = ?, data = ?, goal = ?
                           WHERE id = ?"""
                params = (item.description, item.responsibleID, item.date, dataText, None,
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
        """ Retorna um objeto RPE pelo ID, hidratando 'objectivesIds' pela tabela de junção. """
        try:
            # (Assumindo que self.__db.row_factory = sqlite3.Row foi definido no __init__)
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM rpe WHERE id = ?", (rpeID,))
            row = cursor.fetchone()
            if not row: return None
            
            params = dict(row)
            
            # Hidratação CORRETA: 'objectivesIds' (N-para-N)
            # Busca na tabela de junção 'rpe_objectives'
            cursor.execute("SELECT objectiveID FROM rpe_objectives WHERE rpeID = ?", (rpeID,))
            
            # O construtor do RPE espera 'objectivesIds'
            params["objectivesIds"] = [r["objectiveID"] for r in cursor.fetchall()]
            
            return RPE(**params)
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar RPE (ID: {rpeID}): {e}")
            return None

    def getObjectiveByID(self, objectiveID: str) -> Optional[Objective]:
        """ Retorna um objeto Objective pelo ID, hidratando e separando 'kpiIds' e 'krIds'. """
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM objective WHERE id = ?", (objectiveID,))
            row = cursor.fetchone()
            if not row: return None
            
            params = dict(row)
            
            # Hidratação 1: 'kpiIds' (N-N)
            # Busca IDs que estão na junção E têm 'goal' NULO na tabela 'kpi'
            query_kpis = """
                SELECT OK.kpiID FROM objective_kpis AS OK
                JOIN kpi AS K ON OK.kpiID = K.id
                WHERE OK.objectiveID = ? AND K.goal IS NULL
            """
            cursor.execute(query_kpis, (objectiveID,))
            params["kpiIds"] = [r["kpiID"] for r in cursor.fetchall()]

            # Hidratação 2: 'krIds' (N-N)
            # Busca IDs que estão na junção E têm 'goal' NÃO NULO na tabela 'kpi'
            query_krs = """
                SELECT OK.kpiID FROM objective_kpis AS OK
                JOIN kpi AS K ON OK.kpiID = K.id
                WHERE OK.objectiveID = ? AND K.goal IS NOT NULL
            """
            cursor.execute(query_krs, (objectiveID,))
            params["krIds"] = [r["kpiID"] for r in cursor.fetchall()]
            
            return Objective(**params)
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar objective (ID: {objectiveID}): {e}")
            return None

    def getKPIByID(self, kpiID: str) -> Optional[KPI]:
        """ 
        Retorna um objeto KPI pelo ID. 
        Assume que um KPI tem 'data', mas não tem 'goal'.
        """
        try:
            cursor = self.__db.cursor()
            # Busca um item que DEVE ser um KPI (goal IS NULL)
            cursor.execute("SELECT * FROM kpi WHERE id = ? AND goal IS NULL", (kpiID,))
            row = cursor.fetchone()
            if not row: 
                print(f"[Aviso] Nenhum KPI (com goal=NULL) encontrado com ID {kpiID}.")
                return None
            
            params = dict(row)
            
            # Desserialização: O campo 'data' (que o KPI TEM)
            if params.get("data"):
                try:
                    params["data"] = json.loads(params["data"])
                except json.JSONDecodeError:
                    params["data"] = [] # Padrão
            else:
                params["data"] = [] # Padrão
            
            # Limpeza: O KPI NÃO TEM 'goal'. Removemos antes de chamar o construtor.
            if "goal" in params:
                del params["goal"]
            
            # O construtor KPI(**params) agora recebe 'data', mas não 'goal'.
            return KPI(**params)
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar KPI (ID: {kpiID}): {e}")
            return None
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar KPI (ID: {kpiID}): {e}")
            return None
        
    def getKRByID(self, krID: str) -> Optional[KR]: # Alterei o tipo de retorno para KR
        """ 
        Retorna um objeto KR pelo ID. 
        Assume que um KR tem 'data' e 'goal'.
        """
        try:
            cursor = self.__db.cursor()
            # Busca um item que DEVE ser um KR (goal IS NOT NULL)
            cursor.execute("SELECT * FROM kpi WHERE id = ? AND goal IS NOT NULL", (krID,))
            row = cursor.fetchone()
            if not row: 
                print(f"[Aviso] Nenhum KR (com goal!=NULL) encontrado com ID {krID}.")
                return None
            
            params = dict(row)
            
            # Desserialização: O campo 'data' (que o KR TEM)
            if params.get("data"):
                try:
                    params["data"] = json.loads(params["data"])
                except json.JSONDecodeError:
                    params["data"] = []
            else:
                params["data"] = []
            
            # O construtor KR(**params) recebe 'data' E 'goal'.
            return KR(**params)
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar KR (ID: {krID}): {e}")
            return None
        
    def changeTeamManager(self, teamID: str, personID: str):
        """
        Muda o managerID de um time (team) para um novo personID.
        Se personID for None, o campo managerID será NULL.
        """
        if personID is None or personID == "":
            personID_to_set = None  # SQLite aceita None para NULL
        else:
            personID_to_set = personID

        try:
            with self.__db: # Inicia uma transação
                cursor = self.__db.execute(
                    """UPDATE team 
                       SET managerID = ? 
                       WHERE id = ?""", 
                    (personID_to_set, teamID)
                )
                
                if cursor.rowcount == 0:
                    print(f"[AVISO] Nenhum time encontrado com o ID {teamID}. Gerente não alterado.")
                    return 1 # Código de falha
                    
            print(f"Gerente do Time (ID: {teamID}) alterado para PersonID: {personID_to_set}.")
            return 0 # Código de sucesso
            
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao mudar Gerente do Time (ID: {teamID}): {e}")
            return 1 # Código de falha

    def changeDepartmentDirector(self, departmentID: str, personID: str):
        """
        Muda o directorID de um departamento para um novo personID.
        Se personID for None, o campo directorID será NULL.
        """
        if personID is None or personID == "":
            personID_to_set = None
        else:
            personID_to_set = personID

        try:
            with self.__db: # Inicia uma transação
                cursor = self.__db.execute(
                    """UPDATE department 
                       SET directorID = ? 
                       WHERE id = ?""", 
                    (personID_to_set, departmentID)
                )
                
                if cursor.rowcount == 0:
                    print(f"[AVISO] Nenhum departamento encontrado com o ID {departmentID}. Diretor não alterado.")
                    return 1 # Código de falha
                    
            print(f"Diretor do Departamento (ID: {departmentID}) alterado para PersonID: {personID_to_set}.")
            return 0 # Código de sucesso

        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao mudar Diretor do Departamento (ID: {departmentID}): {e}")
            return 1 # Código de falha
        
    def isObjectiveTeamOrDepartmentLevel(self, objectiveID: str) -> bool:
        """
        Verifica se um Objetivo está associado a pelo menos um Team OU a pelo menos um Department.
        
        Isso é feito verificando o caminho Objective -> RPE -> (Team OR Department).
        Retorna True se houver associação com Team ou Department, False caso contrário.
        """
        try:
            cursor = self.__db.cursor()
            
            # Consulta SQL Otimizada: 
            # Verifica se EXISTE algum RPE que está ligado ao objectiveID E
            # que também está ligado a um team OU a um department.
            
            query = """
                SELECT 1 FROM rpe_objectives AS RO
                WHERE RO.objectiveID = ?
                  AND (
                    -- Verifica se o RPE está ligado a um TEAM
                    EXISTS (
                        SELECT 1 FROM team_rpes AS TR 
                        WHERE TR.rpeID = RO.rpeID
                    )
                    OR
                    -- Verifica se o RPE está ligado a um DEPARTMENT
                    EXISTS (
                        SELECT 1 FROM department_rpes AS DR 
                        WHERE DR.rpeID = RO.rpeID
                    )
                  )
                LIMIT 1;
            """
            
            cursor.execute(query, (objectiveID,))
            
            # Se fetchone() retornar uma linha, significa que existe pelo menos uma associação.
            return cursor.fetchone() is not None

        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao verificar nível do Objetivo {objectiveID}: {e}")
            # Em caso de erro, assumimos que a verificação falhou.
            return False
    
    def isRPETeamOrDepartmentLevel(self, rpeID: str) -> bool:
        """
        Verifica se um RPE está associado a pelo menos um Team OU a pelo menos um Department,
        consultando diretamente as tabelas de junção 'team_rpes' e 'department_rpes'.
        
        Retorna True se houver associação com Team ou Department, False caso contrário.
        """
        try:
            cursor = self.__db.cursor()
            
            # Consulta SQL Otimizada:
            # Verifica se o rpeID existe em team_rpes OU em department_rpes.
            query = """
                SELECT 1 FROM team_rpes AS TR 
                WHERE TR.rpeID = ?
                
                UNION ALL
                
                SELECT 1 FROM department_rpes AS DR 
                WHERE DR.rpeID = ?
                
                LIMIT 1;
            """
            
            # Passamos o rpeID duas vezes para a consulta (uma para cada WHERE)
            cursor.execute(query, (rpeID, rpeID))
            
            # Se fetchone() retornar uma linha, significa que o RPE está associado a pelo
            # menos um Team OU a um Department.
            return cursor.fetchone() is not None

        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao verificar nível do RPE {rpeID}: {e}")
            # Em caso de erro, assume que a verificação falhou.
            return False