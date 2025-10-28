from person import Person
from database import Database

class UserAuth:

    def login(self, email: str, password: str, db: Database) -> bool:
        person = db.getPersonByEmail(email)
        if person.verifyPassword(password):
            return True
        else:
            return False