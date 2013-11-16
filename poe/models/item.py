import logging

from sqlalchemy import create_engine, Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


logger = logging.getLogger(__name__)

Base = declarative_base()
engine = create_engine("sqlite:///items.db")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    league = Column(String)
    verified = Column(Boolean)
    name = Column(String)
