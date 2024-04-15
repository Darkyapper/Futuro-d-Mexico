import sqlite3
import os, time

conexion = sqlite3.connect("../database/machines.db")
conn = conexion.cursor()

debug = False
conection = True
machineid = 97205

conn.execute("""
    SELECT products.product_id, products.name, machine__content.quantity, machine__content.slot_id, machine__content.price
    FROM machine__content
    JOIN products ON machine__content.product_id = products.product_id
    WHERE machine__content.serial_no = ?""", (machineid,))

product_list = []
for row in conn.fetchall():
    product_id = row[0]
    name = row[1]
    quantity = row[2]
    slot_id = row[3]
    cost = row[4]
    product_list.append((product_id, name, quantity, slot_id, cost))

conn.close()


def seleccionar(id):
    os.system('cls')
    producto_seleccionado = None
    for producto in product_list:
        if producto[3] == id:
            if producto[2] > 0:  # Verificar si la cantidad es mayor que 0
                producto_seleccionado = producto
                print("You have selected: {} - ${}".format(producto_seleccionado[1], producto_seleccionado[4]))
                cantidad_ingresada = int(input("Please insert coins: "))
                realizar_pago(producto_seleccionado, cantidad_ingresada)
                time.sleep(1)
                
            else:
                print("ERROR x0001: The selection you made is already sold out! Please choose another product.")
                time.sleep(1)
                break
            break
    if not producto_seleccionado:
        print("ERROR x0002: The selection that you did isn't real! Please enter another code.")
        time.sleep(1)

def realizar_pago(producto_seleccionado, cantidad_ingresada):
    costo_producto = producto_seleccionado[4]
    cambio = cantidad_ingresada - costo_producto
    if cambio >= 0:
        print("Payment successful!")
        if cambio > 0:
            print("Returning change...")
            monedas_devueltas = []
            monedas_disponibles = [10, 5, 2, 1]
            for moneda in monedas_disponibles:
                while cambio >= moneda:
                    monedas_devueltas.append(moneda)
                    cambio -= moneda
            print("Change returned: ", monedas_devueltas)
            time.sleep(1)
            nuevo_stock = producto_seleccionado[2] - 1
            actualizar_stock(producto_seleccionado[0], nuevo_stock)
    else:
        print("ERROR x0004: Insufficient payment! Please insert more coins.")
        time.sleep(1)

def actualizar_stock(producto_id, nuevo_stock):
    conexion = sqlite3.connect("../database/machines.db")
    conn = conexion.cursor()
    conn.execute("UPDATE machine__content SET quantity = ? WHERE product_id = ?", (nuevo_stock, producto_id))
    conexion.commit()
    conexion.close()
    print("Product dropped! Thank you for your purchase.")
    time.sleep(1)

def rellenar_maquina(machineid):
    print("\nRefilling vending machine...")
    slot_id = int(input("Enter the slot ID to refill: "))
    cantidad_nueva = int(input("Enter the quantity to refill: "))

    # Conectar a la base de datos
    conexion = sqlite3.connect("../database/machines.db")
    cursor = conexion.cursor()
    cursor.execute("UPDATE machine__content SET quantity = ? WHERE slot_id = ? AND serial_no = ?",(cantidad_nueva, slot_id, machineid))
    conexion.commit()
    conexion.close()

    print("Slot ID with ID {} successfully refilled with {} units for machine serial number {}.".format(slot_id, cantidad_nueva, machineid))
    time.sleep(1)

while(conection):
    if (debug == False):
        while (conection):
            os.system('cls')
            print("Welcome to the vending machine")
            for producto in product_list:
                print("{} - {} - ${}".format(producto[3], producto[1], producto[4]))
            selection = int(input("Enter a numeric code:"))
            seleccionar(selection)
    elif (debug == True):
        while (conection):
            #os.system('cls')
            print("Welcome to the debug mode of the vending machine")
            idm = machineid
            time.sleep(1)
            print("Analyzing vending machine...")
            productos_agotados = [producto for producto in product_list if producto[2] == 0]
            if productos_agotados:
                print("The following products are sold out:")
                for producto in productos_agotados:
                    print("- {} (Slot ID: {})".format(producto[1], producto[3]))
                    time.sleep(1)
                    print("\nWould you like to refill the vending machine?")
                    opcion = input("Enter '1' to refill or any other key to turn off: ")
                    if opcion.lower() == '1':
                        rellenar_maquina(idm)
                    else:
                        print("Turning off the machine...")
                        debug = False
                        exit()
            else:
                print("No products are sold out.")
                debug = False
                break
    
        