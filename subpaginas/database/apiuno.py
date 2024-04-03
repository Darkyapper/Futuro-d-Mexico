import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

DATABASE_FILE = 'baseuno.sqlite'

def create_conection():
    """Crea una conexión a la base de datos"""
    conn = None;
    try:
        conn = sqlite3.connect(DATABASE_FILE)
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return conn
    
@app.route('/register', methods=['POST'])
def register_machine():
    """Registra una máquina en la base de datos"""
    conn = create_conection()
    if conn is None:
        return jsonify({'error': 'Error al conectar a la base de datos'}), 500
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos incorrectos'}), 400
    
    serial_number = data.get('serialNumber')
    location = data.get('location')
    status = data.get('status')

    if not serial_number or not location or not status:
        return jsonify({'error': 'Datos incorrectos'}), 400
    
    sql = """INSERT INTO (serial_number, location, status) VALUES (?, ?, ?)"""

    try:
        cur = conn.cursor()
        cur.execute(sql, (serial_number, location, status))
        conn.commit()
        return jsonify({'message': 'Máquina registrada correctamente'}), 201
    except sqlite3.Error as e:
        print(f"Error al registrar la máquina: {e}")
        return jsonify({'error': 'Error al registrar la máquina'}), 500
    finally:
        conn.close()
    
    if __name__ == '__main__':
        app.run(debug = True)
