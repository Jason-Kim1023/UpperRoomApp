import os

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    # Production-specific settings
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    
    # Ensure we have required environment variables in production
    @classmethod
    def validate(cls):
        if not cls.SECRET_KEY:
            raise ValueError("FLASK_SECRET_KEY environment variable is required")
        if not cls.SQLALCHEMY_DATABASE_URI:
            raise ValueError("DATABASE_URL environment variable is required")
