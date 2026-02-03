from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    shopper_name = db.Column(db.String(50), nullable=False) # Membre de la famille

    def __repr__(self):
        return f'<Purchase {self.product_name} - {self.price}>'
