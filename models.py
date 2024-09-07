# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    added_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Item('{self.name}', '{self.quantity}', '{self.added_on}')"
