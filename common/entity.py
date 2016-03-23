__author__ = 'hezhiyu'

from sqlalchemy import BigInteger, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column

Base = declarative_base()

'''
class User(Base):

    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    username = Column(Text)
    password = Column(Text)


class Entry(Base):

    __tablename__ = 'entries'
    id = Column(BigInteger, primary_key=True)
    uid = Column(BigInteger)
    title = Column(Text)
    text = Column(Text)
'''


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

    __tablename__ = 'class'
    id = Column(BigInteger, primary_key=True)
    lecturename = Column(Text)
    tid = Column(BigInteger)
    time = Column(DateTime)


class Knowledge(Base):

    __tablename__ = 'knowledge'
    id = Column(BigInteger, primary_key=True)
    cid = Column(BigInteger)
    text = Column(Text)
    yes_count = Column(BigInteger)
    no_count = Column(BigInteger)
