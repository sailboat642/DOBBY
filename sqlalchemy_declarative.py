import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
 
AppBase = declarative_base()
Base = declarative_base()

#######################################
#####       Tables in dobby.db    #####
#######################################

class User(AppBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    hash = Column(String, nullable=False)
 
class Event(AppBase):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    hash = Column(String, nullable=False)
    filename = Column(String, nullable=False, unique=True)

#########################################
######  Tables in 'event'.db       #######
##########################################
class Committee(Base):
    """Committee Table in 'event'.db"""
    __tablename__ = 'committees' 

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    

class School(Base):
    """School Table in 'event'.db"""
    __tablename__ = 'schools' 

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    delegation_size = Column(Integer)
    grade = Column(Integer, nullable=False)



class Student(Base):
    """Student table"""
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    school_id = Column(Integer, ForeignKey("schools.id"))
    gender = Column(Integer, nullable=True) # 1 if male 0 if female

    school = relationship("School", back_populates="students")

class Portfolio(Base):
    """Portfolio table"""
    __tablename__ = 'portfolios'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    committee_id = Column(Integer, ForeignKey("committees.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"))
    rank = Column(Integer, nullable=False)

    committee = relationship("Committee", back_populates="portfolios")
    student = relationship("Student", back_populates="portfolio")



Committee.portfolios = relationship("Portfolio", order_by=Portfolio.id, back_populates="committee")

School.students = relationship("Student", order_by=Student.id, back_populates="school")

Student.portfolio = relationship("Portfolio", back_populates="student")

