import sqlite3 as sql

DB_PATH = 'C:\\Users\\Yeika\\Documents\\Programación\\futuro-d-mexico\\database\\machines.db'

def create_DB():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE machines (serial_no INTEGER PRIMARY KEY, location TEXT, status TEXT)""")
    conn.commit()
    conn.close()

def add_values():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO machines (serial_no, location, status) VALUES (97245, 'Paseo De Montejo', 'On')")
    cursor.execute("INSERT INTO machines (serial_no, location, status) VALUES (97246, 'Tixkokob', 'Off')")
    cursor.execute("INSERT INTO machines (serial_no, location, status) VALUES (97247, 'Las Americas 2', 'On')")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_DB()
    add_values()