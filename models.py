from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # Settings & Personalization
    profile_pic = db.Column(db.String(255), nullable=True)
    currency = db.Column(db.String(10), nullable=False, default='₹')
    language = db.Column(db.String(10), nullable=False, default='en')
    theme_accent = db.Column(db.String(20), nullable=False, default='indigo')
    daily_reminder = db.Column(db.Boolean, nullable=False, default=True)
    weekly_summary = db.Column(db.Boolean, nullable=False, default=True)
    budget_warning_threshold = db.Column(db.Float, nullable=False, default=90.0)
    savings_milestones = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='user', lazy=True, cascade="all, delete-orphan")
    budgets = db.relationship('Budget', backref='user', lazy=True, cascade="all, delete-orphan")
    upcoming_bills = db.relationship('UpcomingBill', backref='user', lazy=True, cascade="all, delete-orphan")
    custom_categories = db.relationship('CustomCategory', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    category = db.Column(db.String(50), nullable=False)  # Food, Travel, Shopping, Bills, etc.
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    receipt_image = db.Column(db.String(255))  # Filename/path of receipt image

class Budget(db.Model):
    __tablename__ = 'budgets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Food, Travel, etc. or 'all' for overall
    amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.String(7), nullable=False)  # Format: YYYY-MM

class UpcomingBill(db.Model):
    __tablename__ = 'upcoming_bills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    is_paid = db.Column(db.Boolean, default=False)

class CustomCategory(db.Model):
    __tablename__ = 'custom_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
