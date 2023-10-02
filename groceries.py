from database import Database

class Groceries:

    _determinants = ['d', 'des', 'du', 'de la', 'un', 'une']

    def __init__(self) -> None:
        self._database = Database()

    def find_determinant_index(self, words : list[str]) -> int:
        for determinant in self._determinants:
            if determinant in words:
                index_of_determinant = words.index(determinant)
                return index_of_determinant
        return -1
    
    def find_grocery(self, message: str, author: int) -> str:
        words = message.split()
        index = self.find_determinant_index(words)
        if index == -1:
            return "Désolé, je n'ai pas compris, que voulez-vous ajouter à votre liste de courses ?"
        elif index < len(words) - 1:
            return self.add_grocery_to_database(words[index+1], author)
        else:
            return "Désolé, je n'ai pas compris, que voulez-vous ajouter à votre liste de courses ?"
    
    def add_grocery_to_database(self, grocery: str, author: int) -> str:
        if not self.exists(author):
            insert_sql = "INSERT INTO users (name) VALUES (?)"
            self._database.cursor.execute(insert_sql, (author,))

            self._database.conn.commit()   
        
        self._database.insert_data('groceries', ["name", "user_id"], [grocery, author])
        self._database.close()
        return f"Très bien, j'ai bien ajouté **{grocery}** à ta liste de courses."

    def exists(self, user_name: int) -> bool:
        self._database.cursor.execute("SELECT id FROM users WHERE id = ?", (user_name,))
        result = self._database.cursor.fetchone()
        
        if result:
            return True
        return False

    def add_grocery(self, message, author) -> str:
        return self.find_grocery(message, author)