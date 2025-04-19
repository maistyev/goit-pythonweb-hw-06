import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import Session

from db import engine, SessionLocal
from models import Base, Student, Group, Teacher, Subject, Grade

fake = Faker('uk_UA')

def create_groups(session: Session):
    """Створення груп"""
    groups = [
        Group(name="ПЗ-21"),
        Group(name="КІ-22"),
        Group(name="КН-23")
    ]
    session.add_all(groups)
    session.commit()
    return groups

def create_teachers(session: Session):
    """Створення викладачів"""
    teachers = []
    for _ in range(5):
        teacher = Teacher(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email()
        )
        teachers.append(teacher)
    
    session.add_all(teachers)
    session.commit()
    return teachers

def create_subjects(session: Session, teachers):
    """Створення предметів та призначення викладачів"""
    subject_names = [
        "Математичний аналіз", 
        "Програмування", 
        "Алгоритми та структури даних", 
        "Веб-розробка",
        "Бази даних", 
        "Операційні системи", 
        "Комп'ютерні мережі", 
        "Штучний інтелект"
    ]
    
    subjects = []
    for name in subject_names:
        subject = Subject(
            name=name,
            teacher_id=random.choice(teachers).id
        )
        subjects.append(subject)
    
    session.add_all(subjects)
    session.commit()
    return subjects

def create_students(session: Session, groups):
    """Створення студентів"""
    students = []
    for _ in range(40):  # Створення 40 студентів
        group = random.choice(groups)
        student = Student(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            group_id=group.id
        )
        students.append(student)
    
    session.add_all(students)
    session.commit()
    return students

def create_grades(session: Session, students, subjects):
    """Створення оцінок"""
    grades = []
    
    # Генерація дат для оцінок (останні 6 місяців)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)  # Останні 6 місяців
    
    for student in students:
        # Від 10 до 20 оцінок для кожного студента
        num_grades = random.randint(10, 20)
        
        for _ in range(num_grades):
            subject = random.choice(subjects)
            grade_value = random.uniform(60.0, 100.0)  # Оцінки від 60 до 100
            date = fake.date_time_between(start_date=start_date, end_date=end_date)
            
            grade = Grade(
                student_id=student.id,
                subject_id=subject.id,
                grade=round(grade_value, 2),
                date_received=date
            )
            grades.append(grade)
    
    session.add_all(grades)
    session.commit()
    return grades

def seed_data():
    """Головна функція для заповнення бази даних"""
    session = SessionLocal()
    
    try:
        groups = create_groups(session)
        teachers = create_teachers(session)
        subjects = create_subjects(session, teachers)
        students = create_students(session, groups)
        grades = create_grades(session, students, subjects)
        
        print(f"Створено {len(groups)} груп")
        print(f"Створено {len(teachers)} викладачів")
        print(f"Створено {len(subjects)} предметів")
        print(f"Створено {len(students)} студентів")
        print(f"Створено {len(grades)} оцінок")
    
    except Exception as e:
        session.rollback()
        print(f"Помилка під час заповнення бази даних: {e}")
    
    finally:
        session.close()

if __name__ == "__main__":
    # Заповнення бази даних випадковими даними
    seed_data()