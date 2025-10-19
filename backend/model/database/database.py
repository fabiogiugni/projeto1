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

class Database:

    def __init__(self):
        self.__db = sqlite3.connect('database/database.sql')

        self.__db.execute('''
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
                directorId TEXT UNIQUE,
                teamsIds TEXT
                )
            CREATE TABLE IF NOT EXISTS team (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                rpeIds TEXT,
                managerId TEXT UNIQUE,
                employeeIds TEXT
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
                print(f"Pessoa {item.name['name']} adicionada.")
            
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
                    "INSERT INTO person (id, name, cpf, companyID, departmentID, teamID, role, email, password, responsibleIds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        item.id, 
                        item.name, 
                        rpeIdsText,
                        item.cnpj,
                        departmentsIdsText,
                        directorsIdsText)
                )
                self.__saveData()
                print(f"Company {item.name['name']} adicionada.")
            
            except sqlite3.IntegrityError as e:
                print(f"Erro ao adicionar Company (ID ou CNPJ já existe?): {e}")
        
        elif isinstance(item, Department):
            
            # --- Serializa a lista de IDs para texto (JSON) ---
            rpeIdsText = json.dumps(item.rpeIds)
            teamsIdsText = json.dumps(item.directorsIds)

            try:
                # Usando '?' para evitar SQL Injection
                self.__db.execute(
                    "INSERT INTO person (id, name, cpf, companyID, departmentID, teamID, role, email, password, responsibleIds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        item.id, 
                        item.name, 
                        rpeIdsText,
                        item.directorID,
                        teamsIdsText)
                )
                self.__saveData()
                print(f"Department {item.name['name']} adicionado.")
            
            except sqlite3.IntegrityError as e:
                print(f"Erro ao adicionar Department (ID ou DirectorID já existe?): {e}")
        
        elif isinstance(item, Team):
            
            # --- Serializa a lista de IDs para texto (JSON) ---
            rpeIdsText = json.dumps(item.rpeIds)
            employeeIdsText = json.dumps(item.directorsIds)

            try:
                # Usando '?' para evitar SQL Injection
                self.__db.execute(
                    "INSERT INTO person (id, name, cpf, companyID, departmentID, teamID, role, email, password, responsibleIds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        item.id, 
                        item.name, 
                        rpeIdsText,
                        item.managerID,
                        employeeIdsText)
                )
                self.__saveData()
                print(f"Team {item.name['name']} adicionado.")
            
            except sqlite3.IntegrityError as e:
                print(f"Erro ao adicionar Team (ID ou ManagerID já existe?): {e}")

    def deleteItem(self, item : Entity):
        """Remove um item do banco de dados, de acordo com o tipo da entidade."""
        try:
            cursor = self.__db.execute("DELETE FROM person WHERE id = ?", (item.id,))
            self.__saveData()

            if cursor.rowcount == 0:
                print(f"[AVISO] Nenhum registro encontrado com o ID {item.id}.")
            else:
                print(f"Pessoa com ID {item.id} removida com sucesso.")
        
        except sqlite3.Error as e:
            print(f"Erro ao deletar pessoa: {e}")

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
                responibleIds=row["responsibleIds"]
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
                responibleIds=row["responsibleIds"]
            )
        return person