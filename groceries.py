from database import Database

class Groceries:

    def __init__(self) -> None:
        database = Database()
        database.close()
    