from App.database import db 
from App.models import Internship, Employer

def belongs_to_employer(internship_id, employer_id):
    internship = Internship.query.get(internship_id)
    if internship:
     return int(internship.employer_id) == int(employer_id)
    return False

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

def get_all_employer_internships(employer_id):
    internships = Internship.query.filter_by(employer_id=employer_id).all()
    return [{'id': internship.id, 
            'title': internship.title, 
            'description': internship.description, 
            'employer_id': internship.employer_id
            } for internship in internships]

def create_internship(employer_id, title, description=''):
    employer = Employer.query.get(employer_id)
    if not employer:
        return False, f'Employer with ID {employer_id} does not exist.'
    if not title or not title.strip():
        return False, "Title cannot be empty."
    
    new_title = title=title.strip() +' ' + f'({employer.name})'
    if Internship.query.filter_by(title= new_title).first():
        return False, f'Internship "{title}" already exists.'
    new_internship = Internship(
        title=title.strip() +' ' + f'({employer.name})',
        description=(description or '').strip(),
        employer_id = employer_id
    )
    db.session.add(new_internship)
    db.session.commit()
    return True, f'Internship "{title}" created by {employer.name}.'

def delete_internship(internship_id):
    internship = Internship.query.get(internship_id)
    if not internship:
        return False, f'Internship with ID {internship_id} does not exist.'
    db.session.delete(internship)
    db.session.commit()
    return True, f'Internship with ID {internship_id} deleted.'

def update_internship_info(internship_id, title=None, description=None):
    internship = Internship.query.filter_by(id=internship_id).first()
    if not internship:
        return False, f'Internship with id "{internship_id}" does not exist.'
    if title:
        new_title = title.strip() + ' ' + f'({internship.employer.name})'
        exising_internship = Internship.query.filter_by(title=new_title).first()
        if internship.id != exising_internship.id if exising_internship else None:
            return False, f'Internship with title "{title}" already exists.'
        internship.title = new_title
    if description:
        internship.description = description
    db.session.commit()
    return True, f'Internship with title "{title}" updated.'