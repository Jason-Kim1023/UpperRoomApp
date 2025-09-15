from flask import Flask, render_template, redirect, url_for
from config import Config
from extensions import db, login_manager
from auth.routes import auth_bp
from admin.routes import admin_bp
from welcomer.routes import welcomer_bp
from models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

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
