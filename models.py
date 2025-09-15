from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="welcomer")  # 'admin' or 'welcomer'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)  # Phone number for contact

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    welcomer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)

    welcomer = db.relationship("User", backref="assignments")
    member = db.relationship("Member", backref="assigned_to")

class Checkoff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    welcomer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    week_key = db.Column(db.String(16), nullable=False)  # e.g., "2025-W38"
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    welcomer = db.relationship("User", backref="checkoffs")
    member = db.relationship("Member", backref="checkoffs")
    __table_args__ = (db.UniqueConstraint("welcomer_id", "member_id", "week_key", name="uq_checkoff_week"),)

class WeeklyTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week_key = db.Column(db.String(16), unique=True, nullable=False)  # e.g., "2025-W38"
    topic = db.Column(db.String(200), nullable=False)
    bible_verse_ref = db.Column(db.String(200), nullable=True)  # e.g., "John 3:16"
    bible_verse_text = db.Column(db.Text, nullable=True)  # Full verse text
    question = db.Column(db.Text, nullable=False)
    activity = db.Column(db.Text, nullable=True)  # Optional activity for the week
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
