import sqlite3
import json
from typing import Optional

from ..entities.entity import Entity
from ..entities.person import Person
from ..entities.company import Company
from ..entities.manager import Manager
from ..entities.director import Director
from ..entities.department import Department
from ..entities.team import Team
from ..entities.rpe import RPE
from ..entities.objective import Objective
from ..entities.kpi import KPI
from ..entities.kr import KR


class Database:

    def __init__(self, db_path: str = 'backend/model/database/database.db'):
        
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
                teamID TEXT,
                role TEXT,
                email TEXT,
                password TEXT,
                FOREIGN KEY(companyID) REFERENCES company(id) ON DELETE SET NULL,
                FOREIGN KEY(departmentID) REFERENCES department(id) ON DELETE SET NULL,
                FOREIGN KEY(teamID) REFERENCES team(id) ON DELETE SET NULL
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

    
    def deleteItemByObject(self, item: Entity) -> Optional[int]:
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
    
    def deleteItembyID(self, id: str) -> bool:
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
                    # Se já existe pessoa, não insere novamente
                    if not self.getPersonByID(item.id):
                        query = """INSERT INTO person (
                                id, name, cpf, companyID, departmentID, teamID, role, email, password
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                        params = (item.id, item.name, item.cpf, 
                                item.companyID, item.departmentID, item.teamID,
                                getattr(item, 'role', None), item.email, item.password)
                        print("chegou")
                        self.__db.execute(query, params)
                        print("chegou")
                        print(f"Person {item.id} inserida com sucesso.")
                    else:
                        print(f"[AVISO] Person {item.id} já existe, ignorando inserção.")

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
                               id, description, responsibleID, date, data, goal
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
        
    def cleanupDataRelationships(self, data_id: str, data_type: str) -> None:
        """
        Remove todas as referências de um objeto Data (RPE, Objective, KPI, KR)
        das tabelas de junção antes de sua exclusão.
        """
        cursor = self.__db.cursor()
        
        try:
            if data_type in ["KPI", "KR"]:
                # KPI/KR está ligado a Objective
                cursor.execute("DELETE FROM objective_kpis WHERE kpiID = ?", (data_id,))

            elif data_type == "Objective":
                # Objective está ligado a RPEs
                cursor.execute("DELETE FROM rpe_objectives WHERE objectiveID = ?", (data_id,))
                # Objective está ligado a KPIs/KRs (caso não use CASCADE)
                cursor.execute("DELETE FROM objective_kpis WHERE objectiveID = ?", (data_id,))

            elif data_type == "RPE":
                # RPE está ligado a Company, Department e Team
                cursor.execute("DELETE FROM company_rpes WHERE rpeID = ?", (data_id,))
                cursor.execute("DELETE FROM department_rpes WHERE rpeID = ?", (data_id,))
                cursor.execute("DELETE FROM team_rpes WHERE rpeID = ?", (data_id,))
                # RPE está ligado a Objectives (caso não use CASCADE)
                cursor.execute("DELETE FROM rpe_objectives WHERE rpeID = ?", (data_id,))
            
            # Confirma as exclusões das relações
            self.__db.commit()
            
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao limpar relações do {data_type} (ID: {data_id}): {e}")
            # É importante fazer um rollback se a exclusão da relação falhar, 
            # para não prosseguir com a exclusão do item principal
            self.__db.rollback() 
            raise # Levanta o erro para interromper a operação principal
    
    def cleanupPersonRelationships(self, person_id: str) -> None:
        """
        Remove todas as referências de uma Pessoa nas tabelas de junção e
        nos campos de Foreign Key (diretor, gerente, responsável) antes de sua exclusão.
        
        :param person_id: O ID da pessoa a ser excluída.
        """
        cursor = self.__db.cursor()
        
        try:
            # --- 1. LIMPAR CARGOS DE LIDERANÇA (SET NULL) ---
            
            # 1a. Remove a pessoa como DIRETOR de um Departamento
            # Garante que o campo FK na tabela 'department' seja nulo.
            cursor.execute("UPDATE department SET directorID = NULL WHERE directorID = ?", (person_id,))
            
            # 1b. Remove a pessoa como GERENTE de um Time
            # Garante que o campo FK na tabela 'team' seja nulo.
            cursor.execute("UPDATE team SET managerID = NULL WHERE managerID = ?", (person_id,))

            # --- 2. LIMPAR RESPONSABILIDADE POR DATA (SET NULL) ---
            # Todos os objetos Data (RPE, Objective, KPI, KR) têm responsibleID.
            
            # 2a. RPEs
            cursor.execute("UPDATE rpe SET responsibleID = NULL WHERE responsibleID = ?", (person_id,))
            
            # 2b. Objectives
            cursor.execute("UPDATE objective SET responsibleID = NULL WHERE responsibleID = ?", (person_id,))

            # 2c. KPIs (Inclui KRs, se usarem a mesma tabela)
            cursor.execute("UPDATE kpi SET responsibleID = NULL WHERE responsibleID = ?", (person_id,))
            
            # --- 3. REMOVER DE TABELAS DE JUNÇÃO ---
            
            # 3a. Remove a pessoa como MEMBRO de um Time
            # Assumindo uma tabela de junção 'team_members' ou 'team_person'.
            # A cláusula IGNORE é usada para evitar falhas caso a tabela não exista com esse nome.
            try:
                cursor.execute("DELETE FROM team_members WHERE personID = ?", (person_id,))
            except sqlite3.OperationalError:
                pass # Tabela 'team_members' pode não existir, o que não impede a deleção.

            # 3b. Remove o ID da pessoa das listas internas de responsáveis
            # (Se você tiver listas armazenadas no DB em JSON, precisaria de uma lógica mais complexa de UPDATE JSON)
            
            # Confirma todas as alterações
            self.__db.commit()
            
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao limpar relações da Pessoa (ID: {person_id}): {e}")
            self.__db.rollback() 
            raise # Levanta o erro para interromper a operação principal

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
    def assignPersonToTeam(self, person_id: str, team_id: str):
        return self._assign_foreign_key("person", "teamID", team_id, person_id)
    
    def unassignPersonToTeam(self, person_id: str) -> bool:
        return self._unassign_foreign_key("person", "teamID", person_id)

    def assignPersonToDepartment(self, person_id: str, department_id: str):
        return self._assign_foreign_key("person", "departmentID", department_id, person_id)
    
    def unassignPersonToDepartment(self, person_id: str) -> bool:
        return self._unassign_foreign_key("person", "departmentID", person_id)
    
    def assignPersonToCompany(self, person_id: str, company_id: str):
        return self._assign_foreign_key("person", "companyID", company_id, person_id)
    
    def unassignPersonToCompany(self, person_id: str) -> bool:
        return self._unassign_foreign_key("person", "companyID", person_id)

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
    
    def deleteObjectiveFromRpe(self, objective_id: str, rpe_id: str) -> bool:
        return self._delete_junction("rpe_objectives", "rpeID", rpe_id, "objectiveID", objective_id)

    # objective_kpis (Objective <-> KPI)
    def addKpiToObjective(self, objective_id: str, kpi_id: str) -> bool:
        return self._add_junction("objective_kpis", "objectiveID", objective_id, "kpiID", kpi_id)

    def deleteKpiFromObjective(self, objective_id: str, kpi_id: str) -> bool:
        return self._delete_junction("objective_kpis", "objectiveID", objective_id, "kpiID", kpi_id)
    
    def updateItem(self, item: Entity) -> int:
        """
        Atualiza os campos diretos de um item no banco de dados.
        Agora também atualiza as relações RPEIDs para Team, Department e Company.
        """
        
        query = ""
        params = ()

        try:
            # --- Bloco Person ---
            if isinstance(item, Person):
                query = """UPDATE person 
                        SET name = ?, cpf = ?, companyID = ?, departmentID = ?, teamID = ?,
                            role = ?, email = ?, password = ?
                        WHERE id = ?"""
                params = (item.name, item.cpf, item.companyID, item.departmentID, item.teamID,
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
                        SET description = ?, responsibleID = ?, date = ?
                        WHERE id = ?"""
                params = (item.description, item.responsibleID, item.date, item.id)

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
                
                # --- ATUALIZAÇÃO DOS RPEIDs PARA TEAM, DEPARTMENT E COMPANY ---
                
                # Team RPEs
                if isinstance(item, Team) and hasattr(item, 'RPEIDs'):
                    # Primeiro remove todos os RPEs existentes
                    self.__db.execute("DELETE FROM team_rpes WHERE teamID = ?", (item.id,))
                    # Depois insere os novos RPEs
                    for rpe_id in item.RPEIDs:
                        self.__db.execute(
                            "INSERT INTO team_rpes (teamID, rpeID) VALUES (?, ?)",
                            (item.id, rpe_id)
                        )
                    print(f"RPEIDs do Team {item.id} atualizados: {item.RPEIDs}")
                
                # Department RPEs
                elif isinstance(item, Department) and hasattr(item, 'RPEIDs'):
                    # Remove todos os RPEs existentes
                    self.__db.execute("DELETE FROM department_rpes WHERE departmentID = ?", (item.id,))
                    # Insere os novos RPEs
                    for rpe_id in item.RPEIDs:
                        self.__db.execute(
                            "INSERT INTO department_rpes (departmentID, rpeID) VALUES (?, ?)",
                            (item.id, rpe_id)
                        )
                    print(f"RPEIDs do Department {item.id} atualizados: {item.RPEIDs}")
                
                # Company RPEs
                elif isinstance(item, Company) and hasattr(item, 'RPEIDs'):
                    # Remove todos os RPEs existentes
                    self.__db.execute("DELETE FROM company_rpes WHERE companyID = ?", (item.id,))
                    # Insere os novos RPEs
                    for rpe_id in item.RPEIDs:
                        self.__db.execute(
                            "INSERT INTO company_rpes (companyID, rpeID) VALUES (?, ?)",
                            (item.id, rpe_id)
                        )
                    print(f"RPEIDs da Company {item.id} atualizados: {item.RPEIDs}")
                
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
        """Retorna um objeto Company pelo ID, hidratando suas listas de junção."""
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM company WHERE id = ?", (companyID,))
            row = cursor.fetchone()
            if not row: 
                return None
            
            # CORREÇÃO: Criar dicionário manualmente usando description
            columns = [description[0] for description in cursor.description]
            params = dict(zip(columns, row))
            
            # Hidratação 1: 'directorsIds' (N-N)
            cursor.execute("SELECT personID FROM company_directors WHERE companyID = ?", (companyID,))
            # CORREÇÃO: Usar índice 0 em vez de chave de dicionário
            params["directorsIDs"] = [r[0] for r in cursor.fetchall()]
            
            # Hidratação 2: 'rpeIds' (N-N)
            cursor.execute("SELECT rpeID FROM company_rpes WHERE companyID = ?", (companyID,))
            params["RPEIDs"] = [r[0] for r in cursor.fetchall()]

            # Hidratação 3: 'departmentsIds' (1-N)
            cursor.execute("SELECT id FROM department WHERE companyID = ?", (companyID,))
            params["departmentsIDs"] = [r[0] for r in cursor.fetchall()]
            
            return Company(**params)
        
        except sqlite3.Error as e:
            print(f"Erro ao buscar company (ID: {companyID}): {e}")
            return None
        except Exception as e:
            print(f"[ERRO] Falha ao construir Company: {e}")
            return None
                
        except sqlite3.Error as e:
            print(f"Erro ao buscar company (ID: {companyID}): {e}")
            return None
    
    def getCompanyByCnpj(self, cnpj: str) -> Optional[Company]:
        """Retorna um objeto Company pelo cnpj, hidratando suas listas de junção."""
        try:
            cursor = self.__db.cursor()
            
            # Buscar pela coluna 'cnpj'
            cursor.execute("SELECT * FROM company WHERE cnpj = ?", (cnpj,))
            row = cursor.fetchone()
            
            if not row: 
                print(f"[AVISO] Nenhuma empresa encontrada com o CNPJ {cnpj}.")
                return None
            
            # CORREÇÃO: Criar dicionário manualmente usando description
            columns = [description[0] for description in cursor.description]
            params = dict(zip(columns, row))
            
            # Extrair o ID da empresa
            company_id = params["id"] 
            
            # --- Hidratação usando o company_id ---
            
            # Buscar directors
            cursor.execute("SELECT personID FROM company_directors WHERE companyID = ?", (company_id,))
            params["directorsIDs"] = [r[0] for r in cursor.fetchall()]  # Usar índice 0
            
            # Buscar RPEs
            cursor.execute("SELECT rpeID FROM company_rpes WHERE companyID = ?", (company_id,))
            params["RPEIDs"] = [r[0] for r in cursor.fetchall()]  # Usar índice 0
            
            # Buscar departments
            cursor.execute("SELECT id FROM department WHERE companyID = ?", (company_id,))
            params["departmentsIDs"] = [r[0] for r in cursor.fetchall()]  # Usar índice 0
            
            return Company(**params)

        except sqlite3.Error as e:
            print(f"Erro ao buscar company (CNPJ: {cnpj}): {e}")
            return None
        except Exception as e:
            print(f"[ERRO] Falha ao construir Company: {e}")
            return None

    def getDepartmentByID(self, departmentID: str) -> Optional[Department]:
        """Retorna um objeto Department pelo ID, hidratando suas listas de junção."""
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM department WHERE id = ?", (departmentID,))
            row = cursor.fetchone()
            if not row: 
                return None
            
            # CORREÇÃO: Criar dicionário manualmente usando description
            columns = [description[0] for description in cursor.description]
            params = dict(zip(columns, row))
            
            # Hidratação 1: 'rpeIds' (N-N)
            cursor.execute("SELECT rpeID FROM department_rpes WHERE departmentID = ?", (departmentID,))
            params["rpeIds"] = [r[0] for r in cursor.fetchall()]  # Usar índice 0

            # Hidratação 2: 'teamsIds' (1-N)
            cursor.execute("SELECT id FROM team WHERE departmentID = ?", (departmentID,))
            params["teamsIds"] = [r[0] for r in cursor.fetchall()]  # Usar índice 0
            
            return Department(**params)
        
        except sqlite3.Error as e:
            print(f"Erro ao buscar department (ID: {departmentID}): {e}")
            return None
        except Exception as e:
            print(f"[ERRO] Falha ao construir Department: {e}")
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
        """Retorna um objeto RPE pelo ID, hidratando 'objectivesIds' pela tabela de junção."""
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM rpe WHERE id = ?", (rpeID,))
            row = cursor.fetchone()
            if not row: 
                return None
            
            # CORREÇÃO: Criar dicionário manualmente usando description
            columns = [description[0] for description in cursor.description]
            params = dict(zip(columns, row))
            
            # Hidratação CORRETA: 'objectivesIds' (N-para-N)
            cursor.execute("SELECT objectiveID FROM rpe_objectives WHERE rpeID = ?", (rpeID,))
            
            # CORREÇÃO: Usar índice 0 em vez de chave de dicionário
            params["objectivesIds"] = [r[0] for r in cursor.fetchall()]
            
            return RPE(**params)
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar RPE (ID: {rpeID}): {e}")
            return None
        except Exception as e:
            print(f"[ERRO] Falha ao construir RPE: {e}")
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
        
    def getRPEsByDepartmentID(self, departmentID: str) -> list[RPE]:
        """
        Retorna uma lista de objetos RPE associados a um departmentID.
        """
        if not departmentID:
            return []
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT rpeID FROM department_rpes WHERE departmentID = ?", (departmentID,))
            rpe_ids = [row["rpeID"] for row in cursor.fetchall()]
            
            rpes = [rpe for rpe in (self.getRPEByID(rid) for rid in rpe_ids) if rpe]
            return rpes
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar RPEs por DepartmentID {departmentID}: {e}")
            return []

    def getRPEsByCompanyID(self, companyID: str) -> list[RPE]:
        """
        Retorna uma lista de objetos RPE associados a um companyID.
        """
        if not companyID:
            return []
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT rpeID FROM company_rpes WHERE companyID = ?", (companyID,))
            rpe_ids = [row["rpeID"] for row in cursor.fetchall()]
            
            rpes = [rpe for rpe in (self.getRPEByID(rid) for rid in rpe_ids) if rpe]
            return rpes
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar RPEs por CompanyID {companyID}: {e}")
            return []

    def getRPEsByObjectiveID(self, objectiveID: str) -> list[RPE]:
        """
        Retorna uma lista de RPEs associados a um objectiveID.
        """
        if not objectiveID:
            return []
        try:
            cursor = self.__db.cursor()
            # 1. Busca IDs de RPE da tabela de junção
            cursor.execute("SELECT rpeID FROM rpe_objectives WHERE objectiveID = ?", (objectiveID,))
            rpe_ids = [row["rpeID"] for row in cursor.fetchall()]
            
            # 2. Reutiliza getRPEByID para construir os objetos
            rpes = [rpe for rpe in (self.getRPEByID(rid) for rid in rpe_ids) if rpe]
            return rpes
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar RPEs por ObjectiveID {objectiveID}: {e}")
            return []

    def getRPEsByKpiID(self, kpiID: str) -> list[RPE]:
        """
        Retorna uma lista de RPEs associados a um kpiID (ou krID), 
        fazendo a busca RPE -> Objective -> KPI.
        """
        if not kpiID:
            return []
        try:
            cursor = self.__db.cursor()
            
            # 1. Busca IDs de RPE usando JOIN de 2 tabelas de junção
            # (Encontra RPEs que têm Objetivos que, por sua vez, têm o KPI)
            query = """
                SELECT DISTINCT T1.rpeID 
                FROM rpe_objectives AS T1
                JOIN objective_kpis AS T2 ON T1.objectiveID = T2.objectiveID
                WHERE T2.kpiID = ?
            """
            cursor.execute(query, (kpiID,))
            rpe_ids = [row["rpeID"] for row in cursor.fetchall()]

            # 2. Reutiliza getRPEByID para construir os objetos
            rpes = [rpe for rpe in (self.getRPEByID(rid) for rid in rpe_ids) if rpe]
            return rpes

        except sqlite3.Error as e:
            print(f"Erro ao buscar RPEs por KpiID {kpiID}: {e}")
            return []
        
    def getRPEsByEntity(self, entity_type: str, entity_id: str) -> list[RPE]:
        """
        Busca RPEs associados a um ID de entidade específico (Team, Department ou Company).

        """
        if not entity_id:
            print("[ALERTA] ID da entidade não fornecido.")
            return []

        if entity_type == "Team":
            return self.getRPEsByTeamID(entity_id) # Esta já existe
        
        elif entity_type == "Department":
            return self.getRPEsByDepartmentID(entity_id) # Esta já existe

        elif entity_type == "Company":
            return self.getRPEsByCompanyID(entity_id) # Esta já existe
            
        else:
            print(f"[ERRO] Tipo de entidade '{entity_type}' não reconhecido.")
            return []

    def getRPEsByTeamID(self, teamID: str) -> list[RPE]:
        """
        Retorna uma lista de objetos RPE associados a um teamID.
        """
        if not teamID:
            return []
        try:
            cursor = self.__db.cursor()
            # 1. Busca todos os IDs de RPE da tabela de junção
            cursor.execute("SELECT rpeID FROM team_rpes WHERE teamID = ?", (teamID,))
            rpe_ids = [row["rpeID"] for row in cursor.fetchall()]
            
            # 2. Reutiliza o getRPEByID para construir cada RPE de forma segura (com hidratação)
            #    Isso é um "list comprehension" que faz um loop e filtra Nones
            rpes = [rpe for rpe in (self.getRPEByID(rid) for rid in rpe_ids) if rpe]
            return rpes
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar RPEs por TeamID {teamID}: {e}")
            return []
        
    def getCompanyByName(self, name: str) -> Optional[Company]:
        """Retorna um objeto Company pelo nome, hidratando suas listas de junção."""
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM company WHERE name = ?", (name,))
            row = cursor.fetchone()
            if not row:
                print(f"[AVISO] Nenhuma empresa encontrada com o nome '{name}'.")
                return None
            
            columns = [description[0] for description in cursor.description]
            params = dict(zip(columns, row))
            company_id = params["id"]
            
            # Hidratação de listas de junção
            cursor.execute("SELECT personID FROM company_directors WHERE companyID = ?", (company_id,))
            params["directorsIDs"] = [r[0] for r in cursor.fetchall()]
            
            cursor.execute("SELECT rpeID FROM company_rpes WHERE companyID = ?", (company_id,))
            params["RPEIDs"] = [r[0] for r in cursor.fetchall()]
            
            cursor.execute("SELECT id FROM department WHERE companyID = ?", (company_id,))
            params["departmentsIDs"] = [r[0] for r in cursor.fetchall()]
            
            return Company(**params)

        except sqlite3.Error as e:
            print(f"[ERRO] Erro SQL ao buscar Company pelo nome '{name}': {e}")
            return None
        except Exception as e:
            print(f"[ERRO] Falha ao construir Company pelo nome '{name}': {e}")
            return None

    def getDepartmentByName(self, name: str) -> Optional[Department]:
        """Retorna um objeto Department pelo nome, hidratando suas listas de junção."""
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM department WHERE name = ?", (name,))
            row = cursor.fetchone()
            if not row:
                print(f"[AVISO] Nenhum departamento encontrado com o nome '{name}'.")
                return None
            
            columns = [description[0] for description in cursor.description]
            params = dict(zip(columns, row))
            departmentID = params["id"]
            
            # Hidratação
            cursor.execute("SELECT rpeID FROM department_rpes WHERE departmentID = ?", (departmentID,))
            params["rpeIds"] = [r[0] for r in cursor.fetchall()]
            
            cursor.execute("SELECT id FROM team WHERE departmentID = ?", (departmentID,))
            params["teamsIds"] = [r[0] for r in cursor.fetchall()]
            
            return Department(**params)

        except sqlite3.Error as e:
            print(f"[ERRO] Erro SQL ao buscar Department pelo nome '{name}': {e}")
            return None
        except Exception as e:
            print(f"[ERRO] Falha ao construir Department pelo nome '{name}': {e}")
            return None

    def getTeamByName(self, name: str) -> Optional[Team]:
        """Retorna um objeto Team pelo nome, hidratando suas listas de junção."""
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM team WHERE name = ?", (name,))
            row = cursor.fetchone()
            if not row:
                print(f"[AVISO] Nenhum time encontrado com o nome '{name}'.")
                return None
            
            columns = [description[0] for description in cursor.description]
            params = dict(zip(columns, row))
            teamID = params["id"]
            
            # Hidratação
            cursor.execute("SELECT personID FROM team_members WHERE teamID = ?", (teamID,))
            params["employeesIDs"] = [r[0] for r in cursor.fetchall()]
            
            cursor.execute("SELECT rpeID FROM team_rpes WHERE teamID = ?", (teamID,))
            params["rpesIDs"] = [r[0] for r in cursor.fetchall()]
            
            return Team(**params)

        except sqlite3.Error as e:
            print(f"[ERRO] Erro SQL ao buscar Team pelo nome '{name}': {e}")
            return None
        except Exception as e:
            print(f"[ERRO] Falha ao construir Team pelo nome '{name}': {e}")
            return None


# --- MÉTODOS DE MUDANÇA DE ESTADO ---

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

# --- MÉTODOS BOOLEAN ---    

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