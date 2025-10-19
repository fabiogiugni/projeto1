import sqlite3
import pandas as pd
from entity import Entity

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
            ''')
        self.__df = pd.read_sql("SELECT * FROM person", self.__db)

    def __saveData(self):
        """Salva as alterações pendentes."""
        self.__db.commit()

    def addItem(self, item: Entity):
        if isinstance(item, Person):
            try:
                # Usando '?' para evitar SQL Injection
                self.__db.execute(
                    "INSERT INTO person (id, name, cpf, companyID, departmentID, teamID, role, email, password, responsibleIds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        item.id['id'], 
                        item.name['name'], 
                        item.cpf['cpf'],
                        item.companyID['companyID'],
                        item.departmentID['departmentID'],
                        item.teamID['teamID'],
                        item.role['role'],
                        item.email['email'],
                        item.password['password'],
                        item.responsibleIds['responsibleIds'])  #Em Person, o responsibleIds deve ser inicializado com algum valor padrão
                )
                self.saveData()
                print(f"Pessoa {item['name']} adicionada.")
            except sqlite3.IntegrityError as e:
                print(f"Erro ao adicionar pessoa (ID ou Email já existe?): {e}")
