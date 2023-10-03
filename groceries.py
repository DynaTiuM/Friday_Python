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

            self._database.insert_data('users', author)    
        
            self._database.insert_data('groceries', [grocery, author])
            self._database.close()
            return f"Très bien, j'ai bien ajouté **{grocery}** à ta liste de courses."
        
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
    
    def get_groceries(self, author) -> str:
        groceries = self.find_groceries(author)
        groceries_str = 'Voici ta liste de courses : \n'
        if groceries != "none":
            for grocery in groceries:
                groceries_str += '\n->' + grocery[0]
                    
            return groceries_str
        else:
            return "Ta liste de courses est vide."
    
    def find_groceries(self, author) -> list[str]:
        self._database.cursor.execute("SELECT name FROM groceries where user_id  = ?", (author,))
        result = self._database.cursor.fetchall()

        if result:
            return result
        return "none"