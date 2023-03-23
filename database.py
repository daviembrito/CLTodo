import sqlite3
from task import Task

conn = sqlite3.connect('todos.db')
cursor = conn.cursor()

def getTablesNames():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name!='sqlite_sequence';")
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

def createTable(table_name):
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            id integer primary key autoincrement,
            todo text,
            category text,
            date_added text,
            date_completed text,
            done integer);""")
    
def deleteTable(table_name):
    cursor.execute(f"DROP TABLE {table_name}")
    
def addTaskToTable(task : Task, table_id : int):
    pass

def tableExists(table_name):
    cursor.execute(f"""SELECT name FROM sqlite_master
            WHERE type='table' 
            AND name='{table_name}';""")
    
    result = cursor.fetchone()
    if result:
        return True
    
    return False