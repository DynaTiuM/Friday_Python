from database import Database

class Groceries:

    _determinants = ['d', 'des', 'du', 'de la', 'un', 'une']
    _deletes = ['supprime', 'enlève', 'retire']

    def __init__(self) -> None:
        self._database = Database()

    def find_prefix_index(self, words : list[str], tab) -> int:
        for prefix in tab:
            if prefix in words:
                return words.index(prefix)
        return -1
        
    
    def find_grocery(self, message: str, author: int, delete: bool) -> str:
        words = message.split()
        if not delete:
            index = self.find_prefix_index(words, self._determinants)
            if index == -1:
                return "Désolé, je n'ai pas compris, que veux-tu ajouter à ta liste de courses ?"
            elif index < len(words) - 1:
                return self.add_grocery_to_database(words[index+1], author)
            else:
                return "Désolé, je n'ai pas compris, que veux-tu ajouter à ta liste de courses ?"
        else:
            index = self.find_prefix_index(words, self._deletes)
            if index == -1:
                return "Désolé, je n'ai pas compris, que veux-tu supprimer de ta liste de courses ?"
            elif index < len(words) - 1:
                return self.remove_grocery_from_database(words[index+1], author)
            else:
                return "Désolé, je n'ai pas compris, que veux-tu supprimer de ta liste de courses ?"
    
    def add_grocery_to_database(self, grocery: str, author: int) -> str:
        if not self.exists(author):
            self._database.cursor.execute("INSERT INTO users VALUES (?)", (author,))  
            self._database.conn.commit()
        
        self._database.insert_data('groceries', ["name", "user_id"], [grocery, author])
    
        return f"Très bien, j'ai bien ajouté **{grocery}** à ta liste de courses."

    def exists(self, user_name: int) -> bool:
        self._database.cursor.execute("SELECT id FROM users WHERE id = ?", (user_name,))
        result = self._database.cursor.fetchone()
        
        if result:
            return True
        return False

    def add_grocery(self, message, author) -> str:
        return self.find_grocery(message, author, False)
    
    def get_groceries(self, author) -> str:
        groceries = self.find_groceries_from_database(author)
        groceries_str = 'Voici ta liste de courses : \n'
        if groceries != "none":
            for grocery in groceries:
                groceries_str += '➜ ' + grocery[0] + ' \n'

            return groceries_str
        else:
            return "Ta liste de courses est vide."
    
    def find_groceries_from_database(self, author) -> list[str]:
        self._database.cursor.execute("SELECT name FROM groceries where user_id  = ?", (author,))
        result = self._database.cursor.fetchall()

        if result:
            return result
        return "none"
    
    def remove_grocery_from_database(self, grocery, author) -> str:
        if self.check_grocery_exists(author, grocery):
            self._database.cursor.execute("DELETE FROM groceries WHERE user_id = ? AND name = ?", (author, grocery,))
            self._database.conn.commit()
            return f"J'ai retiré **{grocery}** de ta liste de courses.\n{self.get_groceries(author)}"
        else:
            return f"Désolé, mais l'élément que tu mentionnes n'est pas dans ta liste de courses.\n{self.get_groceries(author)}"

        
    def check_grocery_exists(self, author, grocery):
        self._database.cursor.execute("SELECT name FROM groceries WHERE user_id = ? AND name = ?", (author, grocery,))
        return self._database.cursor.fetchone() is not None

    def remove_grocery(self, message, author) -> str:
        return self.find_grocery(message, author, True)