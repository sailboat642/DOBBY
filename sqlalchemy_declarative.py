import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

#######################################
#####       Tables in dobby.db    #####
#######################################

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    hash = Column(String, nullable=False)
 
class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    hash = Column(String, nullable=False)
    filename = Column(String, nullable=False, unique=True)



