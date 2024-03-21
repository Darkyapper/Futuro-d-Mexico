import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/machine_reg', methods = ['POST'])

def registrar_maquina():
    data = request.json
    serial_no = data.get('validationDefault01')
    status = data.get('validationDefault04')
    location = data.get('validationDefaultUsername')

    conn = sqlite3.connect('baseuno.sqlite')
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO machines (serial_no,status,location) VALUES ({serial_no}, {status}, {location})")
    conn.commit()
    conn.close()

    return jsonify({"message" : "Maquina registrada con exitosamente"})

if __name__ == '__main__':
    app.run(debug=True)