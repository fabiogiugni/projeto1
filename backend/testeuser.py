from model.database.database import Database
from model.entities.company import Company
from model.entities.department import Department
from model.entities.team import Team
from model.entities.person import Person

DB = Database("database.db")

DB.get_user_by_email

"""
new_company = Company("empresa1", "123456")
DB.addItem(new_company)

new_department = Department("dep 1", companyID=new_company.id)
DB.addItem(new_department)

new_team = Team("team 1", departmentID=new_department.id)
DB.addItem(new_team)

new_user = Person(
"thales",
"141.163.736-48",
companyID=new_company.id,
departmentID=new_department.id,
teamID=new_team.id,
email="thalesds@ufmg.br",
password="teste123")

DB.addItem(new_user)
"""