import sqlite3
from sqlite3 import Error

# def create_connection(db_file):
#    conn = None
#    try:
#        conn = sqlite3.connect(db_file)
#        print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
#    except Error as e:
#        print(e)
#    return conn
# def create_connection_in_memory():
#    conn = None
#    try:
#        conn = sqlite3.connect(":memory:")
#        print(f"Connected, sqlite version: {sqlite3.version}")
#    except Error as e:
#        print(e)
#    return conn
# def create_tables(conn):
#     try:
#         cursor = conn.cursor()
#         cursor.execute(create_projects_sql)
#         cursor.execute(create_tasks_sql)
#         print("Tables created successfully")
#     except Error as e:
#         print(e)
# create_projects_sql = """
# -- projects table
# CREATE TABLE IF NOT EXISTS projects (
#   id integer PRIMARY KEY,
#   nazwa text NOT NULL,
#   start_date text,
#   end_date text
# );
# """

# create_tasks_sql = """
# -- zadanie table
# CREATE TABLE IF NOT EXISTS tasks (
#   id integer PRIMARY KEY,
#   project_id integer NOT NULL,
#   nazwa VARCHAR(250) NOT NULL,
#   opis TEXT,
#   status VARCHAR(15) NOT NULL,
#   start_date text NOT NULL,
#   end_date text NOT NULL,
#   FOREIGN KEY (project_id) REFERENCES projects (id)
# );
# """

# def create_connection(db_file):
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
#     except Error as e:
#         print(e)
#     return conn

# def add_project(conn, project):
#     sql = ''' INSERT INTO projects(nazwa, start_date, end_date)
#               VALUES(?, ?, ?) '''
#     cur = conn.cursor()
#     cur.execute(sql, project)
#     return cur.lastrowid

# def add_task(conn, task):
#     sql = ''' INSERT INTO tasks(project_id, nazwa, opis, status, start_date, end_date)
#               VALUES(?, ?, ?, ?, ?, ?) '''
#     cur = conn.cursor()
#     cur.execute(sql, task)
#     return cur.lastrowid

# if __name__ == '__main__':
#     database = r"tabela1.db"
#     conn = create_connection(database)
#     if conn:
#         project = ('zrób zadanie', '2025-01-01', '2025-12-31')
#         project_id = add_project(conn, project)

#         task = (project_id, 'zrób zadanie', 'Description of task', 'Pending', '2025-01-01', '2025-12-31')
#         task_id = add_task(conn, task)

#         conn.commit()
#         conn.close()

# def create_connection(db_file):
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         print(f"Połączono z {db_file}, wersja SQLite: {sqlite3.version}")
#         return conn
#     except Error as e:
#         print(e)
#         return None

# def insert_project(conn, project):
#     sql = '''INSERT INTO projects(nazwa, start_date, end_date)
#              VALUES(?, ?, ?)'''
#     try:
#         cur = conn.cursor()
#         cur.execute(sql, project)
#         conn.commit()
#         print("Nowy projekt został dodany do tabeli 'projects'")
#     except Error as e:
#         print(f"Błąd podczas wstawiania danych: {e}")

# def create_connection(db_file):
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         print(f"Połączono z {db_file}, wersja SQLite: {sqlite3.version}")
#         return conn
#     except Error as e:
#         print(e)
#         return None

# def insert_project(conn, project):
#     sql = '''INSERT INTO projects(nazwa, start_date, end_date)
#              VALUES(?, ?, ?)'''
#     try:
#         cur = conn.cursor()
#         cur.execute(sql, project)
#         conn.commit()
#         print("Nowy projekt został dodany do tabeli 'projects'")
#         return cur.lastrowid
#     except Error as e:
#         print(f"Błąd podczas wstawiania projektu: {e}")

# def add_task(conn, task):
#     sql = '''INSERT INTO tasks(project_id, nazwa, opis, status, start_date, end_date)
#              VALUES(?, ?, ?, ?, ?, ?)'''
#     try:
#         cur = conn.cursor()
#         cur.execute(sql, task)
#         conn.commit()
#         print("Nowe zadanie zostało dodane do tabeli 'tasks'")
#         return cur.lastrowid
#     except Error as e:
#         print(f"Błąd podczas wstawiania zadania: {e}")

# if __name__ == "__main__":
#     tabela1 = r"tabela1.db"
#     conn = create_connection(tabela1)
#     if conn:
#         project = ("Powtórka z angielskiego", "2020-05-11 00:00:00", "2020-05-13 00:00:00")
#         pr_id = insert_project(conn, project)

#         task = (
#             pr_id,
#             "Czasowniki regularne",
#             "Zapamiętaj czasowniki ze strony 30",
#             "started",
#             "2020-05-11 12:00:00",
#             "2020-05-11 15:00:00"
#         )

#         task_id = add_task(conn, task)

#         print(f"Projekt ID: {pr_id}, Zadanie ID: {task_id}")
#         new_var = conn.commit()
#         new_var
#         conn.close()

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Połączono z {db_file}, wersja SQLite: {sqlite3.version}")
        return conn
    except Error as e:
        print(e)
        return None

def fetch_projects(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM projects")
        rows = cur.fetchall()
        print("Projekty:")
        for row in rows:
            print(row)
        return rows
    except Error as e:
        print(f"Błąd podczas pobierania projektów: {e}")
        return []

def fetch_tasks(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks")
        rows = cur.fetchall()
        print("Zadania:")
        for row in rows:
            print(row)
        return rows
    except Error as e:
        print(f"Błąd podczas pobierania zadań: {e}")
        return []

if __name__ == "__main__":
    tabela1 = r"tabela1.db"
    conn = create_connection(tabela1)
    if conn:
        fetch_projects(conn)
        fetch_tasks(conn)
        conn.close()
