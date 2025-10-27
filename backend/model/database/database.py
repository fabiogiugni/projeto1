import sqlite3
import pandas as pd
import json
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

    def __init__(self):
        
        self.__db = sqlite3.connect('database/database.db')

        self.__db.executescript('''
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
                responsibleIds TEXT
                )
            CREATE TABLE IF NOT EXISTS company (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                rpeIds TEXT,
                cnpj TEXT UNIQUE,
                departmentsIds TEXT,
                directorsIds TEXT
                )
            CREATE TABLE IF NOT EXISTS department (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                rpeIds TEXT,
                directorID TEXT,
                teamsIds TEXT
                )
            CREATE TABLE IF NOT EXISTS team (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                rpeIds TEXT,
                managerID TEXT,
                employeeIds TEXT
                )
            CREATE TABLE IF NOT EXISTS rpe (
                id TEXT PRIMARY KEY,
                description TEXT,
                responsibleID TEXT,
                date TEXT,
                objectivesIds TEXT
                )
            CREATE TABLE IF NOT EXISTS objective (
                id TEXT PRIMARY KEY,
                description TEXT,
                responsibleID TEXT,
                date TEXT,
                krIds TEXT,
                kpiIds TEXT
                )
            CREATE TABLE IF NOT EXISTS kpi (
                id TEXT PRIMARY KEY,
                description TEXT,
                responsibleID TEXT,
                date TEXT,
                data TEXT,
                goal FLOAT
                )
            ''')
        self.__saveData()

    def __saveData(self):
        """Salva as alterações pendentes."""
        self.__db.commit()

    def addItem(self, item: Entity):
        if isinstance(item, Person):
            
            if(item.role == "Director" or item.role == "Manager"):
                # --- Serializa a lista de IDs para texto (JSON) ---
                responsibleIdsText = json.dumps(item.responsibleIds)
            else:
                responsibleIdsText = json.dumps([])

            try:
                # Usando '?' para evitar SQL Injection
                self.__db.execute(
                    "INSERT INTO person (id, name, cpf, companyID, departmentID, teamID, role, email, password, responsibleIds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        item.id, 
                        item.name, 
                        item.cpf,
                        item.companyID,
                        item.departmentID,
                        item.teamID,
                        item.role,
                        item.email,
                        item.password,
                        responsibleIdsText)
                )
                self.__saveData()
                print(f"Pessoa {item.name} adicionada.")
            
            except sqlite3.IntegrityError as e:
                print(f"Erro ao adicionar pessoa (ID ou Email já existe?): {e}")

        elif isinstance(item, Company):
            
            # --- Serializa a lista de IDs para texto (JSON) ---
            rpeIdsText = json.dumps(item.rpeIds)
            departmentsIdsText = json.dumps(item.departmentsIds)
            directorsIdsText = json.dumps(item.directorsIds)

            try:
                # Usando '?' para evitar SQL Injection
                self.__db.execute(
                    "INSERT INTO company (id, name, rpeIds, cnpj, departmentsIds, directorsIds) VALUES (?, ?, ?, ?, ?, ?)", (
                        item.id, 
                        item.name, 
                        rpeIdsText,
                        item.cnpj,
                        departmentsIdsText,
                        directorsIdsText)
                )
                self.__saveData()
                print(f"Company {item.name} adicionada.")
            
            except sqlite3.IntegrityError as e:
                print(f"Erro ao adicionar Company (ID ou CNPJ já existe?): {e}")
        
        elif isinstance(item, Department):
            
            # --- Serializa a lista de IDs para texto (JSON) ---
            rpeIdsText = json.dumps(item.rpeIds)
            teamsIdsText = json.dumps(item.directorsIds)

            try:
                # Usando '?' para evitar SQL Injection
                self.__db.execute(
                    "INSERT INTO department (id, name, rpeIds, directorID, teamsIds) VALUES (?, ?, ?, ?, ?)", (
                        item.id, 
                        item.name, 
                        rpeIdsText,
                        item.directorID,
                        teamsIdsText)
                )
                self.__saveData()
                print(f"Department {item.name} adicionado.")
            
            except sqlite3.IntegrityError as e:
                print(f"Erro ao adicionar Department (ID ou DirectorID já existe?): {e}")
        
        elif isinstance(item, Team):
            
            # --- Serializa a lista de IDs para texto (JSON) ---
            rpeIdsText = json.dumps(item.rpeIds)
            employeeIdsText = json.dumps(item.directorsIds)

            try:
                # Usando '?' para evitar SQL Injection
                self.__db.execute(
                    "INSERT INTO team (id, name, rpeIds, managerID, employeeIds) VALUES (?, ?, ?, ?, ?)", (
                        item.id, 
                        item.name, 
                        rpeIdsText,
                        item.managerID,
                        employeeIdsText)
                )
                self.__saveData()
                print(f"Team {item.name} adicionado.")
            
            except sqlite3.IntegrityError as e:
                print(f"Erro ao adicionar Team (ID ou ManagerID já existe?): {e}")

        elif isinstance(item, RPE):

             # --- Serializa a lista de IDs para texto (JSON) ---
            objectivesIdsText = json.dumps(item.objectivesIds)

            try:
                self.__db.execute(
                    "INSERT INTO rpe (id, description, responsibleID, objectivesIds) VALUES (?, ?, ?, ?)", (
                        item.id,
                        item.description,
                        item.responsibleID,
                        item.date,
                        objectivesIdsText
                    )
                )
                self.__saveData()
                print(f"RPE {item.id} adicionado.")
            except sqlite3.IntegrityError as e:
                print(f"Erro ao adicionar RPE (ID já existe?): {e}")

        elif isinstance(item, Objective):

             # --- Serializa a lista de IDs para texto (JSON) ---
            krIdsText = json.dumps(item.krIds)
            kpiIdsText = json.dumps(item.kpiIds)

            try:
                self.__db.execute(
                    "INSERT INTO objective (id, description, responsibleID, krIds, kpiIds) VALUES (?, ?, ?, ?, ?)", (
                        item.id,
                        item.description,
                        item.responsibleID,
                        item.date,
                        krIdsText,
                        kpiIdsText
                    )
                )
                self.__saveData()
                print(f"Objective {item.id} adicionado.")
            except sqlite3.IntegrityError as e:
                print(f"Erro ao adicionar Objective (ID já existe?): {e}")

        elif isinstance(item, KPI):

            # Serializa o "vetor de floats" para JSON/TEXT
            dataText = json.dumps(item.data)

            try:
                self.__db.execute(
                    "INSERT INTO kpi (id, description, responsibleID, data, goal) VALUES (?, ?, ?, ?, ?)", (
                        item.id,
                        item.description,
                        item.responsibleID,
                        item.date,
                        dataText, # Salva o vetor como texto
                        item.goal
                    )
                )
                self.__saveData()
                print(f"KPI {item.id} adicionado.")

            except sqlite3.IntegrityError as e:
                print(f"Erro ao adicionar KPI (ID já existe?): {e}")

        elif isinstance(item, KR):

            # Serializa o "vetor de floats" para JSON/TEXT
            dataText = json.dumps(item.data)

            try:
                self.__db.execute(
                    "INSERT INTO kpi (id, description, responsibleID, data, goal) VALUES (?, ?, ?, ?, ?)", (
                        item.id,
                        item.description,
                        item.responsibleID,
                        dataText, # Salva o vetor como texto
                        -1
                    )
                )
                self.__saveData()
                print(f"KR {item.id} adicionado.")

            except sqlite3.IntegrityError as e:
                print(f"Erro ao adicionar KPI (ID já existe?): {e}")

        else:
            print(f"[ERRO] Tipo de item desconhecido: {type(item)}")
            return 1
        
        return 0
    
    def addTeamMember(self, personID: str, teamId: str):
        """
        Adiciona uma pessoa a um time.
        Isso atualiza DUAS tabelas: 'person' (seta teamID) e 'team' (adiciona a employeeIds).
        Usa uma transação para garantir que ambas as atualizações ocorram ou nenhuma ocorra.
        """
        try:
            # 'with self.__db:' inicia uma transação (COMMIT ou ROLLBACK automático)
            with self.__db:
                cursor = self.__db.cursor()

                # --- Etapa 1: Atualizar a tabela 'person' ---
                # Define o teamID da pessoa
                cursor.execute("UPDATE person SET teamID = ? WHERE id = ?", (teamId, personID))
                
                if cursor.rowcount == 0:
                    raise Exception(f"Pessoa com ID {personID} não encontrada.")

                # --- Etapa 2: Atualizar a tabela 'team' ---
                # 2a. Obter a lista atual de 'employeeIds'
                cursor.execute("SELECT employeeIds FROM team WHERE id = ?", (teamId,))
                row = cursor.fetchone()

                if row is None:
                    raise Exception(f"Time com ID {teamId} não encontrado.")

                currentIdsStr = row[0]
                
                # 2b. Manipular a lista em Python
                if currentIdsStr:
                    id_list = currentIdsStr.split(',')
                else:
                    id_list = []

                # 2c. Adicionar o novo ID se ainda não estiver na lista
                if personID not in id_list:
                    id_list.append(personID)
                    newIdsStr = ",".join(id_list)
                    
                    # 2d. Salvar a nova lista de volta no banco
                    cursor.execute("UPDATE team SET employeeIds = ? WHERE id = ?", (newIdsStr, teamId))
            
            print(f"Membro {personID} adicionado ao time {teamId} com sucesso.")
            return True
        
        except sqlite3.Error as e:
            print(f"Erro de Banco de Dados ao adicionar membro: {e}")
            return False
        except Exception as e:
            print(f"Erro: {e}") # Imprime "Pessoa não encontrada" ou "Time não encontrado"
            return False

    def updateItem(self, item: Entity): 
        """Atualiza um item existente no banco de dados, baseado no seu tipo."""
        
        # --- Bloco Person ---
        if isinstance(item, Person):

            if(item.role == "Director" or item.role == "Manager"):
                # --- Serializa a lista de IDs para texto (JSON) ---
                responsibleIdsText = json.dumps(item.responsibleIds)
            else:
                responsibleIdsText = json.dumps([])

            try:
                self.__db.execute(
                    """UPDATE person 
                       SET name = ?, cpf = ?, companyID = ?, departmentID = ?, teamID = ?, 
                           role = ?, email = ?, password = ?, responsibleIds = ?
                       WHERE id = ?""", 
                    (item.name, item.cpf, item.companyID, item.departmentID, item.teamID,
                     item.role, item.email, item.password, responsibleIdsText, 
                     item.id) # O ID é o último, para a cláusula WHERE
                )
                self.__saveData()
                print(f"Pessoa {item.name} (ID: {item.id}) atualizada.")
            except sqlite3.Error as e:
                print(f"Erro ao atualizar Pessoa (ID: {item.id}): {e}")

        # --- Bloco Company ---
        elif isinstance(item, Company):
            rpeIdsText = json.dumps(item.rpeIds)
            departmentsIdsText = json.dumps(item.departmentsIds)
            directorsIdsText = json.dumps(item.directorsIds)
            try:
                self.__db.execute(
                    """UPDATE company
                       SET name = ?, rpeIds = ?, cnpj = ?, departmentsIds = ?, directorsIds = ?
                       WHERE id = ?""",
                    (item.name, rpeIdsText, item.cnpj, departmentsIdsText, directorsIdsText,
                     item.id) # ID no final
                )
                self.__saveData()
                print(f"Company {item.name} (ID: {item.id}) atualizada.")
            except sqlite3.Error as e:
                print(f"Erro ao atualizar Company (ID: {item.id}): {e}")
        
        # --- Bloco Department ---
        elif isinstance(item, Department):
            rpeIdsText = json.dumps(item.rpeIds)
            teamsIdsText = json.dumps(item.teamsIds)
            try:
                self.__db.execute(
                    """UPDATE department
                       SET name = ?, rpeIds = ?, directorId = ?, teamsIds = ?
                       WHERE id = ?""",
                    (item.name, rpeIdsText, item.directorId, teamsIdsText,
                     item.id) # ID no final
                )
                self.__saveData()
                print(f"Department {item.name} (ID: {item.id}) atualizado.")
            except sqlite3.Error as e:
                print(f"Erro ao atualizar Department (ID: {item.id}): {e}")
        
        # --- Bloco Team ---
        elif isinstance(item, Team):
            rpeIdsText = json.dumps(item.rpeIds)
            employeeIdsText = json.dumps(item.employeeIds)
            try:
                self.__db.execute(
                    """UPDATE team
                       SET name = ?, rpeIds = ?, managerId = ?, employeeIds = ?
                       WHERE id = ?""",
                    (item.name, rpeIdsText, item.managerId, employeeIdsText,
                     item.id) # ID no final
                )
                self.__saveData()
                print(f"Team {item.name} (ID: {item.id}) atualizado.")
            except sqlite3.Error as e:
                print(f"Erro ao atualizar Team (ID: {item.id}): {e}")

        # --- Bloco RPE ---
        elif isinstance(item, RPE):
            objectivesIdsText = json.dumps(item.objectivesIds)
            try:
                self.__db.execute(
                    """UPDATE rpe
                       SET description = ?, responsibleID = ?, date = ?, objectivesIds = ?
                       WHERE id = ?""",
                    (item.description, item.responsibleID, item.date, objectivesIdsText,
                     item.id) # ID no final
                )
                self.__saveData()
                print(f"RPE (ID: {item.id}) atualizado.")
            except sqlite3.Error as e:
                print(f"Erro ao atualizar RPE (ID: {item.id}): {e}")

        # --- Bloco Objective ---
        elif isinstance(item, Objective):
            krIdsText = json.dumps(item.krIds)
            kpiIdsText = json.dumps(item.kpiIds)
            try:
                self.__db.execute(
                    """UPDATE objective
                       SET description = ?, responsibleID = ?, date = ?, krIds = ?, kpiIds = ?
                       WHERE id = ?""",
                    (item.description, item.responsibleID, item.date, krIdsText, kpiIdsText,
                     item.id) # ID no final
                )
                self.__saveData()
                print(f"Objective (ID: {item.id}) atualizado.")
            except sqlite3.Error as e:
                print(f"Erro ao atualizar Objective (ID: {item.id}): {e}")

        # --- Bloco KPI ---
        elif isinstance(item, KPI):
            dataText = json.dumps(item.data) # Serializa o vetor de floats
            try:
                self.__db.execute(
                    """UPDATE kpi
                       SET description = ?, responsibleID = ?,date = ?, data = ?, goal = ?
                       WHERE id = ?""",
                    (item.description, item.responsibleID, item.date, dataText, item.goal,
                     item.id) # ID no final
                )
                self.__saveData()
                print(f"KPI (ID: {item.id}) atualizado.")
            except sqlite3.Error as e:
                print(f"Erro ao atualizar KPI (ID: {item.id}): {e}")
                return 1
        # --- Bloco Else ---
        else:
            print(f"[ERRO] Tipo de item desconhecido para atualização: {type(item)}")
            return 1
        return 0

    def deleteItem(self, item: Entity):
        """Remove um item do banco de dados, de acordo com o tipo da entidade."""
        
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
            return

        try:
            # Usamos f-string de forma segura pois tableName é controlado internamente
            query = f"DELETE FROM {tableName} WHERE id = ?"
            cursor = self.__db.execute(query, (item.id,))
            self.__saveData()

            if cursor.rowcount == 0:
                print(f"[AVISO] Nenhum registro encontrado em '{tableName}' com o ID {item.id}.")
                return 1
            else:
                print(f"Item de '{tableName}' com ID {item.id} removido com sucesso.")
        
        except sqlite3.Error as e:
            print(f"Erro ao deletar item de '{tableName}': {e}")

        
        return Entity(item.id)
    
    def deleteTeamMember(self, person_id: str, team_id: str):
        """
        Remove uma pessoa de um time.
        Isso atualiza a tabelas 'team' (remove de employeeIds).
        """
        try:
            with self.__db:
                cursor = self.__db.cursor()

                # --- Etapa 1: Atualizar a tabela 'team' ---
                # 1a. Obter a lista atual
                cursor.execute("SELECT employeeIds FROM team WHERE id = ?", (team_id,))
                row = cursor.fetchone()

                if row is None:
                    raise Exception(f"Time com ID {team_id} não encontrado.")

                current_ids_str = row[0]

                # 1b. Manipular a lista
                if current_ids_str:
                    id_list = current_ids_str.split(',')
                    
                    # 1c. Remover o ID se ele existir na lista
                    if person_id in id_list:
                        id_list.remove(person_id)
                        new_ids_str = ",".join(id_list)
                        
                        # 1d. Salvar a nova lista
                        cursor.execute("UPDATE team SET employeeIds = ? WHERE id = ?", (new_ids_str, team_id))
                    else:
                        print(f"Aviso: Membro {person_id} não estava na lista employeeIds do time {team_id}.")
                else:
                    print(f"Aviso: Time {team_id} já estava sem membros na lista.")

            print(f"Membro {person_id} removido do time {team_id} com sucesso.")
            return True

        except sqlite3.Error as e:
            print(f"Erro de Banco de Dados ao remover membro: {e}")
            return False
        except Exception as e:
            print(f"Erro: {e}")
            return False

    def getPersonByID(self, personID: str):
        """Retorna uma pessoa pelo ID."""
        query = "SELECT * FROM person WHERE id = ?"
        df = pd.read_sql(query, self.__db, params=(personID,))

        if df.empty:
            print(f"[AVISO] Nenhuma pessoa encontrada com o ID {personID}.")
            return None

        # Converte o campo JSON de volta para lista
        df["responsibleIds"] = df["responsibleIds"].apply(
            lambda x: json.loads(x) if x else []
        )

        # Constrói um objeto Person a partir do DataFrame
        row = df.iloc[0]
        if row["role"] == "Employee":
            person = Person(
                id=row["id"],
                name=row["name"],
                cpf=row["cpf"],
                companyID=row["companyID"],
                departmentID=row["departmentID"],
                teamID=row["teamID"],
                role=row["role"],
                email=row["email"],
                password=row["password"]
            )
        elif row["role"] == "Manager":
            person = Manager(
                id=row["id"],
                name=row["name"],
                cpf=row["cpf"],
                companyID=row["companyID"],
                departmentID=row["departmentID"],
                teamID=row["teamID"],
                role=row["role"],
                email=row["email"],
                password=row["password"],
                responsibleIds=row["responsibleIds"]
            )
        elif row["role"] == "Director":
            person = Director(
                id=row["id"],
                name=row["name"],
                cpf=row["cpf"],
                companyID=row["companyID"],
                departmentID=row["departmentID"],
                teamID=row["teamID"],
                role=row["role"],
                email=row["email"],
                password=row["password"],
                responsibleIds=row["responsibleIds"]
            )
        return person
    
    def getPersonByEmail(self, email: str):
        """Retorna uma pessoa pelo email."""
        query = "SELECT * FROM person WHERE email = ?"
        df = pd.read_sql(query, self.__db, params=(email,))

        if df.empty:
            print(f"[AVISO] Nenhuma pessoa encontrada com o email {email}.")
            return None

        # Converte o campo JSON de volta para lista
        df["responsibleIds"] = df["responsibleIds"].apply(
            lambda x: json.loads(x) if x else []
        )

        # Constrói um objeto Person a partir do DataFrame
        row = df.iloc[0]
        if row["role"] == "Employee":
            person = Person(
                id=row["id"],
                name=row["name"],
                cpf=row["cpf"],
                companyID=row["companyID"],
                departmentID=row["departmentID"],
                teamID=row["teamID"],
                role=row["role"],
                email=row["email"],
                password=row["password"]
            )
        elif row["role"] == "Manager":
            person = Manager(
                id=row["id"],
                name=row["name"],
                cpf=row["cpf"],
                companyID=row["companyID"],
                departmentID=row["departmentID"],
                teamID=row["teamID"],
                role=row["role"],
                email=row["email"],
                password=row["password"],
                responsibleIds=row["responsibleIds"]
            )
        elif row["role"] == "Director":
            person = Director(
                id=row["id"],
                name=row["name"],
                cpf=row["cpf"],
                companyID=row["companyID"],
                departmentID=row["departmentID"],
                teamID=row["teamID"],
                role=row["role"],
                email=row["email"],
                password=row["password"],
                responsibleIds=row["responsibleIds"]
            )
        return person

    def getCompanyByID(self, companyID: str):
        query = "SELECT * FROM company WHERE id = ?"
        df = pd.read_sql(query, self.__db, params=(companyID,))
        
        if df.empty:
            return None
        
        row = df.iloc[0]
        # Desserializa os campos JSON
        rpeIds = json.loads(row["rpeIds"]) if row["rpeIds"] else []
        departmentsIds = json.loads(row["departmentsIds"]) if row["departmentsIds"] else []
        directorsIds = json.loads(row["directorsIds"]) if row["directorsIds"] else []
        
        # Recria o objeto Company
        return Company(
            id=row["id"],
            name=row["name"],
            rpeIds=rpeIds,
            cnpj=row["cnpj"],
            departmentsIds=departmentsIds,
            directorsIds=directorsIds
        )

    def getDepartmentByID(self, departmentID: str):
        query = "SELECT * FROM department WHERE id = ?"
        df = pd.read_sql(query, self.__db, params=(departmentID,))
        
        if df.empty:
            return None
        
        row = df.iloc[0]
        # Desserializa os campos JSON
        rpeIds = json.loads(row["rpeIds"]) if row["rpeIds"] else []
        teamsIds = json.loads(row["teamsIds"]) if row["teamsIds"] else []
        
        # Recria o objeto Department
        return Department(
            id=row["id"],
            name=row["name"],
            rpeIds=rpeIds,
            directorID=row["directorID"],
            teamsIds=teamsIds
        )

    def getTeamByID(self, teamID: str):
        query = "SELECT * FROM team WHERE id = ?"
        df = pd.read_sql(query, self.__db, params=(teamID,))
        
        if df.empty:
            return None
        
        row = df.iloc[0]
        # Desserializa os campos JSON
        rpeIds = json.loads(row["rpeIds"]) if row["rpeIds"] else []
        employeeIds = json.loads(row["employeesIds"]) if row["employeesIds"] else []
        
        # Recria o objeto Department
        return Team(
            id=row["id"],
            name=row["name"],
            rpeIds=rpeIds,
            managerID=row["managerID"],
            employeeIds=employeeIds
        )

    def getObjectiveById(self, objectiveID: str):
        """
        Retorna um objeto Objective pelo seu ID.
        """
        query = "SELECT * FROM objective WHERE id = ?"
        df = pd.read_sql(query, self.__db, params=(objectiveID,))

        if df.empty:
            print(f"[AVISO] Nenhum Objective encontrado com o ID {objectiveID}.")
            return None

        # Pega a primeira (e única) linha
        row = df.iloc[0]

        # Desserializa os campos JSON de volta para listas
        krIdsText = json.loads(row["krIds"]) if row["krIds"] else []
        kpiIdsText = json.loads(row["kpiIds"]) if row["kpiIds"] else []

        try:
            # Recria o objeto Objective
            return Objective(
                id=row["id"],
                description=row["description"],
                responsibleID=row["responsibleID"],
                krIds=krIdsText,
                kpiIds=kpiIdsText
            )
        
        except Exception as e:
            print(f"Erro ao recriar objeto Objective: {e}")
            return None

    def getRPEById(self, rpeID: str):
        """
        Retorna um objeto RPE pelo seu ID.
        """
        query = "SELECT * FROM rpe WHERE id = ?"
        df = pd.read_sql(query, self.__db, params=(rpeID,))

        if df.empty:
            print(f"[AVISO] Nenhum RPE encontrado com o ID {rpeID}.")
            return None

        # Pega a primeira (e única) linha
        row = df.iloc[0]

        # Desserializa o campo JSON de volta para uma lista
        objectivesIdsText = json.loads(row["objectivesIds"]) if row["objectivesIds"] else []

        try:
            # Recria o objeto RPE
            return RPE(
                id=row["id"],
                description=row["description"],
                responsibleID=row["responsibleID"],
                objectivesIds=objectivesIdsText
            )
        except Exception as e:
            print(f"Erro ao recriar objeto RPE: {e}")
            return None

    def getKPIByID(self, kpiID: str):
        query = "SELECT * FROM kpi WHERE id = ?"
        df = pd.read_sql(query, self.__db, params=(kpiID,))
        
        if df.empty:
            return None
            
        row = df.iloc[0]
        # Desserializa o vetor de floats
        data_list = json.loads(row["data"]) if row["data"] else []
        if row["goal"]=="-1":
            return KR(
                id=row["id"],
                description=row["description"],
                responsibleID=row["responsibleID"],
                data=data_list
            )
        else:
            return KPI(
                id=row["id"],
                description=row["description"],
                responsibleID=row["responsibleID"],
                data=data_list,
                goal=row["goal"]
            )
    
    def getAllCompanyRPEs(self, company: Company) -> list: # Retorna list[RPE]
        """
        Retorna uma lista de todos os objetos RPE associados a uma Company específica.
        """
        # 1. Pega a lista de IDs de RPE do objeto Company
        rpeIDText = company.rpeIds
        
        # 2. Se a lista estiver vazia, não há nada para buscar.
        if not rpeIDText:
            print(f"[INFO] Companhia {company.name} não possui RPEs associados.")
            return [] # Retorna uma lista vazia
            
        # 3. Cria os placeholders (?) para a consulta SQL.
        # Se a lista for ['id1', 'id2', 'id3'], placeholders será "?,?,?"
        placeholders = ','.join(['?'] * len(rpeIDText))
        
        # 4. Cria a consulta SQL
        # Esta é a forma segura de fazer "WHERE id IN (lista)"
        query = f"SELECT * FROM rpe WHERE id IN ({placeholders})"
        
        # 5. Executa a consulta
        # 'params' recebe a lista de IDs para preencher os '?'
        df = pd.read_sql(query, self.__db, params=rpeIDText)
        
        if df.empty:
            print(f"[AVISO] A Companhia {company.name} tem IDs de RPEs, mas eles não foram encontrados no banco.")
            return []
            
        # 6. Converte o DataFrame em uma lista de objetos RPE
        # (Esta lógica é a mesma do seu 'getAllRPEs')
        rpeList = []
        for row in df.itertuples(index=False):
            
            # Desserializa o campo JSON
            objectivesIds_list = json.loads(row.objectivesIds) if row.objectivesIds else []
            
            try:
                # Cria o objeto RPE e o adiciona à lista
                rpe = RPE(
                    id=row.id,
                    description=row.description,
                    responsibleID=row.responsibleID,
                    objectivesIds=objectivesIds_list
                )
                rpeList.append(rpe)
            except Exception as e:
                print(f"Erro ao recriar RPE (ID: {row.id}): {e}")
                
        return rpeList

    def close(self):
        """Fecha a conexão com o banco."""
        self.__db.close()