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
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    hash = Column(String, nullable=False)
 
class Events(Base):
    __tablename__ = 'events'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    hash = Column(String, nullable=False)
    address = Column(String, nullable=False, unique=True)



