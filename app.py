import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


file_path = os.path.abspath(os.getcwd()) + '/database/machines.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Machines(db.Model):
    serial_no = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), nullable=False)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/registro')
def registro():
    machines = Machines.query.all()
    return render_template('registrar.html', machines=machines)

@app.route('/save_machine', methods=['POST'])
def save_machine():
    machines = Machines(serial_no=request.form['serial_no'], location=request.form['location'], status=request.form['status'])
    db.session.add(machines)
    db.session.commit()
    return 'Machine created'

@app.route('/delete_machine/<serial_no>')
def delete_machine(serial_no):
    machines = Machines.query.filter_by(serial_no=int(serial_no)).delete()
    db.session.commit()
    return redirect(url_for('registro'))


if __name__ == '__main__':
    app.run(debug=True, port=4000)
    if not os.path.exists('db.sqlite'):
        db.create_all()