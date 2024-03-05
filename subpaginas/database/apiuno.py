import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('baseuno.sqlite')

# Crear un cursor
cursor = conn.cursor()

cursor.execute("SELECT * FROM machines")

print(cursor.fetchall())