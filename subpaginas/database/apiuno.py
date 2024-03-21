import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/machine_reg', methods = ['POST'])

def machine_reg():
    data = request.json
    serial_no = data.get('ValidationDefault01')
    status = data.get('ValidationDefault04')
    location = data.get('ValidationDefaultUsername')

    conn = sqlite3.connect('baseuno.sqlite')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO machines (serial_no,status,location) VALUES (?, ?, ?)", (serial_no, status,location))
    conn.commit()
    conn.close()

    return jsonify({"message" : "Maquina registrada con exitosamente"})

if __name__ == '__main__':
    app.run(debug=True)