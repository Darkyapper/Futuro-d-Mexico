import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


file_path = os.path.abspath(os.getcwd()) + '/database/machines.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Aquí se definen las tablas de la base de datos
class Machines(db.Model):
    serial_no = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), nullable=False)

class Report(db.Model):
    id_report = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    serial_no = db.Column(db.Integer, db.ForeignKey('machines.serial_no'), nullable=False)
    machines = relationship('Machines', backref='report')

class Products(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    supplier = db.Column(db.String(100), nullable=False)
    pack_cost = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(10), nullable=False)
    details = db.Column(db.String(100), nullable=False)

class Gains(db.Model):
    profit_id = db.Column(db.Integer, primary_key=True)
    serial_no = db.Column(db.Integer, db.ForeignKey('machines.serial_no'), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    gain_amount = db.Column(db.Integer, nullable=False)
    machines = relationship('Machines', backref='gains')


class Machine_Content(db.Model):
    serial_no = db.Column(db.Integer, db.ForeignKey('machines.serial_no'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    slot_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    action_needed = db.Column(db.Integer, nullable=False)
    machines = relationship('Machines', backref='machine_contents')
    products = relationship('Products', backref='machine_contents')

#Aqupi se definen funciones para filtros unicos
def unique_suppliers(products): #Funcion para obtener los proveedores unicos en Filtros de Consulta_pro
    unique = set()
    for product in products:
        unique.add(product.supplier)
    return unique

def unique_dates(products): #Funcion para obtener las fechas unicas en Filtros de Consulta_pro
    unique = set()
    for product in products:
        unique.add(product.date)
    return unique

@app.before_request
def create_tables():
    db.create_all()

#aquí se definen las rutas para acceder a las páginas
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

@app.route('/productos')
def productos():
    products = Products.query.all()
    return render_template('consulta_pro.html', products=products,unique_suppliers=unique_suppliers,unique_dates=unique_dates)

@app.route('/consult')
def consult():
    gains = Gains.query.all()
    machines= Machines.query.all()
    return render_template('consulta_din.html', gains=gains, machines=machines)

@app.route('/productos/registrar_producto')
def registrar_producto():
    products = Products.query.all()
    return render_template('agregar_prod.html', products=products)

@app.route('/productos/machine_st')
def machine_st():
    machines = Machines.query.all()
    products = Products.query.all()
    machine_contents = Machine_Content.query.all()
    return render_template('status_machines.html', machines=machines, products=products, machine_contents=machine_contents)

#Aquí se definen todas las solicitudes que la página necesite hacer
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

@app.route('/get_machine_contents/<serial_no>', methods=['GET'])
def get_machines_content(serial_no):
    machine_contents = Machine_Content.query.filter_by(serial_no=int(serial_no)).all()
    machine_info = []
    for content in machine_contents:
        machine_info.append({
            'serial_no': content.serial_no,
            'location': content.machines.location,
            'product_id': content.product_id,
            'product_name': content.products.name,
            'slot_id': content.slot_id,
            'quantity': content.quantity,
            'price': content.price,
            'action_needed':"Acción necesaria" if content.action_needed == 1 else "Ninguna"
        })
    return jsonify(machine_info)

if __name__ == '__main__':
    app.run(debug=True, port=4000)
    if not os.path.exists('db.sqlite'):
        db.create_all()