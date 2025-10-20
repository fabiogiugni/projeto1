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

class Database:

    def __init__(self):
        self.__db = sqlite3.connect('database/database.sql')

        self.__db.executescript('''
            CREATE TABLE IF NOT EXISTS person (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                cpf TEXT UNIQUE,
                companyID TEXT UNIQUE,
                departmentID TEXT UNIQUE,
                teamID TEXT UNIQUE,
                role TEXT,
                email TEXT UNIQUE,
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
                directorID TEXT UNIQUE,
                teamsIds TEXT
                )
            CREATE TABLE IF NOT EXISTS team (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                rpeIds TEXT,
                managerID TEXT UNIQUE,
                employeeIds TEXT
                )
            CREATE TABLE IF NOT EXISTS rpe (
                id TEXT PRIMARY KEY,
                description TEXT,
                responsibleID TEXT,
                objectivesIds TEXT
                )
            CREATE TABLE IF NOT EXISTS objective (
                id TEXT PRIMARY KEY,
                description TEXT,
                responsibleID TEXT,
                krIds TEXT,
                kpiIds TEXT
                )
            CREATE TABLE IF NOT EXISTS kpi (
                id TEXT PRIMARY KEY,
                description TEXT,
                responsibleID TEXT,
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

            # --- Serializa a lista de IDs para texto (JSON) ---
            responsibleIdsText = json.dumps(item.responsibleIds)

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
                        responsibleIdsText)  #Em Person, o responsibleIds deve ser inicializado com algum valor padrão
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
                        dataText, # Salva o vetor como texto
                        item.goal
                    )
                )
                self.__saveData()
                print(f"KPI {item.id} adicionado.")

            except sqlite3.IntegrityError as e:
                print(f"Erro ao adicionar KPI (ID já existe?): {e}")

        else:
            print(f"[ERRO] Tipo de item desconhecido: {type(item)}")

    def deleteItem(self, item: Entity):
        """Remove um item do banco de dados, de acordo com o tipo da entidade."""
        
        table_name = None
        if isinstance(item, Person): table_name = "person"
        elif isinstance(item, Company): table_name = "company"
        elif isinstance(item, Department): table_name = "department"
        elif isinstance(item, Team): table_name = "team"
        elif isinstance(item, RPE): table_name = "rpe"
        elif isinstance(item, Objective): table_name = "objective"
        elif isinstance(item, KPI): table_name = "kpi"
        else:
            print(f"[ERRO] Não é possível deletar tipo desconhecido: {type(item)}")
            return

        try:
            # Usamos f-string de forma segura pois table_name é controlado internamente
            query = f"DELETE FROM {table_name} WHERE id = ?"
            cursor = self.__db.execute(query, (item.id,))
            self.__saveData()

            if cursor.rowcount == 0:
                print(f"[AVISO] Nenhum registro encontrado em '{table_name}' com o ID {item.id}.")
            else:
                print(f"Item de '{table_name}' com ID {item.id} removido com sucesso.")
        
        except sqlite3.Error as e:
            print(f"Erro ao deletar item de '{table_name}': {e}")

    def getPersonById(self, person_id: str):
        """Retorna uma pessoa pelo ID."""
        query = "SELECT * FROM person WHERE id = ?"
        df = pd.read_sql(query, self.__db, params=(person_id,))

        if df.empty:
            print(f"[AVISO] Nenhuma pessoa encontrada com o ID {person_id}.")
            return None

        # Converte o campo JSON de volta para lista
        df["responsibleIds"] = df["responsibleIds"].apply(
            lambda x: json.loads(x) if x else []
        )

        # Constrói um objeto Person a partir do DataFrame
        row = df.iloc[0]
        if row["role"] == "Employee":
            person = Employee(
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
    
    def close(self):
        """Fecha a conexão com o banco."""
        self.__db.close()