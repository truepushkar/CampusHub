from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
SECRET_KEY = os.getenv("SECRET_KEY", "devsecret")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

client = MongoClient(MONGO_URI)
db = client["campushub"]

# Collections
events_col = db["events"]
notices_col = db["notices"]
complaints_col = db["complaints"]
attendance_col = db["attendance"]
clubs_col = db["clubs"]
feedback_col = db["feedback"]

# Helper
def to_json(doc):
    doc["_id"] = str(doc["_id"])
    return doc

def is_admin():
    return session.get("is_admin") is True

@app.route("/")
def index():
    events = list(events_col.find().sort("created_at", -1).limit(5))
    notices = list(notices_col.find().sort("created_at", -1).limit(5))
    return render_template("index.html", events=events, notices=notices)

# ---------- AUTH ROUTES ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin_dashboard"))
        return render_template("login.html", error="Invalid password")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/admin")
def admin_dashboard():
    if not is_admin():
        return redirect(url_for("login"))
    # load some recent docs
    events = list(events_col.find().sort("created_at", -1).limit(5))
    notices = list(notices_col.find().sort("created_at", -1).limit(5))
    complaints = list(complaints_col.find().sort("created_at", -1).limit(5))
    return render_template("admin.html", events=events, notices=notices, complaints=complaints)

# ---------- PUBLIC PAGES ----------
@app.route("/events")
def events_page():
    events = list(events_col.find().sort("date", 1))
    return render_template("events.html", events=events, admin=is_admin())

@app.route("/notices")
def notices_page():
    notices = list(notices_col.find().sort("created_at", -1))
    return render_template("notices.html", notices=notices, admin=is_admin())

@app.route("/complaints")
def complaints_page():
    complaints = list(complaints_col.find().sort("created_at", -1))
    return render_template("complaints.html", complaints=complaints, admin=is_admin())

@app.route("/clubs")
def clubs_page():
    clubs = list(clubs_col.find().sort("created_at", -1))
    return render_template("clubs.html", clubs=clubs, admin=is_admin())

@app.route("/attendance")
def attendance_page():
    records = list(attendance_col.find().sort("date", -1).limit(50))
    return render_template("attendance.html", records=records, admin=is_admin())

@app.route("/feedback")
def feedback_page():
    feedbacks = list(feedback_col.find().sort("created_at", -1))
    return render_template("feedback.html", feedbacks=feedbacks, admin=is_admin())

# ---------- API ROUTES (require admin for POST/DELETE) ----------
@app.route("/api/events", methods=["GET", "POST"])
def api_events():
    if request.method == "GET":
        return jsonify([to_json(e) for e in events_col.find().sort("date", 1)])
    if not is_admin():  # 👈 restrict
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json or request.form
    event = {
        "title": data.get("title"),
        "description": data.get("description"),
        "location": data.get("location"),
        "date": data.get("date"),
        "created_at": datetime.utcnow()
    }
    res = events_col.insert_one(event)
    event["_id"] = str(res.inserted_id)
    return jsonify(event), 201

@app.route("/api/events/<id>", methods=["DELETE"])
def api_event_delete(id):
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403
    events_col.delete_one({"_id": ObjectId(id)})
    return jsonify({"status": "deleted"})

@app.route("/api/notices", methods=["GET", "POST"])
def api_notices():
    if request.method == "GET":
        return jsonify([to_json(n) for n in notices_col.find().sort("created_at", -1)])
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json or request.form
    notice = {
        "title": data.get("title"),
        "body": data.get("body"),
        "audience": data.get("audience", "all"),
        "created_at": datetime.utcnow()
    }
    res = notices_col.insert_one(notice)
    notice["_id"] = str(res.inserted_id)
    return jsonify(notice), 201

@app.route("/api/notices/<id>", methods=["DELETE"])
def api_notice_delete(id):
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403
    notices_col.delete_one({"_id": ObjectId(id)})
    return jsonify({"status": "deleted"})

@app.route("/api/complaints", methods=["GET", "POST"])
def api_complaints():
    if request.method == "GET":
        return jsonify([to_json(c) for c in complaints_col.find().sort("created_at", -1)])
    # students can submit complaints without login
    data = request.json or request.form
    comp = {
        "user": data.get("user"),
        "category": data.get("category"),
        "title": data.get("title"),
        "description": data.get("description"),
        "status": "open",
        "created_at": datetime.utcnow(),
        "updates": []
    }
    res = complaints_col.insert_one(comp)
    comp["_id"] = str(res.inserted_id)
    return jsonify(comp), 201

@app.route("/api/complaints/<id>/resolve", methods=["POST"])
def api_complaint_resolve(id):
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json or request.form
    update = data.get("update", "Resolved by admin")
    complaints_col.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "resolved"},
         "$push": {"updates": {"text": update, "at": datetime.utcnow()}}}
    )
    return jsonify({"status": "resolved"})

@app.route("/api/attendance", methods=["GET", "POST"])
def api_attendance():
    if request.method == "GET":
        return jsonify([to_json(r) for r in attendance_col.find().sort("date", -1)])
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json or request.form
    rec = {
        "student_id": data.get("student_id"),
        "student_name": data.get("student_name"),
        "date": data.get("date", datetime.utcnow().strftime("%Y-%m-%d")),
        "status": data.get("status", "present"),
        "created_at": datetime.utcnow()
    }
    res = attendance_col.insert_one(rec)
    rec["_id"] = str(res.inserted_id)
    return jsonify(rec), 201

@app.route("/api/clubs", methods=["GET", "POST"])
def api_clubs():
    if request.method == "GET":
        return jsonify([to_json(c) for c in clubs_col.find().sort("created_at", -1)])
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json or request.form
    club = {
        "name": data.get("name"),
        "description": data.get("description"),
        "members": data.get("members", "").split(",") if data.get("members") else [],
        "posts": [],
        "created_at": datetime.utcnow()
    }
    res = clubs_col.insert_one(club)
    club["_id"] = str(res.inserted_id)
    return jsonify(club), 201

@app.route("/api/feedback", methods=["GET", "POST"])
def api_feedback():
    if request.method == "GET":
        return jsonify([to_json(f) for f in feedback_col.find().sort("created_at", -1)])
    # anyone can post feedback
    data = request.json or request.form
    f = {
        "user": data.get("user"),
        "type": data.get("type", "general"),
        "text": data.get("text"),
        "created_at": datetime.utcnow()
    }
    res = feedback_col.insert_one(f)
    f["_id"] = str(res.inserted_id)
    return jsonify(f), 201

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
