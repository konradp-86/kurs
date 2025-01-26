import sqlite3
from sqlite3 import Error

# def create_connection(db_file):
#    """ create a tabela1 connection to a SQLite tabela1 """
#    conn = None
#    try:
#        conn = sqlite3.connect(db_file)
#        print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
#    except Error as e:
#        print(e)
#    return conn

# def create_connection_in_memory():
#    """ create a tabela1 connection to a SQLite tabela1 """
#    conn = None
#    try:
#        conn = sqlite3.connect(":memory:")
#        print(f"Connected, sqlite version: {sqlite3.version}")
#    except Error as e:
#        print(e)
#    return conn

# def create_tables(conn):
#     """ create tables in the provided database connection """
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

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
    except Error as e:
        print(e)
    return conn

def add_project(conn, project):
    """ add a new project to the projects table """
    sql = ''' INSERT INTO projects(nazwa, start_date, end_date)
              VALUES(?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid

def add_task(conn, task):
    """ add a new task to the tasks table """
    sql = ''' INSERT INTO tasks(project_id, nazwa, opis, status, start_date, end_date)
              VALUES(?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid

if __name__ == '__main__':
    database = r"tabela1.db"
    conn = create_connection(database)
    if conn:
        project = ('zrób zadanie', '2025-01-01', '2025-12-31')
        project_id = add_project(conn, project)

        task = (project_id, 'zrób zadanie', 'Description of task', 'Pending', '2025-01-01', '2025-12-31')
        task_id = add_task(conn, task)

        conn.commit()
        conn.close()