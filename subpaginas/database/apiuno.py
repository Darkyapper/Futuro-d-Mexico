import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('machines.db')

# Crear un cursor
cursor = conn.cursor()

# Ejecutar una consulta
cursor.execute("SELECT * FROM machines")

# Obtener los resultados
resultados = cursor.fetchall()

# Cerrar la conexión
conn.close()