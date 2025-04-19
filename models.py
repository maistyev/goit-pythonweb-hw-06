from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    
    students = relationship('Student', back_populates='group')
    
    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"


class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))
    
    group = relationship('Group', back_populates='students')
    grades = relationship('Grade', back_populates='student')
    
    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.first_name} {self.last_name}', group_id={self.group_id})>"


class Teacher(Base):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    
    subjects = relationship('Subject', back_populates='teacher')
    
    def __repr__(self):
        return f"<Teacher(id={self.id}, name='{self.first_name} {self.last_name}')>"


class Subject(Base):
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='SET NULL'), nullable=True)
    
    teacher = relationship('Teacher', back_populates='subjects')
    grades = relationship('Grade', back_populates='subject')
    
    def __repr__(self):
        return f"<Subject(id={self.id}, name='{self.name}', teacher_id={self.teacher_id})>"


class Grade(Base):
    __tablename__ = 'grades'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    grade = Column(Float, nullable=False)
    date_received = Column(DateTime, default=datetime.now, nullable=False)
    
    student = relationship('Student', back_populates='grades')
    subject = relationship('Subject', back_populates='grades')
    
    def __repr__(self):
        return f"<Grade(id={self.id}, student_id={self.student_id}, subject_id={self.subject_id}, grade={self.grade})>"