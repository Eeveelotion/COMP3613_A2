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

def update_employer_info(employer_id, new_company_name=None, new_password=None):
    employer = Employer.query.get(employer_id)
    if not employer:
        return False, f'Employer with ID {employer_id} does not exist.'
    if new_company_name:
        if Employer.by_name(new_company_name):
            return False, f'Employer "{new_company_name}" already exists.'
        employer.name = new_company_name
    if new_password:
        employer.set_password(new_password)
    db.session.commit()
    return True, f'Employer with ID {employer_id} updated.'