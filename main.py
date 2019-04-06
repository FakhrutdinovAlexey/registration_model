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
                                 password_hash VARCHAR(128),
                                 user_type VARCHAR(10))''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password, user_type):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                              (user_name, password_hash, user_type) 
                              VALUES (?,?,?)''', (user_name, password, user_type))
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
        cursor.close()
        self.connection.commit()

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


class TasksModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_customer INTEGER,
                            task VARCHAR(1000),
                            status VARCHAR(10))''')
        cursor.close()
        self.connection.commit()

    def insert_task(self, id_customer, task, status):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO tasks
                        (id_customer, task, status)
                        VALUES (?,?,?)''', (str(id_customer), task, status))
        cursor.close()
        self.connection.commit()

    def get(self, task_id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM tasks WHERE id = ?''', str(task_id))
        row = cursor.fetchone()
        return row


class RequestModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS requests
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_performer INTEGER,
                        request VARCHAR(1000),
                        id_task INTEGER)''')
        cursor.close()
        self.connection.commit()

    def insert_request(self, id_performer, request, id_task):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO requests
                        (id_performer, request, id_task)
                        VALUES (?,?,?)''', (str(id_performer), request, str(id_task)))
        cursor.close()
        self.connection.commit()

    def get_by_id(self, id_task):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM requests WHERE id_task = ?''', str(id_task))
        rows = cursor.fetchall()
        return rows


if __name__ == '__main__':
    pass
