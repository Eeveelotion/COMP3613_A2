from App.database import db 
from App.models import Internship, Employer

def get_internship_by_id(internship_id):
    internship = Internship.query.get(internship_id)
    return {'id': internship.id, 
            'title': internship.title, 
            'description': internship.description, 
            'employer_id': internship.employer_id
            } if internship else None
            

def get_internship_by_title(title):
    internship = Internship.by_title(title)
    return {'id': internship.id, 
            'title': internship.title, 
            'description': internship.description, 
            'employer_id': internship.employer_id
            } if internship else None

def create_internship(employer_id, title, description=''):
    employer = Employer.query.get(employer_id)
    if not employer:
        return False, f'Employer with ID {employer_id} does not exist.'
    if not title or not title.strip():
        return False, "Title cannot be empty."
    if Internship.query.filter_by(title= title.strip()).first():
        return False, f'Internship "{title}" already exists.'
    new_internship = Internship(
        title=title.strip() +' ' + f'({employer.company_name})',
        description=(description or '').strip(),
        employer_id = employer_id
    )
    db.session.add(new_internship)
    db.session.commit()
    return True, f'Internship "{title}" created by {employer.company_name}.'

def delete_internship(internship_id):
    internship = Internship.query.get(internship_id)
    if not internship:
        return False, f'Internship with ID {internship_id} does not exist.'
    db.session.delete(internship)
    db.session.commit()
    return True, f'Internship with ID {internship_id} deleted.'

def update_internship(title=None, description=None):
    internship = Internship.query.filter_by(title=title).first()
    if not internship:
        return False, f'Internship with title "{title}" does not exist.'
    if title:
        if Internship.query.filter_by(title=title).first():
            return False, f'Internship with title "{title}" already exists.'
        internship.title = title
    if description is not None:
        internship.description = description
    db.session.commit()
    return True, f'Internship with title "{title}" updated.'