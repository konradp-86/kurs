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
   finally:
       if conn:
           conn.close()

def create_connection_in_memory():
   """ create a tabela1 connection to a SQLite tabela1 """
   conn = None
   try:
       conn = sqlite3.connect(":memory:")
       print(f"Connected, sqlite version: {sqlite3.version}")
   except Error as e:
       print(e)
   finally:
       if conn:
           conn.close()

if __name__ == '__main__':
   create_connection(r"tabela1.db")
   create_connection_in_memory()