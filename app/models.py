from app import db


# class gsUser(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     FirstName = db.Column(db.String(120), index=True, unique=False)
#     LastName = db.Column(db.String(120), index=True, unique=False)
# 
#     def __repr__(self):
#         return '<User %r>' % (self.username)

class gsClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classCode = db.Column(db.String(64), index=True, unique=False)
    cohort = db.Column(db.Integer, index=True, unique=False)
    teacher = db.Column(db.String(120), index=True, unique=False)
    calendarYear = db.Column(db.Integer, index=True, unique=False)
 
#class gsClassStudent(db.Model):
#    classid = db.Column(db.Integer, db.ForeignKey('gsClass.id'))
#    studentid = db.Column(db.Integer, db.ForeignKey('gsStudent.id'))
#    classStudentid = db.Column(db.Integer, primary_key=True)
# 
#class gsStudent(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(64), index=True, unique=True)
#    FirstName = db.Column(db.String(120), index=True, unique=False)
#    LastName = db.Column(db.String(120), index=True, unique=False)
#    cohort = db.Column(db.Integer, index=True, unique=False)
 
# class gsClassNote(db.Model):
#     Noteid = db.Column(db.Integer, primary_key=True)
#     classStudentid = db.Column(db.Integer, db.ForeignKey('gsClassStudent.classid'))
#     note = db.Column(db.Text, index=False, unique=False)
#     value = db.Column(db.Integer, index=False)
#     date = db.Column(db.DateTime, index=True)
