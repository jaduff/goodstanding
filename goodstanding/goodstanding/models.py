from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Table,
    ForeignKey,
    String,
    Boolean,
    DateTime,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


#class MyModel(Base):
#    __tablename__ = 'models'
#    id = Column(Integer, primary_key=True)
#    name = Column(Text)
#    value = Column(Integer)

gsClassStudent = Table('gsClassStudent',
        Base.metadata,
        Column('id', Integer, primary_key=True),
        Column('classid', Integer, ForeignKey('gsClass.id')),
        Column('studentid', Integer, ForeignKey('gsStudent.id'))
        )

class gsUser(Base):
    __tablename__ = 'gsUser'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    FirstName = Column(String(120), index=True, unique=False)
    LastName = Column(String(120), index=True, unique=False)

    def __repr__(self):
        return '<User %r>' % (self.username)

class gsStudent(Base):
    __tablename__ = 'gsStudent'
    id = Column(Integer, primary_key=True, autoincrement=False)
    username = Column(String(64), index=True, unique=True)
    FirstName = Column(String(120), index=True, unique=False)
    LastName = Column(String(120), index=True, unique=False)
    cohort = Column(Integer, index=True, unique=False)
    current = Column(Boolean, default=False)

class gsClass(Base):
    __tablename__ = 'gsClass'
    id = Column(Integer, primary_key=True)
    classCode = Column(String(64), index=True, unique=False)
    cohort = Column(Integer, index=True, unique=False)
    teacher = Column(String(120), index=True, unique=False)
    calendarYear = Column(Integer, index=True, unique=False)
    students = relationship('gsStudent',
            secondary=gsClassStudent,
            primaryjoin=(gsClassStudent.c.classid == id),
            secondaryjoin=(gsClassStudent.c.studentid == gsStudent.id),
            lazy='dynamic')
                                 
class gsClassNote(Base):
    __tablename__ = 'gsClassNote'
    Noteid = Column(Integer, primary_key=True)
    classStudentid = Column(Integer, ForeignKey('gsClassStudent.id'))
    note = Column(Text, index=False, unique=False)
    value = Column(Integer, index=False)
    date = Column(DateTime, index=True)

#Index('my_index', MyModel.name, unique=True, mysql_length=255)
