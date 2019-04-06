import sqlite3
import hashlib


class DB:
    def __init__(self, database):
        conn = sqlite3.connect(database, check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class UsersModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                 user_name VARCHAR(50),
                                 password_hash VARCHAR(128)
                                 )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                              (user_name, password_hash) 
                              VALUES (?,?)''', (user_name, password))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)


class AskModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS asks 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             question VARCHAR(1000),
                             answer VARCHAR(10000),
                             user_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert_question(self, question, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO asks 
                          (question, answer, user_id) 
                          VALUES (?,?,?)''', (question, '', str(user_id)))
        cursor.close()
        self.connection.commit()

    def insert_answer(self, answer, question_id):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE asks
                            SET answer = ?
                            WHERE id = ?''', (answer, str(question_id),))

    def get(self, asks_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM asks WHERE id = ?", (str(asks_id),))
        row = cursor.fetchone()
        return row

    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM asks WHERE user_id = ?",
                           (str(user_id),))
        else:
            cursor.execute("SELECT * FROM asks")
        rows = cursor.fetchall()
        return rows

    def delete(self, asks_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM asks WHERE id = ?''', (str(asks_id),))
        cursor.close()
        self.connection.commit()
