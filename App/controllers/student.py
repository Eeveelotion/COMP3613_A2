from App.models import Student
from App.database import db

def get_student_by_id(student_id):
    return Student.query.get(student_id)

def get_student_by_name(name):
    return Student.by_name(name)

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

def update_student_info(student_id, new_name=None, new_password=None):
    student = Student.query.get(student_id)
    if not student:
        return False, f'Student with ID {student_id} does not exist.'
    if new_name:
        if Student.by_name(new_name) and student.name != new_name:
            return False, f'Student "{new_name}" already exists.'
        student.name = new_name
    if new_password:
        student.set_password(new_password)
    db.session.commit()
    return True, f'Student with ID {student_id} updated.'