from App.models import Student
from App.database import db

def get_student_by_id(student_id):
    student = Student.query.get(student_id)
    return {'id': student.id, 'name': student.name} if student else None

def get_student_by_name(name):
    student = Student.by_name(name)
    return {'id': student.id, 'name': student.name} if student else None

def get_all_students():
    students =Student.query.all()
    return [{"name": s.name, "id": s.id} for s in students]

def create_student(name, password):
    if Student.by_name(name):
        return False, f'Student "{name}" already exists.'
    student = Student(name=name, password=password)
    db.session.add(student)
    db.session.commit()
    return True, f'Student "{name}" created.'