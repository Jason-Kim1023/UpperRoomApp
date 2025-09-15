from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models import Assignment, Member, Checkoff, WeeklyTopic
from week import current_week_key

welcomer_bp = Blueprint("welcomer", __name__, template_folder="../templates/welcomer")

@welcomer_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "welcomer" and current_user.role != "admin":
        return redirect(url_for("auth.login"))
    week_key = current_week_key()
    
    # Get current weekly topic
    current_topic = WeeklyTopic.query.filter_by(week_key=week_key).first()
    
    # List assigned members to this welcomer
    assignments = Assignment.query.filter_by(welcomer_id=current_user.id).all()
    members = []
    for a in assignments:
        m = Member.query.get(a.member_id)
        if not m: 
            continue
        checked = Checkoff.query.filter_by(welcomer_id=current_user.id, member_id=m.id, week_key=week_key).first() is not None
        members.append({"id": m.id, "name": m.name, "phone": m.phone, "checked": checked})
    return render_template("welcomer/dashboard.html", members=members, week_key=week_key, current_topic=current_topic)

@welcomer_bp.route("/check/<int:member_id>")
@login_required
def check(member_id):
    week_key = current_week_key()
    existing = Checkoff.query.filter_by(welcomer_id=current_user.id, member_id=member_id, week_key=week_key).first()
    if not existing:
        c = Checkoff(welcomer_id=current_user.id, member_id=member_id, week_key=week_key)
        db.session.add(c)
        db.session.commit()
    return redirect(url_for("welcomer.dashboard"))

@welcomer_bp.route("/uncheck/<int:member_id>")
@login_required
def uncheck(member_id):
    week_key = current_week_key()
    existing = Checkoff.query.filter_by(welcomer_id=current_user.id, member_id=member_id, week_key=week_key).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
    return redirect(url_for("welcomer.dashboard"))
