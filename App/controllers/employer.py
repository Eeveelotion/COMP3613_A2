from App.models import Employer
from App.database import db

def get_employer_by_id(employer_id):
    employer = Employer.query.get(employer_id)
    return {"id": employer.id, "name": employer.name} if employer else None

def get_employer_by_name(company_name):
    employer = Employer.by_name(company_name)
    return {"id": employer.id, "name": employer.name} if employer else None

def get_all_employers():
    employers = Employer.query.all()
    return [{"id": emp.id, "name": emp.name} for emp in employers]

def create_employer(name, password):
    if Employer.by_name(name):
        return False, f'Employer "{name}" already exists.'
    employer = Employer(name=name, password=password)
    db.session.add(employer)
    db.session.commit()
    return True, f'Employer "{name}" created.'