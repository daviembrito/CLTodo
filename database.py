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

def getAllRows(table_name:str):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    tasks = []
    for row in rows:
        tasks.append(Task(*row))
    return tasks

def createTable(table_name:str):
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            position INTEGER NOT NULL,
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
            (position, todo, category, date_added, done) 
            VALUES ((SELECT IFNULL(MAX(position), 0) + 1 FROM {table_name}), 
            '{task.name}', 
            '{task.category}', 
            '{task.created_date}', 
            FALSE);""")
        
def removeTaskFromTable(task_position:int, table_name:str):
    with conn:
        cursor.execute(f"""DELETE FROM {table_name} 
            WHERE position = {task_position};""")
        
        cursor.execute(f"""UPDATE {table_name}
            SET position = position-1 
            WHERE position > {task_position};""")


def invertTaskStatus(task_position:int, table_name:str):
    with conn:
        cursor.execute(f"""UPDATE {table_name}
            SET done = NOT done
            WHERE position = {task_position};""")

def tableExists(table_name:str):
    cursor.execute(f"""SELECT name FROM sqlite_master
            WHERE type='table' 
            AND name='{table_name}';""")
    
    result = cursor.fetchone()
    if result:
        return True
    
    return False