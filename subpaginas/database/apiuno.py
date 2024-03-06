import sqlite3, os, time

conn = sqlite3.connect('baseuno.sqlite')
cursor = conn.cursor()

def InsertMachine(SN, ST, LOC):
    cursor.execute(f"SELECT * FROM machines WHERE serial_no = '{SN}'")
    existing_machine = cursor.fetchone()
    
    if existing_machine:
        print("Ya existe una máquina con este número de serie en la base de datos.")
        time.sleep(2)
        return
    else:
        cursor.execute(f"INSERT INTO machines (serial_no,status,location) VALUES ('{SN}','{ST}','{LOC}')")
        conn.commit()
        conn.close()
        print("Maquina registrada exitosamente.")
        time.sleep(2)

def DeleteMachine(SN):
    cursor.execute(f"SELECT * FROM machines WHERE serial_no = '{SN}'")
    existing_machine = cursor.fetchone()

    if existing_machine:
        cursor.execute(f"DELETE FROM machines WHERE serial_no='{SN}'")
        conn.commit()
        print("Maquina borrada exitosamente.")
        time.sleep(2)
    else:
        print("La maquina no existe.")
        time.sleep(2)
        return
    
def EstadoMaquinaUno(SN):
    cursor.execute(f"SELECT * FROM machines WHERE serial_no = '{SN}'")
    resultado = cursor.fetchone()

    if resultado:
        print("Status: " + resultado[1])
        time.sleep(2)
    else:
        print("Maquina no encontrada.")
        time.sleep(2)

e = False
while e == False:
    os.system("cls")
    print("Escoge una opcion para realizar:")
    print("1.- Insertar una maquina.")
    print("2.- Eliminar una maquina.")
    print("3.- Ver estado de una maquina.")
    print("0.- Salir.")

    choose = input()
    if choose == "1":
        os.system("cls")
        serialnum = ""
        status = ""
        location = ""

        print("Escribe el Numero de serie de la maquina:")
        serialnum = int(input())
        print("Escribe el estado actual de la maquina:")
        status = input()
        print("Escribe la ubicación de la maquina:")
        location = input()

        InsertMachine(serialnum, status, location)
    elif choose == "2":
        os.system("cls")
        serialnum = ""

        print("Escribe el Numero de serie de la maquina:")
        serialnum = int(input())
        DeleteMachine(serialnum)
    elif choose  == "3":
        os.system("cls")
        serialnum = ""

        print("Escribe el Numero de serie de la maquina:")
        serialnum = int(input())
        EstadoMaquinaUno(serialnum)
    elif choose == "0":
        break
    else:
        os.system("cls")
        print("Esta no es una opción valida.")