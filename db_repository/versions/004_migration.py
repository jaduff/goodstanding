from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
gs_classes = Table('gs_classes', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('classCode', VARCHAR(length=64)),
    Column('cohort', VARCHAR(length=120)),
    Column('teacher', VARCHAR(length=120)),
    Column('calendarYear', INTEGER),
)

gs_class = Table('gs_class', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('classCode', String(length=64)),
    Column('cohort', String(length=120)),
    Column('teacher', String(length=120)),
    Column('calendarYear', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['gs_classes'].drop()
    post_meta.tables['gs_class'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['gs_classes'].create()
    post_meta.tables['gs_class'].drop()
