__author__ = 'hezhiyu'

from sqlalchemy import BigInteger, Text, DateTime, TIMESTAMP, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column

Base = declarative_base()



class Teacher(Base):

    __tablename__ = 'teacher'
    id = Column(BigInteger, primary_key=True)
    teachername = Column(Text)
    password = Column(Text)


class Student(Base):

    __tablename__ = 'student'
    id = Column(BigInteger, primary_key=True)
    studentname = Column(Text)
    password = Column(Text)


class Lecture(Base):

    __tablename__ = 'lecture'
    id = Column(BigInteger, primary_key=True)
    lecturename = Column(Text)
    tid = Column(BigInteger)
    time = Column(TIMESTAMP)


class Knowledge(Base):

    __tablename__ = 'knowledge'
    id = Column(BigInteger, primary_key=True)
    lid = Column(BigInteger)
    text = Column(Text)
    yes_count = Column(BigInteger)
    no_count = Column(BigInteger)
    is_send = Column(Boolean)


class Question(Base):

    __tablename__ = 'question'
    id = Column(BigInteger, primary_key=True)
    body = Column(Text)
    ans1 = Column(Text)
    ans1_count = Column(BigInteger)
    ans2 = Column(Text)
    ans2_count = Column(BigInteger)
    ans3 = Column(Text)
    ans3_count = Column(BigInteger)
    ans4 = Column(Text)
    ans4_count = Column(BigInteger)
    lid = Column(BigInteger)
    is_send = Column(Boolean)
