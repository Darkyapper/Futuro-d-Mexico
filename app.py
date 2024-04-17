import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlalchemy.orm import relationship
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO

file_path = os.path.abspath(os.getcwd()) + '/database/machines.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#definir acciones
def generar_pdf2(nombre_archivo):
    # Conectar a la base de datos SQLite
    conexion = sqlite3.connect("database/machines.db")
    cursor = conexion.cursor()
    # Obtener los datos de la tabla de reportes
    cursor.execute("SELECT * FROM empty__report")
    datos = cursor.fetchall()
    # Cerrar la conexión a la base de datos
    conexion.close()
    # Crear el documento PDF
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter)
    tabla_datos = []
    # Agregar encabezados de columna a la tabla de datos
    encabezados = ["Report ID", "Serial No", "Location", "Product ID", "Name", "Date", "Status"]
    tabla_datos.append(encabezados)
    # Agregar los datos de la tabla a la tabla de datos
    for fila in datos:
        tabla_datos.append(fila)
    # Crear la tabla con los datos
    tabla = Table(tabla_datos)

    # Estilo de la tabla
    estilo_tabla = TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey),
                               ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                               ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                               ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0,0), (-1,0), 12),
                               ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                               ('GRID', (0,0), (-1,-1), 1, colors.black)])

    tabla.setStyle(estilo_tabla)
    # Agregar la tabla al documento
    elementos = [tabla]
    doc.build(elementos)

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

class Empty_Report(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    serial_no = db.Column(db.Integer, db.ForeignKey('machines.serial_no'), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    products = relationship('Products', backref='empty_report')
    machines = relationship('Machines', backref='empty_report')

#Aqui se definen funciones para filtros unicos
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
    machine_contents = db.session.query(Machine_Content, Machines, Products).\
        join(Machines, Machines.serial_no == Machine_Content.serial_no).\
        join(Products, Products.product_id == Machine_Content.product_id).\
        all()
    return render_template('status_machines.html', machine_contents=machine_contents)

@app.route('/productos/machine_st/reportes')
def report_pro_mac():
    machines = Machines.query.all();
    empty_reports = Empty_Report.query.all()
    return render_template('report_pro_mac.html', machines=machines, empty_reports=empty_reports)

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

@app.route('/get_report_info/<serial_no>', methods=['GET'])
def get_report_info(serial_no):
    ereports = Empty_Report.query.filter_by(serial_no=int(serial_no)).all()
    ereport_info = []
    for ereport in ereports:
        ereport_info.append({
            'report_id': ereport.report_id,
            'serial_no': ereport.machines.serial_no,
            'location': ereport.machines.location,
            'date': ereport.date,
            'status': "Ok" if ereport.status == 1 else "Necesita rellenarse"
        })
    return jsonify(ereport_info)

@app.route('/generar_pdf', methods=['GET'])
def generar_reporte_pdf():
    # Generar el PDF
    nombre_archivo_pdf = "reporte.pdf"
    generar_pdf2(nombre_archivo_pdf)  # Llamada a la función para generar el PDF
    
    # Enviar el PDF como respuesta
    return send_file(nombre_archivo_pdf, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=4000)
    if not os.path.exists('db.sqlite'):
        db.create_all()