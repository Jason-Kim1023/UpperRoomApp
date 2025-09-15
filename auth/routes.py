import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, login_manager
from models import User
from werkzeug.security import generate_password_hash

auth_bp = Blueprint("auth", __name__, template_folder="../templates/auth")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))
            else:
                return redirect(url_for("welcomer.dashboard"))
        flash("Invalid credentials", "error")
    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth_bp.route("/init-admin")
def init_admin():
    # Convenience route to setup an initial admin user from env or defaults.
    email = os.getenv("ADMIN_EMAIL", "admin@example.com").lower()
    password = os.getenv("ADMIN_PASSWORD", "admin123")
    name = "Administrator"
    
    # Debug: Show what environment variables are being read
    debug_info = f"Environment variables:<br>"
    debug_info += f"ADMIN_EMAIL: {os.getenv('ADMIN_EMAIL', 'NOT SET')}<br>"
    debug_info += f"ADMIN_PASSWORD: {os.getenv('ADMIN_PASSWORD', 'NOT SET')}<br>"
    debug_info += f"Using email: {email}<br>"
    debug_info += f"Using password: {password}<br><br>"
    
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(name=name, email=email, role="admin")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        msg = debug_info + f"Created admin {email} with provided password."
    else:
        msg = debug_info + f"Admin {email} already exists."
    return msg
