from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from auth.utils import role_required
from extensions import db
from models import User, Member, Assignment, Checkoff, WeeklyTopic
from week import current_week_key

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")

@admin_bp.route("/dashboard")
@role_required("admin")
def dashboard():
    welcomers = User.query.filter_by(role="welcomer").all()
    members = Member.query.all()
    assignments = Assignment.query.all()
    week_key = current_week_key()
    
    # Get current weekly topic
    current_topic = WeeklyTopic.query.filter_by(week_key=week_key).first()
    
    # Add checkoff status to each assignment
    assignments_with_status = []
    for assignment in assignments:
        checked = Checkoff.query.filter_by(
            welcomer_id=assignment.welcomer_id, 
            member_id=assignment.member_id, 
            week_key=week_key
        ).first() is not None
        assignments_with_status.append({
            'assignment': assignment,
            'checked': checked
        })
    
    # Add assignment count to each welcomer
    welcomers_with_counts = []
    for welcomer in welcomers:
        assignment_count = Assignment.query.filter_by(welcomer_id=welcomer.id).count()
        welcomers_with_counts.append({
            'welcomer': welcomer,
            'assignment_count': assignment_count
        })
    
    # Add assignment status to each member
    members_with_status = []
    for member in members:
        assigned = Assignment.query.filter_by(member_id=member.id).first() is not None
        members_with_status.append({
            'member': member,
            'assigned': assigned
        })
    
    return render_template("admin/dashboard.html", 
                         welcomers_with_counts=welcomers_with_counts, 
                         members_with_status=members_with_status, 
                         assignments_with_status=assignments_with_status,
                         week_key=week_key,
                         current_topic=current_topic)

@admin_bp.route("/create-welcomer", methods=["GET","POST"])
@role_required("admin")
def create_welcomer():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"].strip()
        if User.query.filter_by(email=email).first():
            flash("Email already exists", "error")
            return redirect(url_for("admin.create_welcomer"))
        user = User(name=name, email=email, role="welcomer")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Welcomer created", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/create_welcomer.html")

@admin_bp.route("/create-member", methods=["GET","POST"])
@role_required("admin")
def create_member():
    if request.method == "POST":
        name = request.form["name"].strip()
        phone = request.form.get("phone", "").strip()
        m = Member(name=name, phone=phone if phone else None)
        db.session.add(m)
        db.session.commit()
        flash("Member created", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/create_member.html")

@admin_bp.route("/assign", methods=["GET","POST"])
@role_required("admin")
def assign():
    welcomers = User.query.filter_by(role="welcomer").all()
    
    # Get only unassigned members
    assigned_member_ids = [a.member_id for a in Assignment.query.all()]
    unassigned_members = Member.query.filter(~Member.id.in_(assigned_member_ids)).all()
    
    if request.method == "POST":
        welcomer_id = int(request.form["welcomer_id"])
        member_ids = request.form.getlist("member_ids")  # Get multiple member IDs
        
        if not member_ids:
            flash("Please select at least one member.", "error")
            return redirect(url_for("admin.assign"))
        
        assigned_count = 0
        for member_id in member_ids:
            member_id = int(member_id)
            # Avoid duplicate assignment
            existing = Assignment.query.filter_by(welcomer_id=welcomer_id, member_id=member_id).first()
            if not existing:
                db.session.add(Assignment(welcomer_id=welcomer_id, member_id=member_id))
                assigned_count += 1
        
        if assigned_count > 0:
            db.session.commit()
            flash(f"Assigned {assigned_count} member(s).", "success")
        else:
            flash("No new assignments made (all selected members were already assigned).", "info")
        
        return redirect(url_for("admin.dashboard"))
    
    return render_template("admin/assign.html", welcomers=welcomers, unassigned_members=unassigned_members)

@admin_bp.route("/unassign/<int:assignment_id>", methods=["POST"])
@role_required("admin")
def unassign(assignment_id):
    a = Assignment.query.get_or_404(assignment_id)
    db.session.delete(a)
    db.session.commit()
    flash("Unassigned.", "success")
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/delete-member", methods=["GET", "POST"])
@role_required("admin")
def delete_member():
    members = Member.query.all()
    if request.method == "POST":
        member_id = int(request.form["member_id"])
        member = Member.query.get_or_404(member_id)
        
        # Delete all assignments for this member first
        Assignment.query.filter_by(member_id=member_id).delete()
        
        # Delete all checkoffs for this member
        Checkoff.query.filter_by(member_id=member_id).delete()
        
        # Delete the member
        db.session.delete(member)
        db.session.commit()
        flash(f"Member '{member.name}' deleted.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/delete_member.html", members=members)

@admin_bp.route("/delete-welcomer", methods=["GET", "POST"])
@role_required("admin")
def delete_welcomer():
    welcomers = User.query.filter_by(role="welcomer").all()
    if request.method == "POST":
        welcomer_id = int(request.form["welcomer_id"])
        welcomer = User.query.get_or_404(welcomer_id)
        
        # Prevent deleting admin users
        if welcomer.role == "admin":
            flash("Cannot delete admin users.", "error")
            return redirect(url_for("admin.delete_welcomer"))
        
        # Delete all assignments for this welcomer first
        Assignment.query.filter_by(welcomer_id=welcomer_id).delete()
        
        # Delete all checkoffs for this welcomer
        Checkoff.query.filter_by(welcomer_id=welcomer_id).delete()
        
        # Delete the welcomer
        db.session.delete(welcomer)
        db.session.commit()
        flash(f"Welcomer '{welcomer.name}' deleted.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/delete_welcomer.html", welcomers=welcomers)

@admin_bp.route("/set-weekly-topic", methods=["POST"])
@role_required("admin")
def set_weekly_topic():
    week_key = current_week_key()
    topic = request.form["topic"].strip()
    bible_verse_ref = request.form.get("bible_verse_ref", "").strip()
    bible_verse_text = request.form.get("bible_verse_text", "").strip()
    question = request.form["question"].strip()
    activity = request.form.get("activity", "").strip()
    
    if not topic or not question:
        flash("Both topic and question are required.", "error")
        return redirect(url_for("admin.dashboard"))
    
    # Check if topic already exists for this week
    existing_topic = WeeklyTopic.query.filter_by(week_key=week_key).first()
    
    if existing_topic:
        # Update existing topic
        existing_topic.topic = topic
        existing_topic.bible_verse_ref = bible_verse_ref if bible_verse_ref else None
        existing_topic.bible_verse_text = bible_verse_text if bible_verse_text else None
        existing_topic.question = question
        existing_topic.activity = activity if activity else None
        flash("Weekly topic updated.", "success")
    else:
        # Create new topic
        new_topic = WeeklyTopic(
            week_key=week_key, 
            topic=topic, 
            bible_verse_ref=bible_verse_ref if bible_verse_ref else None, 
            bible_verse_text=bible_verse_text if bible_verse_text else None, 
            question=question,
            activity=activity if activity else None
        )
        db.session.add(new_topic)
        flash("Weekly topic set.", "success")
    
    db.session.commit()
    return redirect(url_for("admin.dashboard"))

