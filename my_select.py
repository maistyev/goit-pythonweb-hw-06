from sqlalchemy import func, desc, select, and_
from sqlalchemy.orm import Session

from models import Student, Group, Teacher, Subject, Grade
from db import SessionLocal

def select_1():
    """
    Запит 1: Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    """
    session = SessionLocal()
    try:
        # Обчислення середнього балу кожного студента
        subquery = (
            session.query(
                Grade.student_id,
                func.avg(Grade.grade).label('avg_grade')
            )
            .group_by(Grade.student_id)
            .subquery()
        )
        
        result = (
            session.query(
                Student.id,
                Student.first_name,
                Student.last_name,
                subquery.c.avg_grade
            )
            .join(subquery, Student.id == subquery.c.student_id)
            .order_by(desc(subquery.c.avg_grade))
            .limit(5)
            .all()
        )
        
        return result
    finally:
        session.close()

def select_2(subject_id: int):
    """
    Запит 2: Знайти студента із найвищим середнім балом з певного предмета.
    
    Args:
        subject_id: ID предмета
    """
    session = SessionLocal()
    try:
        # Обчислення середнього балу кожного студента з конкретного предмета
        subquery = (
            session.query(
                Grade.student_id,
                func.avg(Grade.grade).label('avg_grade')
            )
            .filter(Grade.subject_id == subject_id)
            .group_by(Grade.student_id)
            .subquery()
        )
        
        result = (
            session.query(
                Student.id,
                Student.first_name,
                Student.last_name,
                Subject.name.label('subject_name'),
                subquery.c.avg_grade
            )
            .join(subquery, Student.id == subquery.c.student_id)
            .join(Grade, Student.id == Grade.student_id)
            .join(Subject, Grade.subject_id == Subject.id)
            .filter(Subject.id == subject_id)
            .order_by(desc(subquery.c.avg_grade))
            .first()
        )
        
        return result
    finally:
        session.close()

def select_3(subject_id: int):
    """
    Запит 3: Знайти середній бал у групах з певного предмета.
    
    Args:
        subject_id: ID предмета
    """
    session = SessionLocal()
    try:
        result = (
            session.query(
                Group.id,
                Group.name,
                func.avg(Grade.grade).label('avg_grade')
            )
            .select_from(Grade)
            .join(Student, Grade.student_id == Student.id)
            .join(Group, Student.group_id == Group.id)
            .filter(Grade.subject_id == subject_id)
            .group_by(Group.id, Group.name)
            .order_by(desc('avg_grade'))
            .all()
        )
        
        return result
    finally:
        session.close()

def select_4():
    """
    Запит 4: Знайти середній бал на потоці (по всій таблиці оцінок).
    """
    session = SessionLocal()
    try:
        result = session.query(func.avg(Grade.grade)).scalar()
        return result
    finally:
        session.close()

def select_5(teacher_id: int):
    """
    Запит 5: Знайти які курси читає певний викладач.
    
    Args:
        teacher_id: ID викладача
    """
    session = SessionLocal()
    try:
        teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            return None
        
        courses = (
            session.query(Subject)
            .filter(Subject.teacher_id == teacher_id)
            .all()
        )
        
        return {
            'teacher': f"{teacher.first_name} {teacher.last_name}",
            'courses': [course.name for course in courses]
        }
    finally:
        session.close()

def select_6(group_id: int):
    """
    Запит 6: Знайти список студентів у певній групі.
    
    Args:
        group_id: ID групи
    """
    session = SessionLocal()
    try:
        result = (
            session.query(
                Student.id,
                Student.first_name,
                Student.last_name,
                Group.name.label('group_name')
            )
            .join(Group, Student.group_id == Group.id)
            .filter(Group.id == group_id)
            .all()
        )
        
        return result
    finally:
        session.close()

def select_7(group_id: int, subject_id: int):
    """
    Запит 7: Знайти оцінки студентів у окремій групі з певного предмета.
    
    Args:
        group_id: ID групи
        subject_id: ID предмета
    """
    session = SessionLocal()
    try:
        result = (
            session.query(
                Student.id,
                Student.first_name,
                Student.last_name,
                Subject.name.label('subject_name'),
                Grade.grade,
                Grade.date_received
            )
            .select_from(Grade)
            .join(Student, Grade.student_id == Student.id)
            .join(Subject, Grade.subject_id == Subject.id)
            .filter(
                Student.group_id == group_id,
                Grade.subject_id == subject_id
            )
            .order_by(Student.last_name, Student.first_name, Grade.date_received)
            .all()
        )
        
        return result
    finally:
        session.close()

def select_8(teacher_id: int):
    """
    Запит 8: Знайти середній бал, який ставить певний викладач зі своїх предметів.
    
    Args:
        teacher_id: ID викладача
    """
    session = SessionLocal()
    try:
        result = (
            session.query(
                Teacher.id,
                Teacher.first_name,
                Teacher.last_name,
                func.avg(Grade.grade).label('avg_grade')
            )
            .select_from(Grade)
            .join(Subject, Grade.subject_id == Subject.id)
            .join(Teacher, Subject.teacher_id == Teacher.id)
            .filter(Teacher.id == teacher_id)
            .group_by(Teacher.id, Teacher.first_name, Teacher.last_name)
            .first()
        )
        
        return result
    finally:
        session.close()

def select_9(student_id: int):
    """
    Запит 9: Знайти список курсів, які відвідує певний студент.
    
    Args:
        student_id: ID студента
    """
    session = SessionLocal()
    try:
        student = session.query(Student).filter(Student.id == student_id).first()
        if not student:
            return None
        
        courses = (
            session.query(Subject.id, Subject.name)
            .join(Grade, Subject.id == Grade.subject_id)
            .filter(Grade.student_id == student_id)
            .group_by(Subject.id, Subject.name)
            .all()
        )
        
        return {
            'student': f"{student.first_name} {student.last_name}",
            'courses': [{'id': course.id, 'name': course.name} for course in courses]
        }
    finally:
        session.close()

def select_10(student_id: int, teacher_id: int):
    """
    Запит 10: Список курсів, які певному студенту читає певний викладач.
    
    Args:
        student_id: ID студента
        teacher_id: ID викладача
    """
    session = SessionLocal()
    try:
        student = session.query(Student).filter(Student.id == student_id).first()
        teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
        
        if not student or not teacher:
            return None
        
        courses = (
            session.query(Subject.id, Subject.name)
            .join(Grade, Subject.id == Grade.subject_id)
            .filter(
                Grade.student_id == student_id,
                Subject.teacher_id == teacher_id
            )
            .group_by(Subject.id, Subject.name)
            .all()
        )
        
        return {
            'student': f"{student.first_name} {student.last_name}",
            'teacher': f"{teacher.first_name} {teacher.last_name}",
            'courses': [{'id': course.id, 'name': course.name} for course in courses]
        }
    finally:
        session.close()

if __name__ == "__main__":
    print("\n\n>>> Топ-5 студентів за середнім балом")
    top_students = select_1()
    for student in top_students:
        print(f"{student.first_name} {student.last_name}: {student.avg_grade:.2f}")
    
    avg_grade = select_4()
    print(f"\n>>> Середній бал на потоці: {avg_grade:.2f}")
    