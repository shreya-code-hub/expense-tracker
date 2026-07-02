import sqlite3
import os
from flask import Flask
from models import db

def init_db():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    db_path = 'instance/database.db'
    if os.path.exists(db_path):
        print("Database file found. Migrating users table...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        new_cols = [
            ("profile_pic", "TEXT NULL"),
            ("currency", "VARCHAR(10) NOT NULL DEFAULT '₹'"),
            ("language", "VARCHAR(10) NOT NULL DEFAULT 'en'"),
            ("theme_accent", "VARCHAR(20) NOT NULL DEFAULT 'indigo'"),
            ("daily_reminder", "BOOLEAN NOT NULL DEFAULT 1"),
            ("weekly_summary", "BOOLEAN NOT NULL DEFAULT 1"),
            ("budget_warning_threshold", "FLOAT NOT NULL DEFAULT 90.0"),
            ("savings_milestones", "BOOLEAN NOT NULL DEFAULT 1")
        ]
        
        for col_name, col_type in new_cols:
            try:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name}")
                conn.commit()
                print(f"Added column {col_name} to users table successfully.")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e).lower():
                    # Column already exists, safe to ignore
                    pass
                else:
                    print(f"Warning adding column {col_name}: {e}")
        
        conn.close()

    with app.app_context():
        db.create_all()
        print("Database schema synchronization complete.")

if __name__ == '__main__':
    init_db()
