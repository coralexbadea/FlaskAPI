from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import ComplexEncoder, Note
from sqlalchemy.sql import func
from . import db
import json

views = Blueprint('views', __name__)


@views.route('', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.get_json()

        if len(note) < 1:
            return "short note"
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            return "added note"

    notes = current_user.notes
    return json.dumps([note.jsonify() for note in notes], cls=ComplexEncoder)

@views.route('/<int:nid>', methods=['DELETE'])
def delete_note(nid):
    noteId = nid
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return f"deleted note {noteId}"


@views.route("/<int:nid>", methods=["PUT"])
def edit_note(nid):
    newNote = request.get_json()
    newText = newNote["data"]
    note = Note.query.get(nid)
    if note:
        if note.user_id == current_user.id:
            note.data = newText
            note.date = func.now()
            db.session.commit()
            return f"Modified note with id {nid}"
        else:
            return "You don't have permission to modify this note."
    else:
        return "An error occured"
    

