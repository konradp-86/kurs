import sqlite3
from sqlite3 import Error

def create_connection(db_file):
   """ create a tabela1 connection to a SQLite tabela1 """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
   except Error as e:
       print(e)
   return conn

def create_connection_in_memory():
   """ create a tabela1 connection to a SQLite tabela1 """
   conn = None
   try:
       conn = sqlite3.connect(":memory:")
       print(f"Connected, sqlite version: {sqlite3.version}")
   except Error as e:
       print(e)
   return conn

def create_tables(conn):
    """ create tables in the provided database connection """
    try:
        cursor = conn.cursor()
        cursor.execute(create_projects_sql)
        cursor.execute(create_tasks_sql)
        print("Tables created successfully")
    except Error as e:
        print(e)

create_projects_sql = """
-- projects table
CREATE TABLE IF NOT EXISTS projects (
  id integer PRIMARY KEY,
  nazwa text NOT NULL,
  start_date text,
  end_date text
);
"""

create_tasks_sql = """
-- zadanie table
CREATE TABLE IF NOT EXISTS tasks (
  id integer PRIMARY KEY,
  project_id integer NOT NULL,
  nazwa VARCHAR(250) NOT NULL,
  opis TEXT,
  status VARCHAR(15) NOT NULL,
  start_date text NOT NULL,
  end_date text NOT NULL,
  FOREIGN KEY (project_id) REFERENCES projects (id)
);
"""

if __name__ == '__main__':
    conn = create_connection(r"tabela1.db")
    if conn is not None:
        create_tables(conn)
        conn.close()

    conn_in_memory = create_connection_in_memory()
    if conn_in_memory is not None:
        create_tables(conn_in_memory)
        conn_in_memory.close()