import os
from datetime import date, datetime
from flask import Flask
from models import db, User, Transaction, Budget, UpcomingBill

def seed():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        # Find or create demo_user
        user = User.query.filter_by(username='demo_user').first()
        if not user:
            user = User(username='demo_user', email='demo@example.com')
            user.set_password('Password123')
            db.session.add(user)
            db.session.commit()
            print("Created demo_user.")
        else:
            # Clear old transactions, budgets, bills for demo_user to prevent duplicate stacks
            Transaction.query.filter_by(user_id=user.id).delete()
            Budget.query.filter_by(user_id=user.id).delete()
            UpcomingBill.query.filter_by(user_id=user.id).delete()
            db.session.commit()
            print("Cleared old records for demo_user.")

        # Seed budgets for current month (July 2026)
        cur_month = "2026-07"
        budgets = [
            Budget(user_id=user.id, category='Food', amount=400.0, month=cur_month),
            Budget(user_id=user.id, category='Travel', amount=300.0, month=cur_month),
            Budget(user_id=user.id, category='Shopping', amount=200.0, month=cur_month),
            Budget(user_id=user.id, category='all', amount=3000.0, month=cur_month),
        ]
        db.session.add_all(budgets)
        
        # Seed upcoming bills
        bills = [
            UpcomingBill(user_id=user.id, title='Internet Subscription', amount=60.0, due_date=date(2026, 7, 15), category='Bills', is_paid=False),
            UpcomingBill(user_id=user.id, title='Gym Membership', amount=40.0, due_date=date(2026, 7, 18), category='Entertainment', is_paid=False),
            UpcomingBill(user_id=user.id, title='Insurance Premium', amount=150.0, due_date=date(2026, 7, 22), category='Bills', is_paid=False),
        ]
        db.session.add_all(bills)

        # Seed transactions history
        transactions = []
        
        # July 2026 (Current Month)
        transactions.extend([
            Transaction(user_id=user.id, type='income', category='Salary', amount=5000.0, description='Monthly Paycheck', date=date(2026, 7, 1)),
            Transaction(user_id=user.id, type='expense', category='Bills', amount=1200.0, description='Rent/Mortgage Payment', date=date(2026, 7, 1)),
            Transaction(user_id=user.id, type='expense', category='Bills', amount=120.0, description='Electricity Bill', date=date(2026, 7, 3)),
            Transaction(user_id=user.id, type='expense', category='Food', amount=150.0, description='Weekly Grocery Shopping', date=date(2026, 7, 2)),
            Transaction(user_id=user.id, type='expense', category='Food', amount=85.0, description='Restaurant Team Dinner', date=date(2026, 7, 5)),
            Transaction(user_id=user.id, type='expense', category='Travel', amount=60.0, description='Gas Station Refuel', date=date(2026, 7, 4)),
            Transaction(user_id=user.id, type='expense', category='Travel', amount=350.0, description='Flight Tickets (Holiday)', date=date(2026, 7, 8)),
            Transaction(user_id=user.id, type='expense', category='Shopping', amount=180.0, description='Amazon purchase - Electronics', date=date(2026, 7, 6)),
            Transaction(user_id=user.id, type='expense', category='Entertainment', amount=40.0, description='Cinema & Snacks', date=date(2026, 7, 7)),
            Transaction(user_id=user.id, type='expense', category='Other', amount=25.0, description='Starbucks Coffee', date=date(2026, 7, 2)),
        ])

        # June 2026
        transactions.extend([
            Transaction(user_id=user.id, type='income', category='Salary', amount=5000.0, description='Monthly Paycheck', date=date(2026, 6, 1)),
            Transaction(user_id=user.id, type='expense', category='Bills', amount=1320.0, description='Rent & Bills', date=date(2026, 6, 1)),
            Transaction(user_id=user.id, type='expense', category='Food', amount=300.0, description='Food & Groceries', date=date(2026, 6, 10)),
            Transaction(user_id=user.id, type='expense', category='Travel', amount=200.0, description='Travel & Gas', date=date(2026, 6, 15)),
            Transaction(user_id=user.id, type='expense', category='Entertainment', amount=150.0, description='Concert Ticket', date=date(2026, 6, 20)),
            Transaction(user_id=user.id, type='expense', category='Shopping', amount=400.0, description='Summer Shopping', date=date(2026, 6, 25)),
        ])

        # May 2026
        transactions.extend([
            Transaction(user_id=user.id, type='income', category='Salary', amount=4800.0, description='Monthly Paycheck', date=date(2026, 5, 1)),
            Transaction(user_id=user.id, type='expense', category='Bills', amount=1320.0, description='Rent & Bills', date=date(2026, 5, 1)),
            Transaction(user_id=user.id, type='expense', category='Food', amount=280.0, description='Food & Groceries', date=date(2026, 5, 12)),
            Transaction(user_id=user.id, type='expense', category='Travel', amount=150.0, description='Travel Expenses', date=date(2026, 5, 18)),
            Transaction(user_id=user.id, type='expense', category='Entertainment', amount=80.0, description='Movies & Bowling', date=date(2026, 5, 22)),
            Transaction(user_id=user.id, type='expense', category='Shopping', amount=250.0, description='Malls & Clothing', date=date(2026, 5, 28)),
        ])

        # April 2026
        transactions.extend([
            Transaction(user_id=user.id, type='income', category='Salary', amount=4800.0, description='Monthly Paycheck', date=date(2026, 4, 1)),
            Transaction(user_id=user.id, type='expense', category='Bills', amount=1320.0, description='Rent & Bills', date=date(2026, 4, 1)),
            Transaction(user_id=user.id, type='expense', category='Food', amount=310.0, description='Food & Groceries', date=date(2026, 4, 11)),
            Transaction(user_id=user.id, type='expense', category='Travel', amount=180.0, description='Travel Expenses', date=date(2026, 4, 16)),
            Transaction(user_id=user.id, type='expense', category='Entertainment', amount=110.0, description='Subscriptions & Diners', date=date(2026, 4, 21)),
            Transaction(user_id=user.id, type='expense', category='Shopping', amount=320.0, description='Home Decors', date=date(2026, 4, 27)),
        ])

        # March 2026
        transactions.extend([
            Transaction(user_id=user.id, type='income', category='Salary', amount=4800.0, description='Monthly Paycheck', date=date(2026, 3, 1)),
            Transaction(user_id=user.id, type='expense', category='Bills', amount=1320.0, description='Rent & Bills', date=date(2026, 3, 1)),
            Transaction(user_id=user.id, type='expense', category='Food', amount=290.0, description='Food & Groceries', date=date(2026, 3, 9)),
            Transaction(user_id=user.id, type='expense', category='Travel', amount=220.0, description='Travel Expenses', date=date(2026, 3, 14)),
            Transaction(user_id=user.id, type='expense', category='Entertainment', amount=60.0, description='Subscriptions', date=date(2026, 3, 22)),
            Transaction(user_id=user.id, type='expense', category='Shopping', amount=190.0, description='Books & Stationery', date=date(2026, 3, 29)),
        ])

        # February 2026
        transactions.extend([
            Transaction(user_id=user.id, type='income', category='Salary', amount=4800.0, description='Monthly Paycheck', date=date(2026, 2, 1)),
            Transaction(user_id=user.id, type='expense', category='Bills', amount=1320.0, description='Rent & Bills', date=date(2026, 2, 1)),
            Transaction(user_id=user.id, type='expense', category='Food', amount=270.0, description='Food & Groceries', date=date(2026, 2, 8)),
            Transaction(user_id=user.id, type='expense', category='Travel', amount=120.0, description='Travel Expenses', date=date(2026, 2, 14)),
            Transaction(user_id=user.id, type='expense', category='Entertainment', amount=90.0, description='Theatre tickets', date=date(2026, 2, 19)),
            Transaction(user_id=user.id, type='expense', category='Shopping', amount=450.0, description='Electronics Shopping', date=date(2026, 2, 24)),
        ])

        db.session.add_all(transactions)
        db.session.commit()
        print("Successfully seeded all transactions, budgets, and upcoming bills for demo_user.")

if __name__ == '__main__':
    seed()
