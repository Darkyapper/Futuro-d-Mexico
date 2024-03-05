import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('baseuno.sqlite')

# Crear un cursor
cursor = conn.cursor()

#SELECCIONAR
#cursor.execute("SELECT * FROM machines")

#INSERTAR
#cursor.execute("INSERT INTO machines (serial_no,status,location) VALUES (97251,'On','Tixkokob')")
#conn.commit()

#BORRAR
#cursor.execute("DELETE FROM machines WHERE serial_no=97251")
#conn.commit()

print(cursor.fetchall())

conn.close()