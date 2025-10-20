from App.models import Shortlist, Internship, Employer, Student
from App.database import db

def get_shortlist_by_id(shortlist_id):
    return Shortlist.query.get(shortlist_id)

def get_shortlist_by_student_and_internship(student_id, internship_id):
    shortlist_entry = Shortlist.query.filter_by(
        student_id=student_id,
        internship_id=internship_id
    ).first()

    if not shortlist_entry:
        return None
    return {
        'id': shortlist_entry.id,
        'student_id': shortlist_entry.student_id,
        'internship_id': shortlist_entry.internship_id,
        'added_by_staff_id': shortlist_entry.added_by_staff_id,
        'status': shortlist_entry.status,
    }

def get_shortlist_by_student(student_id):
    shortlisted_positions = (db.session.query(
                Shortlist.id.label('id'),
                Shortlist.status.label('status'),
                Internship.title.label('title'),
                Employer.name.label('employer_name'))
             .join(Internship, Shortlist.internship_id == Internship.id)
             .join(Employer, Internship.employer_id == Employer.id)
             .filter(Shortlist.student_id == student_id))
    return [
            {
                'shortlist id': r.id, 
                'internship': r.title, 
                'employer': r.employer_name, 
                'status': r.status 
            } 
            for r in shortlisted_positions.all()
    ]

def get_shortlist_by_internship(internship_id):
    shortlisted_students = (db.session.query(
                Shortlist.id.label('id'),
                Student.name.label('student_name'),
                Shortlist.status.label('status'))
             .join(Student, Shortlist.student_id == Student.id)
             .filter(Shortlist.internship_id == internship_id))
    return [
            {
                'shortlist id': r.id,
                'student': r.student_name,
                'status': r.status
            }
            for r in shortlisted_students.all()
    ]

def create_shortlist_position(student_id, internship_id, staff_id):
    new_entry = Shortlist(
        student_id=student_id,
        internship_id=internship_id,
        added_by_staff_id=staff_id,
        status="PENDING"
    )
    db.session.add(new_entry)
    try:
        db.session.commit()
        return True, f'Student ID {student_id} shortlisted for Internship ID {internship_id}.'
    except Exception as e:
        db.session.rollback()
        return False, f'Error: Student ID {student_id} is already shortlisted for Internship ID {internship_id}.'

def delete_shortlist_position(shortlist_id):
    entry = Shortlist.query.get(shortlist_id)
    if not entry:
        return False, f'Shortlist entry with ID {shortlist_id} does not exist.'
    db.session.delete(entry)
    db.session.commit()
    return True, f'Shortlist entry with ID {shortlist_id} deleted.'

def update_shortlist_status(shortlist_id, employer_id, new_status):
    entry = Shortlist.query.get(shortlist_id)
    if not entry:
        return False, f'Shortlist entry with ID {shortlist_id} does not exist.'
    if int(entry.internship.employer_id) != int(employer_id):
        return False, f'Employer with ID {employer_id} does not own the internship for this shortlist entry.'
    new_status = (new_status or '').strip().upper()
    if new_status not in ("ACCEPTED", "REJECTED"):
            return False, 'Decision must be "ACCEPTED" or "REJECTED".'
    entry.status = new_status
    db.session.commit()
    return True, f'Shortlist entry with ID {shortlist_id} updated to status {new_status}.'