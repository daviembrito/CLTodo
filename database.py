import sqlite3
from task import Task

conn = sqlite3.connect("todos.db")
cursor = conn.cursor()

def getTablesNames():
    cursor.execute("""SELECT name FROM sqlite_master 
        WHERE type = 'table' 
        AND name != 'sqlite_sequence';""")
    
    tables = cursor.fetchall()
    if not tables:
        return ["No list found!"]
    
    tables_list = [table[0] for table in tables]
    return tables_list

def getNumberOfTables():
    cursor.execute("""SELECT count(*) FROM sqlite_master 
            WHERE type='table' 
            AND name!='sqlite_sequence';""")
    num_tables = cursor.fetchone()[0]
    return num_tables

def createTable(table_name:str):
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            posicao INTEGER NOT NULL,
            todo TEXT NOT NULL,
            category TEXT,
            date_added TEXT PRIMARY KEY,
            date_completed TEXT,
            done BOOLEAN NOT NULL);""")
    
def deleteTable(table_name:str):
    cursor.execute(f"DROP TABLE {table_name}")

def addTaskToTable(task:Task, table_name:str):
    with conn:
        cursor.execute(f"""INSERT INTO {table_name}
            (posicao, todo, category, date_added, done) 
            VALUES ((SELECT IFNULL(MAX(posicao), 0) + 1 FROM {table_name}), 
            '{task.name}', 
            '{task.category}', 
            '{task.created_date}', 
            FALSE);""")

def tableExists(table_name:str):
    cursor.execute(f"""SELECT name FROM sqlite_master
            WHERE type='table' 
            AND name='{table_name}';""")
    
    result = cursor.fetchone()
    if result:
        return True
    
    return False