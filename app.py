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

class Report(db.Model):
    id_report = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    serial_no = db.Column(db.Integer, nullable=False)

class Gains(db.Model):
    profit_id = db.Column(db.Integer, primary_key=True)
    serial_no = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    gain_amount = db.Column(db.Integer, nullable=False)

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

@app.route('/reportar_user')
def reportar_user():
    machines = Machines.query.all()  
    return render_template('report_user.html', machines=machines)

@app.route('/reportes')
def reportes():
    reports = Report.query.all()
    return render_template('report_admin.html', reports=reports)

@app.route('/save_machine', methods=['POST'])
def save_machine():
    machines = Machines(serial_no=request.form['serial_no'], location=request.form['location'], status=request.form['status'])
    db.session.add(machines)
    db.session.commit()
    return 'Machine created'

@app.route('/consult')
def consult():
    gains = Gains.query.all()
    machines= Machines.query.all()
    return render_template('consulta_din.html', gains=gains, machines=machines)

@app.route('/delete_machine/<serial_no>')
def delete_machine(serial_no):
    machines = Machines.query.filter_by(serial_no=int(serial_no)).delete()
    db.session.commit()
    return redirect(url_for('registro'))

@app.route('/set_status/<serial_no>')
def set_status(serial_no):
    machines = Machines.query.filter_by(serial_no=int(serial_no)).first()
    if machines:
        machines.status = 'Off' if machines.status == 'On' else 'On'
        db.session.commit()
        return redirect(url_for('registro'))

@app.route('/save_report', methods=['POST'])
def save_report():
    report = Report(description=request.form['description'], date=request.form['date'], serial_no=request.form['serial_no'])
    db.session.add(report)
    db.session.commit()
    return 'Report created'

@app.route('/delete_report/<id_report>')
def delete_report(id_report):
    report = Report.query.filter_by(id_report=int(id_report)).delete()
    db.session.commit()
    return redirect(url_for('reportes'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)
    if not os.path.exists('db.sqlite'):
        db.create_all()