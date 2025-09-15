# app/models.py
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    transactions = db.relationship('Transaction', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    # 'type' será 'ingreso' o 'gasto'
    type = db.Column(db.String(10), nullable=False, default='gasto')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Category {self.name}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    # Eliminamos el campo de texto 'category'
    # category = db.Column(db.String(64), nullable=False)
    
    # Y lo reemplazamos con una relación a la nueva tabla
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('transactions', lazy=True))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    month = db.Column(db.Integer, nullable=False) # 1 = Enero, 12 = Diciembre
    year = db.Column(db.Integer, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    category = db.relationship('Category', backref=db.backref('budgets', lazy=True))
    
    # Restricción para que no haya dos presupuestos para la misma categoría/mes/año/usuario
    __table_args__ = (db.UniqueConstraint('user_id', 'category_id', 'year', 'month', name='_user_category_period_uc'),)
