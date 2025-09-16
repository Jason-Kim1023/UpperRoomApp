#!/usr/bin/env python3
"""
Database initialization script for Railway deployment.
Run this after deploying to create the admin user.
"""

import os
from app import create_app
from models import User, db

def init_database():
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        print("✅ Database tables created/verified")
        
        # Create admin user if it doesn't exist
        admin_username = os.getenv("ADMIN_USERNAME", "admin")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        admin_name = "Administrator"
        
        existing_admin = User.query.filter_by(username=admin_username).first()
        
        if not existing_admin:
            admin_user = User(
                name=admin_name,
                username=admin_username,
                role="admin"
            )
            admin_user.set_password(admin_password)
            db.session.add(admin_user)
            db.session.commit()
            print(f"✅ Admin user created: {admin_username}")
        else:
            print(f"✅ Admin user already exists: {admin_username}")
        
        # Show current users
        users = User.query.all()
        print(f"\n📊 Current users in database:")
        for user in users:
            print(f"  - {user.name} ({user.username}) - {user.role}")

if __name__ == "__main__":
    init_database()
