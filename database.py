import sqlite3

# Conecta ao banco de dados
conn = sqlite3.connect('todos.db')
cursor = conn.cursor()

def getTables():
    number_of_tables = getNumberOfTables()
    if (number_of_tables == 0):
        return ["No lists found"]
    
    return number_of_tables

def getNumberOfTables():
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
    num_tables = cursor.fetchone()[0]
    return num_tables
    

# Exibe o número de tabelas
print(f"Existem {getNumberOfTables()} tabelas na base de dados")

# Fecha a conexão
conn.close()