from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import json

class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    def jsonify(self):
        return dict(id=self.id, data=self.data, user=int(self.user_id))
        
user_roles = db.Table('user_roles', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    roles = db.relationship("Role",
                    secondary=user_roles)
    def jsonify(self):
        return dict(first_name=self.first_name, notes=self.notes)
        
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name =  db.Column(db.String(150), unique=True)



class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'jsonify'):
            return obj.jsonify()
        else:
            return json.JSONEncoder.default(self, obj)
