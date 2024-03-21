import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/subpaginas/database/machine_reg', methods = ['POST'])

def registrar_maquina():
    #data = request.json
    #data.get

    serial_no = request.form.get('validationDefault01')
    status = request.form.get('validationDefault04')
    location = request.form.get('validationDefaultUsername')

    conn = sqlite3.connect('baseuno.sqlite')
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO machines (serial_no,status,location) VALUES ({serial_no}, {status}, {location})")
    conn.commit()
    conn.close()

    return jsonify({"message" : "Maquina registrada exitosamente"})

if __name__ == '__main__':
    app.run(debug=True , port=8000)