from flask.ext.appbuilder import Model
from flask.ext.appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey 
from sqlalchemy.orm import relationship
from app import db
"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
        
gsClassStudent = db.Table('gsClassStudent',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('classid', db.Integer, db.ForeignKey('gsClass.id')),
        db.Column('studentid', db.Integer, db.ForeignKey('gsStudent.id'))
        )

class gsUser(db.Model):
    __tablename__ = 'gsUser'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    FirstName = db.Column(db.String(120), index=True, unique=False)
    LastName = db.Column(db.String(120), index=True, unique=False)

    def __repr__(self):
        return '<User %r>' % (self.username)

class gsStudent(db.Model):
    __tablename__ = 'gsStudent'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    username = db.Column(db.String(64), index=True, unique=True)
    FirstName = db.Column(db.String(120), index=True, unique=False)
    LastName = db.Column(db.String(120), index=True, unique=False)
    cohort = db.Column(db.Integer, index=True, unique=False)
    current = db.Column(db.Boolean, default=False)

class gsClass(db.Model):
    __tablename__ = 'gsClass'
    id = db.Column(db.Integer, primary_key=True)
    classCode = db.Column(db.String(64), index=True, unique=False)
    cohort = db.Column(db.Integer, index=True, unique=False)
    teacher = db.Column(db.String(120), index=True, unique=False)
    calendarYear = db.Column(db.Integer, index=True, unique=False)
    students = db.relationship('gsStudent',
            secondary=gsClassStudent,
            primaryjoin=(gsClassStudent.c.classid == id),
            secondaryjoin=(gsClassStudent.c.studentid == gsStudent.id),
            lazy='dynamic')
                                 
class gsClassNote(db.Model):
    __tablename__ = 'gsClassNote'
    Noteid = db.Column(db.Integer, primary_key=True)
    classStudentid = db.Column(db.Integer, db.ForeignKey('gsClassStudent.id'))
    note = db.Column(db.Text, index=False, unique=False)
    value = db.Column(db.Integer, index=False)
    date = db.Column(db.DateTime, index=True)
