import sqlite3

class Database:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect('database.db')
            cls._instance.cursor = cls._instance.conn.cursor()
            cls._instance.create_tables_if_not_exist()
        return cls._instance

    def close(self):
        self.conn.commit()
        self.conn.close()

    def create_tables_if_not_exist(self):
        self._create_user_table()
        self._create_groceries_table()
        
    def _create_user_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY
            )
        ''')
    
    def _create_groceries_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groceries (
                id INTEGER PRIMARY KEY,
                name TEXT,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

    def insert_data(self, table_name, columns, data):
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['?'] * len(columns))

        insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    
        self.cursor.execute(insert_sql, data)
        
        self.conn.commit()


