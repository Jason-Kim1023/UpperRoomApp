from flask import Flask, render_template, redirect, url_for
from config import Config, ProductionConfig
from extensions import db, login_manager
import os
from auth.routes import auth_bp
from admin.routes import admin_bp
from welcomer.routes import welcomer_bp
from models import User

def create_app():
    app = Flask(__name__)
    
    # Use ProductionConfig if DATABASE_URL is set (production environment)
    if os.getenv("DATABASE_URL"):
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # Always create tables - this is safe for both SQLite and PostgreSQL
        # For PostgreSQL, this will only create tables if they don't exist
        # For SQLite, this ensures tables are created on first run
        print("Creating/updating database tables...")
        db.create_all()
        print("Database tables ready!")

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(welcomer_bp, url_prefix="/welcomer")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
#hello mini change