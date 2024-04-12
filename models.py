from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Machine(db.Model):
    serial_no = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Machine('{self.serial_no}', '{self.location}', '{self.status}')"