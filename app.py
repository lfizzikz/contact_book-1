import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///contacts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev"

db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        number = request.form.get("number", "").strip()

        if name:
            new_contact = Contact(name=name, email=email, phone=number)
            db.session.add(new_contact)
            db.session.commit()
        return redirect(url_for("index"))
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template("index.html", contacts=contacts)


@app.route("/contacts/<int:contact_id>/edit", methods=["GET", "POST"])
def edit_contact(contact_id: int):
    contact = db.session.get(Contact, contact_id)
    if not contact:
        return redirect(url_for("index"))
    if request.method == "POST":
        contact.name = request.form["name"].strip()
        contact.email = request.form.get("email", "").strip() or None
        contact.number = request.form.get("number", "").strip() or None
        db.session.commit()
        return redirect(url_for("index"))

    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template("index.html", contacts=contacts, editing_id=contact.id)


@app.route("/contacts/<int:contact_id>/delete", methods=["POST"])
def delete_contact(contact_id: int):
    contact = db.session.get(Contact, contact_id)
    if contact is not None:
        db.session.delete(contact)
        db.session.commit()
    return redirect(url_for("index"))


# TODO add in ability to edit contacts from homepage
# TODO: flash messages: show "added/updated/deleted" with flask.flash
# TODO: timestamps: add "updated_at"
# TODO: add soft delete, "is_archived"
# TODO: add in tags/groups to contacts
# TODO: Search: search by name/email/phone/tag
# TODO: duplicate detection
# TODO: Notes field per contact
# TODO: Auth: simple login - per user contacts
