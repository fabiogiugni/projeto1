import sqlite3
import json
from typing import TYPE_CHECKING,Optional,Union

if TYPE_CHECKING:
    from ..entities.data import Data

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

        self.__db.row_factory = sqlite3.Row
        
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
                departmentID TEXT NULL,
                teamID TEXT NULL,
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
                rpeID TEXT,
                date TEXT,
                FOREIGN KEY(rpeID) REFERENCES rpe(id) ON DELETE CASCADE,
                FOREIGN KEY(responsibleID) REFERENCES person(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS kpi (
                id TEXT PRIMARY KEY,
                description TEXT,
                responsibleID TEXT,
                objectiveID TEXT,
                date TEXT,
                data TEXT,
                goal FLOAT,
                FOREIGN KEY(objectiveID) REFERENCES objective(id) ON DELETE CASCADE,
                FOREIGN KEY(responsibleID) REFERENCES person(id) ON DELETE SET NULL
            );

            --- TABELAS DE JUNÇÃO (Muitos-para-Muitos) ---

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

    #Fazer deleteItemByID
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
    

        """
        Remove referências de um objeto Data (RPE, Objective, KPI, KR)
        das tabelas de junção ANTES de sua exclusão.
        """
        cursor = self.__db.cursor()
        
        try:
            # 1. Limpeza para RPE:
            # RPE está ligado a Company, Department e Team (tabelas de junção antigas que persistem)
            if data_type == "RPE":                
                cursor.execute("DELETE FROM company_rpes WHERE rpeID = ?", (data_id,))
                cursor.execute("DELETE FROM department_rpes WHERE rpeID = ?", (data_id,))
                cursor.execute("DELETE FROM team_rpes WHERE rpeID = ?", (data_id,))
            self.__db.commit()
            
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao limpar relações do {data_type} (ID: {data_id}): {e}")
            self.__db.rollback() 
            raise

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
                        print(f"Person {item.id} inserida com sucesso.")
                        # EXECUTA A QUERY PRINCIPAL AQUI
                        self.__db.execute(query, params)
                        
                        # LÓGICA DE RELACIONAMENTO BASE PARA PERSON
                        # 1. Atribui a Pessoa aos grupos
                        self.assignPersonToCompany(item.id, item.companyID)
                        self.assignPersonToDepartment(item.id, item.departmentID)
                        self.assignPersonToTeam(item.id, item.teamID)
                    else:
                        print(f"[AVISO] Person {item.id} já existe, ignorando inserção.")

                # --- Bloco Company ---
                elif isinstance(item, Company):
                    query = """INSERT INTO company (
                               id, name, cnpj
                               ) VALUES (?, ?, ?)"""
                    params = (item.id, item.name, item.cnpj)
                    # EXECUTA A QUERY PRINCIPAL AQUI
                    self.__db.execute(query, params)
                    
                    # LÓGICA DE RELACIONAMENTO BASE PARA COMPANY
                    # Adiciona os diretores à tabela de junção
                    for director_id in item.directorIds:
                        self.addDirectorToCompany(item.id, director_id)

                # --- Bloco Department ---
                elif isinstance(item, Department):
                    query = """INSERT INTO department (
                               id, name, companyID, directorID
                               ) VALUES (?, ?, ?, ?)"""
                    params = (item.id, item.name, item.companyID, item.directorID)
                    # EXECUTA A QUERY PRINCIPAL AQUI
                    self.__db.execute(query, params)
                    
                    # LÓGICA DE RELACIONAMENTO BASE PARA DEPARTMENT
                    # 1. Adiciona o departamento à lista de departamentos da empresa
                    self.assignDepartmentToCompany(item.id, item.companyID)

                # --- Bloco Team ---
                elif isinstance(item, Team):
                    query = """INSERT INTO team (
                               id, name, departmentID, managerID
                               ) VALUES (?, ?, ?, ?)"""
                    params = (item.id, item.name, item.departmentID, item.managerID)
                    # EXECUTA A QUERY PRINCIPAL AQUI
                    self.__db.execute(query, params)
                    
                    # LÓGICA DE RELACIONAMENTO BASE PARA TEAM
                    # 1. Adiciona o time à lista de times do departamento
                    self.assignTeamToDepartment(item.id, item.departmentID)

                # --- Bloco RPE ---
                elif isinstance(item, RPE):
                    query = """INSERT INTO rpe (
                               id, description, responsibleID, date
                               ) VALUES (?, ?, ?, ?)"""
                    params = (item.id, item.description, item.responsibleID, item.date)
                    self.__db.execute(query, params)
                    self.assignResponsibleToRPE(item.responsibleID, item.id)

                # --- Bloco Objective ---
                elif isinstance(item, Objective):
                    query = """INSERT INTO objective (
                               id, description, responsibleID, rpeID, date
                               ) VALUES (?, ?, ?, ?, ?)"""
                    params = (item.id, item.description, item.responsibleID, item.rpeID, item.date)
                    self.__db.execute(query, params)
                    self.assignResponsibleToObjective(item.responsibleID, item.id)
                    self.assignObjectiveToRPE(item.rpeID, item.id)

                # --- Bloco KPI (usado para KPI e KR, com 'goal' e 'data' opcionais) ---
                elif isinstance(item, KPI):
                    # O campo 'data' (vetor de floats) ainda precisa ser serializado
                    dataText = json.dumps(getattr(item, 'data', [])) 
                    # O campo 'goal' e 'current_value' são tratados. 
                    # Se não existirem no objeto KPI, use NULL (None em Python) ou 0.0
                    goal = getattr(item, 'goal', None)
                    
                    query = """INSERT INTO kpi (
                               id, description, responsibleID, objectiveID, date, data, goal
                               ) VALUES (?, ?, ?, ?, ?, ?, ?)"""
                    params = (item.id, item.description, item.responsibleID, item.objectiveID, item.date, 
                              dataText, goal)
                    self.__db.execute(query, params)
                    self.assignResponsibleToKPI(item.responsibleID, item.id)
                    self.assignKPIToObjective(item.objectiveID, item.id)

                else:
                    print(f"[ERRO] Tipo de item desconhecido para inserção: {entity_name}")
                    return 1

                # Executa a inserção                
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

    # Relações de Department UM-PARA-MUITOS
    def assignDepartmentToCompany(self, department_id: str, company_id: str):
        return self._assign_foreign_key("department", "companyID", company_id, department_id)

    def assignDirectorToDepartment(self, director_id: str, department_id: str):
        return self._assign_foreign_key("department", "directorID", director_id, department_id)

    # Relações de Team UM-PARA-MUITOS
    def assignTeamToDepartment(self, team_id: str, department_id: str):
        return self._assign_foreign_key("team", "departmentID", department_id, team_id)

    def assignManagerToTeam(self, manager_id: str, team_id: str):
        return self._assign_foreign_key("team", "managerID", manager_id, team_id)

    # Relações de Person UM-PARA-MUITOS
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

    # Relações de RPE UM-PARA-MUITOS
    def assignResponsibleToRPE(self, responsible_id: str, rpe_id: str):
        return self._assign_foreign_key("rpe", "responsibleID", responsible_id, rpe_id)

    #Relações de Objective UM-PARA-MUITOS
    def assignResponsibleToObjective(self, responsible_id: str, objective_id: str):
        return self._assign_foreign_key("objective", "responsibleID", responsible_id, objective_id)
    
    def unassignResponsibleToObjective(self, objective_id: str):
        return self._unassign_foreign_key("objective", "responsibleID", objective_id)
    
    def assignObjectiveToRPE(self, rpe_id: str, objective_id: str):
        return self._assign_foreign_key("objective", "rpeID", rpe_id, objective_id)
    
    def unassignObjectiveToRPE(self, objective_id: str):
        return self._unassign_foreign_key("objective", "rpeID", objective_id)

    # Relações de KPI UM-PARA-MUITOS
    def assignResponsibleToKPI(self, responsible_id: str, kpi_id: str):
        return self._assign_foreign_key("kpi", "responsibleID", responsible_id, kpi_id)
    
    def unassignResponsibleToKPI(self, kpi_id: str):
        return self._unassign_foreign_key("kpi", "responsibleID", kpi_id)
    
    def assignKPIToObjective(self, objective_id: str, kpi_id: str):
        return self._assign_foreign_key("kpi", "objectiveID", objective_id, kpi_id)
    
    def unassignKPIToObjective(self, kpi_id: str):
        return self._unassign_foreign_key("kpi", "objectiveID", kpi_id)

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
    
    # department_rpes (Company <-> RPE)
    def addRpeToDepartment(self, department_id: str, rpe_id: str) -> bool:
        return self._add_junction("department_rpes", "departmentID", department_id, "rpeID", rpe_id)

    def deleteRpeFromDepartment(self, department_id: str, rpe_id: str) -> bool:
        return self._delete_junction("department_rpes", "departmentID", department_id, "rpeID", rpe_id)
    
    # team_rpes (Company <-> RPE)
    def addRpeToTeam(self, team_id: str, rpe_id: str) -> bool:
        return self._add_junction("team_rpes", "teamID", team_id, "rpeID", rpe_id)

    def deleteRpeFromTeam(self, team_id: str, rpe_id: str) -> bool:
        return self._delete_junction("team_rpes", "teamID", team_id, "rpeID", rpe_id)
        
    def updateItem(self, item: Entity) -> int:
        """
        Atualiza os campos diretos de um item no banco de dados.
        Agora também atualiza as relações rpeIds para Team, Department e Company.
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
                        SET description = ?, responsibleID = ?, rpeID = ?, date = ?
                        WHERE id = ?"""
                params = (item.description, item.responsibleID, item.rpeID, item.date, item.id)

            # --- Bloco KR ---
            elif isinstance(item, KR):
                dataText = json.dumps(item.data) 
                query = """UPDATE kpi
                        SET description = ?, responsibleID = ?, objectiveID = ?, date = ?, data = ?, goal = ?
                        WHERE id = ?"""
                params = (item.description, item.responsibleID, item.objectiveID, item.date, dataText, item.goal,
                        item.id)

            # --- Bloco KPI ---
            elif isinstance(item, KPI):
                dataText = json.dumps(item.data) 
                query = """UPDATE kpi
                        SET description = ?, responsibleID = ?, objectiveID = ?, date = ?, data = ?, goal = ?
                        WHERE id = ?"""
                params = (item.description, item.responsibleID, item.objectiveID, item.date, dataText, None,
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
                
                # --- ATUALIZAÇÃO DOS rpeIds PARA TEAM, DEPARTMENT E COMPANY ---
                
                # Team RPEs
                if isinstance(item, Team) and hasattr(item, 'rpeIds'):
                    # Primeiro remove todos os RPEs existentes
                    self.__db.execute("DELETE FROM team_rpes WHERE teamID = ?", (item.id,))
                    # Depois insere os novos RPEs
                    for rpe_id in item.rpeIds:
                        self.__db.execute(
                            "INSERT INTO team_rpes (teamID, rpeID) VALUES (?, ?)",
                            (item.id, rpe_id)
                        )
                    print(f"rpeIds do Team {item.id} atualizados: {item.rpeIds}")
                
                # Department RPEs
                elif isinstance(item, Department) and hasattr(item, 'rpeIds'):
                    # Remove todos os RPEs existentes
                    self.__db.execute("DELETE FROM department_rpes WHERE departmentID = ?", (item.id,))
                    # Insere os novos RPEs
                    for rpe_id in item.rpeIds:
                        self.__db.execute(
                            "INSERT INTO department_rpes (departmentID, rpeID) VALUES (?, ?)",
                            (item.id, rpe_id)
                        )
                    print(f"rpeIds do Department {item.id} atualizados: {item.rpeIds}")
                
                # Company RPEs
                elif isinstance(item, Company) and hasattr(item, 'rpeIds'):
                    # Remove todos os RPEs existentes
                    self.__db.execute("DELETE FROM company_rpes WHERE companyID = ?", (item.id,))
                    # Insere os novos RPEs
                    for rpe_id in item.rpeIds:
                        self.__db.execute(
                            "INSERT INTO company_rpes (companyID, rpeID) VALUES (?, ?)",
                            (item.id, rpe_id)
                        )
                    print(f"rpeIds da Company {item.id} atualizados: {item.rpeIds}")
                
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
        
        columns = [col[0] for col in cursor.description]
        params = dict(zip(columns, row))
        personID = params["id"]
        role = params.get("role")
        
        # Hidratação: Busca IDs de responsabilidade se for Manager ou Director
        responsibleIds = []
        if role in ("Manager", "Director"):
            cursor.execute("SELECT responsibleID FROM person_responsibles WHERE personID = ?", (personID,))
            id_rows = cursor.fetchall()
            responsibleIds = [r["responsibleID"] for r in id_rows]
        
        # Remove kwargs que não existem nos construtores
        params.pop("role", None)
        if "responsibleIds" in params:
            params.pop("responsibleIds")

        # Factory: Constrói o objeto da classe correta
        try:
            if role == "Manager":
                obj = Manager(responsibleIds=responsibleIds, **params)
            elif role == "Director":
                obj = Director(responsibleIds=responsibleIds, **params)
            else:
                obj = Person(**params)
            return obj
        except TypeError as e:
            print(f"[ERRO] Falha ao construir objeto Person/Manager/Director. Verifique os construtores.")
            print(f"   Erro: {e}")
            print(f"   Parâmetros: {params}")
            return None

# --- MÉTODOS DE BUSCA "GET" ---

    def _get_single(self, table: str, field: str, value: str, cls):
        try:
            cursor = self.__db.cursor()

            query = f"SELECT * FROM {table} WHERE {field} = ? LIMIT 1;"
            cursor.execute(query, (value,))
            row = cursor.fetchone()

            if not row:
                return None

            # Caso row_factory não esteja setado, converte manualmente
            if not isinstance(row, sqlite3.Row):
                columns = [desc[0] for desc in cursor.description]
                row = {columns[i]: row[i] for i in range(len(columns))}

            # Cria o objeto dinamicamente
            return cls(**row)

        except sqlite3.Error as e:
            print(f"[ERRO] Falha no get genérico para {table}: {e}")
            return None
        
    def _get_single_raw(self, table: str, field: str, value: str):
        try:
            cursor = self.__db.cursor()

            query = f"SELECT * FROM {table} WHERE {field} = ? LIMIT 1;"
            cursor.execute(query, (value,))
            row = cursor.fetchone()

            if not row:
                return None

            columns = [desc[0] for desc in cursor.description]
            return {columns[i]: row[i] for i in range(len(columns))}

        except sqlite3.Error as e:
            print(f"[ERRO] Falha no get genérico para {table}: {e}")
            return None

    def _get_many(self, table: str, field: str, value: str, cls):
        try:
            cursor = self.__db.cursor()
            query = f"SELECT * FROM {table} WHERE {field} = ?;"
            cursor.execute(query, (value,))
            rows = cursor.fetchall()

            results = []
            for row in rows:
                if not isinstance(row, sqlite3.Row):
                    columns = [desc[0] for desc in cursor.description]
                    row = {columns[i]: row[i] for i in range(len(columns))}
                results.append(cls(**row))

            return results

        except sqlite3.Error as e:
            print(f"[ERRO] Falha no get many para {table}: {e}")
            return []
    
    def _hydrateOneToMany(self, parent_id: str, join_table: str, parent_fk: str, child_fk: str) -> list[str]:
        """
        Busca IDs relacionados em uma tabela de junção.
        """
        try:
            cursor = self.__db.cursor()
            query = f"SELECT {child_fk} FROM {join_table} WHERE {parent_fk} = ?;"
            cursor.execute(query, (parent_id,))
            return [row[0] for row in cursor.fetchall()]
        except:
            return []

    def _hydrateCompany(self, company:Company):
        cid = company.id
        company.directorIds = self._hydrateOneToMany(cid, "company_directors", "companyID", "personID")
        company.rpeIds       = self._hydrateOneToMany(cid, "company_rpes", "companyID", "rpeID")
        company.departmentIds = self._hydrateOneToMany(cid, "department", "companyID", "id")
        return company

    def _hydrateDepartment(self, department: Department):
        did = department.id
        department.teamIds = self._hydrateOneToMany(did, "team", "departmentID", "id")
        department.rpeIds   = self._hydrateOneToMany(did, "department_rpes", "departmentID", "rpeID")
        return department

    def _hydrateTeam(self, team: Team):
        tid = team.id
        cursor = self.__db.cursor()
        cursor.execute("SELECT id FROM person WHERE teamID = ?", (tid,))
        team.employeeIDs = [row[0] for row in cursor.fetchall()]  # Nome correto
        
        team.rpeIds = self._hydrateOneToMany(tid, "team_rpes", "teamID", "rpeID")
        return team
        
    def _getRPEsFromRelation(self, relation_table: str, column: str, value: str) -> list[RPE]:
        if not value:
            return []
        try:
            cursor = self.__db.cursor()
            query = f"SELECT rpeID FROM {relation_table} WHERE {column} = ?"
            cursor.execute(query, (value,))

            rpe_ids = [row["rpeID"] for row in cursor.fetchall()]
            return [rpe for rpe in (self.getRPEByID(rid) for rid in rpe_ids) if rpe]

        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao buscar RPEs na relação {relation_table}.{column}={value}: {e}")
            return []
        
    def getResponsibleIDs(self, personID: str) -> list[str]:
        cursor = self.__db.cursor()
        cursor.execute("""
            SELECT responsibleID FROM person_responsibles WHERE personID = ?
        """, (personID,))
        return [row[0] for row in cursor.fetchall()]

    def getMeasureByID(self, measureID: str) -> Optional[Union[KPI, KR]]:
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM kpi WHERE id = ?", (measureID,))
            row = cursor.fetchone()
            if not row:
                return None

            params = dict(zip([c[0] for c in cursor.description], row))
            params["data"] = json.loads(params["data"]) if params.get("data") else []

            # Se goal é None → KPI
            if params.get("goal") is None:
                params.pop("goal", None)
                return KPI(**params)

            # Se goal tem valor → KR
            return KR(**params)

        except Exception as e:
            print(f"[ERRO] Falha ao buscar Measure (ID: {measureID}): {e}")
            return None

    def getPersonByID(self, personID: str):
        data = self._get_single_raw("person", "id", personID)
        if data is None:
            return None

        role = data.get("role", "Employee")

        # Hidratar Manager/Director (responsibleIDs)
        if role == "Manager":
            resp = self.getResponsibleIDs(personID)
            return Manager(responsibleIds=resp, **data)

        elif role == "Director":
            resp = self.getResponsibleIDs(personID)
            return Director(responsibleIds=resp, **data)

        return Person(**data)

    def getPersonByEmail(self, email: str) -> Optional[Person]:
        data = self._get_single_raw("person", "email", email)
        if data is None:
            return None

        role = data.get("role", "Employee")
        personID = data["id"]

        # Hidratar Manager/Director (responsibleIDs)
        if role == "Manager":
            resp = self.getResponsibleIDs(personID)
            return Manager(responsibleIds=resp, **data)

        elif role == "Director":
            resp = self.getResponsibleIDs(personID)
            return Director(responsibleIds=resp, **data)

        return Person(**data)

    def getCompanyByID(self, companyID: str) -> Optional[Company]:
        company = self._get_single("company", "id", companyID, Company)
        return self._hydrateCompany(company) if company else None

    def getCompanyByCnpj(self, cnpj: str) -> Optional[Company]:
        company = self._get_single("company", "cnpj", cnpj, Company)
        return self._hydrateCompany(company) if company else None   
    
    def getCompanyByName(self, name: str):
        company = self._get_single("company", "name", name, Company)
        return self._hydrateCompany(company) if company else None  

    def getDepartmentByID(self, departmentID: str) -> Optional[Department]:
        department = self._get_single("department", "id", departmentID, Department)
        return self._hydrateDepartment(department) if department else None

    def getDepartmentByName(self, name: str) -> Optional[Department]:
        department = self._get_single("department", "name", name, Department)
        return self._hydrateDepartment(department) if department else None  

    def getTeamByID(self, teamID: str) -> Optional[Team]:
        team = self._get_single("team", "id", teamID, Team)
        return self._hydrateTeam(team) if team else None

    def getTeamByName(self, name: str) -> Optional[Team]:
        team = self._get_single("team", "name", name, Team)
        return self._hydrateTeam(team) if team else None

    def getRPEByID(self, rpeID: str) -> Optional[RPE]:
        return self._get_single("rpe", "id", rpeID, RPE)
    
    def getRPEsByCompanyID(self, companyID) -> list[RPE]:
        return self._getRPEsFromRelation("company_rpes", "companyID", companyID)

    def getRPEsByDepartmentID(self, departmentID: str) -> list[RPE]:
        return self._getRPEsFromRelation("department_rpes", "departmentID", departmentID)

    def getRPEsByTeamID(self, teamID: str) -> list[RPE]:
        return self._getRPEsFromRelation("team_rpes", "teamID", teamID)

    def getObjectiveByID(self, objectiveID: str) -> Optional[Objective]:
        return self._get_single("objective", "id", objectiveID, Objective)
    
    def getObjectivesByRPE(self, rpeID: str) -> list[str]:
        cursor = self.__db.cursor()
        cursor.execute("SELECT id FROM objective WHERE rpeID = ?", (rpeID,))
        return [row[0] for row in cursor.fetchall()]

    def getKPIByID(self, kpiID: str) -> Optional[KPI]:
        result = self.getMeasureByID(kpiID)
        return result if isinstance(result, KPI) else None

    def getKPIsByObjective(self, objectiveID: str) -> list[str]:
        cursor = self.__db.cursor()
        cursor.execute("SELECT id FROM kpi WHERE objectiveID = ? AND goal IS NULL", (objectiveID,))
        return [row[0] for row in cursor.fetchall()]

    def getKRByID(self, krID: str) -> Optional[KR]:
        result = self.getMeasureByID(krID)
        return result if isinstance(result, KR) else None

    def getKRsByObjective(self, objectiveID: str) -> list[str]:
        cursor = self.__db.cursor()
        cursor.execute("SELECT id FROM kpi WHERE objectiveID = ? AND goal IS NOT NULL", (objectiveID,))
        return [row[0] for row in cursor.fetchall()]
    
    def getDataByEntity(self, group_type: str, group_id: str, data_type: str):
        """
        Retorna dados (RPE / Objective / KPI / KR) associados a Company, Department ou Team.
        """

        # --- 1) RPE ---
        if data_type == "RPE":
            match group_type:
                case "Company":
                    return self.getRPEsByCompanyID(group_id)
                case "Department":
                    return self.getRPEsByDepartmentID(group_id)
                case "Team":
                    return self.getRPEsByTeamID(group_id)
            return []

        # --- 2) Objective ---
        if data_type == "Objective":
            rpes = self.getDataByEntity(group_type, group_id, "RPE")
            objectives = []
            for rpe in rpes:
                objectives.extend(self.getObjectivesByRPE(rpe.id))
            return [self.getObjectiveByID(oid) for oid in objectives]

        # --- 3) KPI ---
        if data_type == "KPI":
            objectives = self.getDataByEntity(group_type, group_id, "Objective")
            kpis = []
            for obj in objectives:
                for kpiID in self.getKPIsByObjective(obj.id):
                    kpis.append(self.getKPIByID(kpiID))
            return kpis

        # --- 4) KR ---
        if data_type == "KR":
            objectives = self.getDataByEntity(group_type, group_id, "Objective")
            krs = []
            for obj in objectives:
                for krID in self.getKRsByObjective(obj.id):
                    krs.append(self.getKRByID(krID))
            return krs

        return []
    
    def getTeams(self) -> list[Team]:
        cursor = self.__db.cursor()
        cursor.execute("SELECT * FROM team ")
        rows = cursor.fetchall()

        teams = []
        for row in rows:
            if not isinstance(row, sqlite3.Row):
                columns = [desc[0] for desc in cursor.description]
                row = {columns[i]: row[i] for i in range(len(columns))}
                team = Team(**row)
            else:
                team = Team(**row)

            # Hidratar (employeeIDs, rpeIds)
            teams.append(self._hydrateTeam(team))
        
        return teams

    def getDepartmentsByCompanyID(self, companyID: str ) -> list[Department]:
        """
        Retorna todos os departamentos pertencentes a uma empresa.
        """

        print(companyID)
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM department WHERE companyID = ?", (companyID,))
            rows = cursor.fetchall()
            print(rows)
            departments = []
            for row in rows:
                # Convert Row → dict caso necessário
                if not isinstance(row, sqlite3.Row):
                    columns = [desc[0] for desc in cursor.description]
                    row = {columns[i]: row[i] for i in range(len(columns))}
                    dept = Department(**row)
                else:
                    dept = Department(**row)

                # Hidratar relações (teamIds, rpeIds)
                departments.append(self._hydrateDepartment(dept))
            
            return departments

        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao buscar departamentos da empresa {companyID}: {e}")
            return []

    def getTeamsByDepartmentID(self, departmentID: str) -> list[Team]:
        """
        Retorna todos os times pertencentes a um departamento.
        """
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM team WHERE departmentID = ?", (departmentID,))
            rows = cursor.fetchall()

            teams = []
            for row in rows:
                if not isinstance(row, sqlite3.Row):
                    columns = [desc[0] for desc in cursor.description]
                    row = {columns[i]: row[i] for i in range(len(columns))}
                    team = Team(**row)
                else:
                    team = Team(**row)

                # Hidratar (employeeIDs, rpeIds)
                teams.append(self._hydrateTeam(team))
            
            return teams

        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao buscar times do departamento {departmentID}: {e}")
            return []

    def getPersonsByTeamID(self, teamID: str) -> list[Person]:
        """
        Retorna todos os usuários que pertencem a um time.
        """
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT id FROM person WHERE teamID = ?", (teamID,))
            rows = cursor.fetchall()

            persons = []
            for row in rows:
                # row[0] contém o id da pessoa
                person = self.getPersonByID(row[0])
                if person:
                    persons.append(person)

            return persons

        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao buscar pessoas do time {teamID}: {e}")
            return []
        
    def getPersonsByDepartmentID(self, departmentID: str) -> list[Person]:
        """
        Retorna todas as pessoas que pertencem diretamente a um departamento
        (independente de terem time atribuído ou não).
        """
        try:
            cursor = self.__db.cursor()
            cursor.execute("""
                SELECT id FROM person 
                WHERE departmentID = ?
            """, (departmentID,))
            rows = cursor.fetchall()

            persons = []
            for row in rows:
                person = self.getPersonByID(row[0])  # Hidrata Manager/Director corretamente
                if person:
                    persons.append(person)

            return persons

        except Exception as e:
            print(f"[ERRO] Falha ao buscar pessoas do departamento {departmentID}: {e}")
            return []

    def getPersonsByCompanyID(self, companyID: str) -> list[Person]:
        """
        Retorna todas as pessoas que pertencem diretamente à empresa,
        independente de departamento ou time.
        """
        try:
            cursor = self.__db.cursor()
            cursor.execute("""
                SELECT id FROM person 
                WHERE companyID = ?
            """, (companyID,))
            rows = cursor.fetchall()

            persons = []
            for row in rows:
                person = self.getPersonByID(row[0])  # Hidrata Manager/Director corretamente
                if person:
                    persons.append(person)

            return persons

        except Exception as e:
            print(f"[ERRO] Falha ao buscar pessoas da empresa {companyID}: {e}")
            return []

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
        Verifica se um Objective é Team-level ou Department-level,
        verificando se o seu RPE associado está ligado a um Team ou Department.
        """
        try:
            cursor = self.__db.cursor()

            # 1) Descobre o rpeID do Objective
            cursor.execute("SELECT rpeID FROM objective WHERE id = ?", (objectiveID,))
            row = cursor.fetchone()

            if not row:
                # Se não existir RPE associado, não é Team/Department
                return False

            rpeID = row[0]

            # 2) Reutiliza o método **correto** já existente
            return self.isRPETeamOrDepartmentLevel(rpeID)

        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao verificar nível do Objective {objectiveID}: {e}")
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