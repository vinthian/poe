from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from poe.config import settings

import os

Base = declarative_base()


class Db(object):
    def __init__(self):
        self.engine = create_engine("sqlite:///%s" % settings["DB_PATH"])

    def clear(self):
        if os.path.exists(settings["DB_PATH"]):
            os.remove(settings["DB_PATH"])
        Base.metadata.create_all(self.engine)

    def init(self):
        Base.metadata.bind = self.engine
        DBSession = sessionmaker()
        DBSession.bind = self.engine
        self.session = DBSession()


class StashTab(Base):
    __tablename__ = "stashtab"

    id = Column(Integer, primary_key=True)
    league = Column(String)
    name = Column(String)
    tab_index = Column(Integer)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    stash_tab = ForeignKey("stashtab.id")

    name = Column(String)
    icon = Column(String)
    type_line = Column(String)

    w = Column(Integer)
    h = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    frame_type = Column(Integer)

    support = Column(Boolean)
    verified = Column(Boolean)
    identified = Column(Boolean)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    return instance if instance else model(**kwargs)
