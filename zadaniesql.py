import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Połączono z {db_file}, wersja SQLite: {sqlite3.version}")
    except Error as e:
        print(e)
    return conn

def create_connection_in_memory():
    conn = None
    try:
        conn = sqlite3.connect(":memory:")
        print(f"Połączono, wersja SQLite: {sqlite3.version}")
    except Error as e:
        print(e)
    return conn

def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(create_projects_sql)
        cursor.execute(create_tasks_sql)
        print("Tabele zostały utworzone")
    except Error as e:
        print(e)

create_projects_sql = """
-- tabela projects
CREATE TABLE IF NOT EXISTS projects (
  id integer PRIMARY KEY,
  nazwa text NOT NULL,
  start_date text,
  end_date text
);
"""

create_tasks_sql = """
-- tabela tasks
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

def add_project(conn, project):
    sql = ''' INSERT INTO projects(nazwa, start_date, end_date)
              VALUES(?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    print("Nowy projekt został dodany do tabeli 'projects'")
    return cur.lastrowid

def add_task(conn, task):
    sql = ''' INSERT INTO tasks(project_id, nazwa, opis, status, start_date, end_date)
              VALUES(?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    print("Nowe zadanie zostało dodane do tabeli 'tasks'")
    return cur.lastrowid

def fetch_projects(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM projects")
        rows = cur.fetchall()
        print("Projekty:")
        for row in rows:
            print(row)
        print("Pobieranie projektów zostało wykonane.")
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
        print("Pobieranie zadań zostało wykonane.")
        return rows
    except Error as e:
        print(f"Błąd podczas pobierania zadań: {e}")
        return []

def update_task(conn, task_id, status, start_date, end_date):
    sql = '''
    UPDATE tasks
    SET status = ?,
        start_date = ?,
        end_date = ?
    WHERE id = ?;
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (status, start_date, end_date, task_id))
        conn.commit()
        print(f"Zadanie o ID {task_id} zostało zaktualizowane")
        print("Aktualizacja zadania została wykonana.")
    except Error as e:
        print(f"Błąd podczas aktualizacji zadania: {e}")

def delete_tasks_by_project(conn, project_id):
    sql = '''
    DELETE FROM tasks
    WHERE project_id = ?;
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (project_id,))
        conn.commit()
        print(f"Zadania związane z projektem o ID {project_id} zostały usunięte.")
        print("Usuwanie zadań związanych z projektem zostało wykonane.")
    except Error as e:
        print(f"Błąd podczas usuwania zadań: {e}")

def delete_project(conn, project_id):
    sql = '''
    DELETE FROM projects
    WHERE id = ?;
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (project_id,))
        conn.commit()
        print(f"Projekt o ID {project_id} został usunięty.")
        print("Usuwanie projektu zostało wykonane.")
    except Error as e:
        print(f"Błąd podczas usuwania projektu: {e}")

if __name__ == '__main__':
    database = r"tabela1.db"
    conn = create_connection(database)
    if conn:
        create_tables(conn)
        print("Tworzenie tabel zostało wykonane.")

        project = ('zrób zadanie', '2025-01-01', '2025-12-31')
        project_id = add_project(conn, project)
        print("Dodawanie projektu zostało wykonane.")

        task = (project_id, 'zrób zadanie', 'Description of task', 'Pending', '2025-01-01', '2025-12-31')
        task_id = add_task(conn, task)
        print("Dodawanie zadania zostało wykonane.")

        fetch_projects(conn)
        fetch_tasks(conn)

        task_id = 1
        status = "ended"
        start_date = "2025-01-01 12:00:00"
        end_date = "2025-01-01 15:00:00"
        update_task(conn, task_id, status, start_date, end_date)

        project_id = 1
        delete_tasks_by_project(conn, project_id)
        delete_project(conn, project_id)

        conn.close()
        print("Połączenie z bazą danych zostało zamknięte.")
