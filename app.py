import os
import sqlite3
from datetime import datetime

from flask import Flask, g, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///contacts.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SECRET_KEY"] = "dev"
#
# db = SQLAlchemy(app)

CONTACTS: list[dict] = []

# class Contact(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), nullable=False)
#     email = db.Column(db.String(255))
#     phone = db.Column(db.String(50))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)


# with app.app_context():
#     db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    # contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        number = request.form.get("number", "").strip()

        if name:
            contact = {
                "id": len(CONTACTS) + 1,
                "name": name,
                "email": email,
                "number": number,
            }
            CONTACTS.append(contact)
        return redirect(url_for("index"))
    return render_template("index.html", contacts=CONTACTS)
