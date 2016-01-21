from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
gs_class_student = Table('gs_class_student', post_meta,
    Column('classid', Integer),
    Column('studentid', Integer),
    Column('classStudentid', Integer, primary_key=True, nullable=False),
)

gs_student = Table('gs_student', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('FirstName', String(length=120)),
    Column('LastName', String(length=120)),
    Column('cohort', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['gs_class_student'].create()
    post_meta.tables['gs_student'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['gs_class_student'].drop()
    post_meta.tables['gs_student'].drop()
