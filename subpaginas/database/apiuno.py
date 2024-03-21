import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

conn = sqlite3.connect('baseuno.sqlite')
cursor = conn.cursor()

@app.route('/machine_reg', methods = ['POST'])

def machine_reg():
    data = request.json
    serial_no = data.get('ValidationDefault01')