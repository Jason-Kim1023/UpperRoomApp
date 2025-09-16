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
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
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
    username = os.getenv("ADMIN_USERNAME", "admin")
    password = os.getenv("ADMIN_PASSWORD", "admin123")
    name = "Administrator"
    
    # Debug: Show what environment variables are being read
    debug_info = f"Environment variables:<br>"
    debug_info += f"ADMIN_USERNAME: {os.getenv('ADMIN_USERNAME', 'NOT SET')}<br>"
    debug_info += f"ADMIN_PASSWORD: {os.getenv('ADMIN_PASSWORD', 'NOT SET')}<br>"
    debug_info += f"Using username: {username}<br>"
    debug_info += f"Using password: {password}<br><br>"
    
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(name=name, username=username, role="admin")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        msg = debug_info + f"Created admin {username} with provided password."
    else:
        msg = debug_info + f"Admin {username} already exists."
    return msg
