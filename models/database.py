from config.config import db
from datetime import datetime

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id_unique = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    clase = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(150), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    importe = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"Ticket('{self.id}', '{self.fecha}', '{self.clase}', '{self.descripcion}', '{self.cantidad}', '{self.importe}', '{self.total}', '{self.peso}')"
    
    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "clase": self.clase,
            "descripcion": self.descripcion,
            "cantidad": self.cantidad,
            "importe": self.importe,
            "total": self.total,
            "peso": self.peso
            }

        
    
        
    
    
        