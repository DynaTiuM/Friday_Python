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
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')

    def insert_data(self, table_name, data):
        placeholders = ', '.join(['?'] * len(data))
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(insert_sql, data)
        self.conn.commit()

    def display_users(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()

        for row in rows:
            print(f"ID: {row[0]}, Nom: {row[1]}")