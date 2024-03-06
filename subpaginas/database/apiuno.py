import sqlite3, os, time

conn = sqlite3.connect('baseuno.sqlite')
cursor = conn.cursor()

def InsertMachine(SN, ST, LOC): #Insertar maquinas a la base de datos
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

def DeleteMachine(SN): #Borrar maquina de la base de datos
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

def EstadoMaquinaUno(SN): #Ver el estado de una maquina de la base de datos
    cursor.execute(f"SELECT * FROM machines WHERE serial_no = '{SN}'")
    resultado = cursor.fetchone()

    if resultado:
        print("Status: " + resultado[1])
        time.sleep(2)
    else:
        print("Maquina no encontrada.")
        time.sleep(2)
    input()

def EstadoMaquinasTodas(): #Ver el estado de todas las maquinas de la base de datos
    cursor.execute(f"SELECT serial_no, status FROM machines")
    resultado = cursor.fetchall()
    if resultado:
        for serial_no, status in resultado:
            print(f"No machine: {serial_no} ||Status: {status}")
            time.sleep(1)
    else:
        print("Maquinas no encontradas.")
        time.sleep(2)
    input()

def VerReportesTodos(): #Ver todos los reportes
    cursor.execute(f"SELECT no_reporte, detalle, serial_no FROM reportes")
    resultado = cursor.fetchall()

    if resultado:
        for no_reporte, detalle, serial_no in resultado:
            print(f"No Reporte: {no_reporte} ||Descripción: {detalle} ||No Maquina: {serial_no}")
            time.sleep(1)
    else:
        print("No se han encontrado reportes.")
        time.sleep(2)
    input()

def VerReporteUno(RN): #Ver un reporte por codigo
    cursor.execute(f"SELECT * FROM reportes WHERE no_reporte = '{RN}'")
    resultado = cursor.fetchone()

    if resultado:
        print("Status: " + resultado[1])
        time.sleep(2)
    else:
        print("No se han encontrado reportes.")
        time.sleep(2)
    input()

#MAIN - Ejecutor de los comandos principales
e = False
while e == False:
    os.system("cls")
    print("Escoge una opcion para realizar:")
    print("--------CODIGOS MAQUINAS--------")
    print("1.- Insertar una maquina.")
    print("2.- Eliminar una maquina.")
    print("3.- Ver estado de una maquina.")
    print("4.- Ver estado de todas las maquinas.")
    print("---------CODIGOS VENTAS---------")
    print("5.- Ver todos los reportes.")
    print("6.- Ver un reporte.")

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

    elif choose == "4":
        EstadoMaquinasTodas()

    elif choose == "5":
        VerReportesTodos()

    elif choose == "6":
        os.system("cls")
        serialnum = ""

        print("Escribe el Numero del reporte:")
        repornum = int(input())
        VerReporteUno(repornum)

    elif choose == "0":
        break

    else:
        os.system("cls")
        print("Esta no es una opción valida.")