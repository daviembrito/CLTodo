import sqlite3
from todo import Todo

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
    cursor.execute(f"""SELECT * FROM {table_name}
            ORDER BY position""")
    rows = cursor.fetchall()

    todos = []
    for row in rows:
        todos.append(Todo(*row))
    return todos

def getRowsFromCategory(category:str, table_name:str):
    cursor.execute(f"""SELECT * FROM {table_name}
            WHERE category = '{category}'
            ORDER BY position""")
    rows = cursor.fetchall()

    tasks = []
    for row in rows:
        tasks.append(Todo(*row))
    return tasks

def createTable(table_name:str):
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            position INTEGER NOT NULL,
            todo TEXT NOT NULL,
            category TEXT,
            created_date TEXT PRIMARY KEY,
            done_date TEXT,
            done BOOLEAN NOT NULL);""")
    
def deleteTable(table_name:str):
    cursor.execute(f"DROP TABLE {table_name}")

def addTaskToTable(todo:Todo, table_name:str):
    with conn:
        cursor.execute(f"""INSERT INTO {table_name}
            (position, todo, category, created_date, done) 
            VALUES ((SELECT IFNULL(MAX(position), 0) + 1 FROM {table_name}), 
            '{todo.name}', 
            '{todo.category}', 
            '{todo.created_date}', 
            FALSE);""")
        
def removeTaskFromTable(todo_position:int, table_name:str):
    try:
        conn.execute("BEGIN TRANSACTION;")

        cursor.execute(f"""DELETE FROM {table_name} 
            WHERE position = {todo_position};""")
        
        cursor.execute(f"""UPDATE {table_name}
            SET position = position-1 
            WHERE position > {todo_position};""")
    
        conn.commit()
        
    except sqlite3.Error as error:
        conn.rollback()
        print("[ERRO] ", error)

def changeTaskPosition(old_position:int, new_position:int, table_name:str):
    try:
        conn.execute("BEGIN TRANSACTION;")

        cursor.execute(f"""UPDATE {table_name}
            SET position = 0
            WHERE position = {old_position};""")
        
        if new_position > old_position:
            cursor.execute(f"""UPDATE {table_name}
            SET position = position - 1 
            WHERE position > {old_position} 
            AND position <= {new_position}
            AND position > 0;""")
        else:
            cursor.execute(f"""UPDATE {table_name}
            SET position = position + 1 
            WHERE position >= {new_position} 
            AND position < {old_position}
            AND position > 0;""")
        
        cursor.execute(f"""UPDATE {table_name}
            SET position = {new_position}
            WHERE position = 0;""")
        
        conn.commit()
    
    except sqlite3.Error as error:
        conn.rollback()
        print("[ERROR] ", error)

def invertTaskStatus(todo_position:int, done_date:str, table_name:str):
    with conn:
        cursor.execute(f"""UPDATE {table_name}
            SET done_date = 
            CASE 
            WHEN done = TRUE THEN NULL ELSE '{done_date}'
            END, 
            done = NOT done
            WHERE position = {todo_position};""")

def tableExists(table_name:str):
    cursor.execute(f"""SELECT name FROM sqlite_master
            WHERE type='table' 
            AND name='{table_name}';""")
    
    result = cursor.fetchone()
    if result:
        return True
    
    return False