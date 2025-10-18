from App.models import Employer
from App.database import db

def get_employer_by_id(employer_id):
    return Employer.query.get(employer_id)

def get_employer_by_name(company_name):
    return Employer.by_name(company_name)

def get_all_employers():
    return Employer.query.all()

def create_employer(comapny_name, password):
    if Employer.by_name(comapny_name):
        return False, f'Employer "{comapny_name}" already exists.'
    employer = Employer(comapny_name=comapny_name, password='password')
    db.session.add(employer)
    db.session.commit()
    return True, f'Employer "{comapny_name}" created.'

def delete_employer(employer_id):
    employer = Employer.query.get(employer_id)
    if not employer:
        return False, f'Employer with ID {employer_id} does not exist.'
    db.session.delete(employer)
    db.session.commit()
    return True, f'Employer with ID {employer_id} deleted.'

def update_employer_info(employer_id, new_company_name=None, new_password=None):
    employer = Employer.query.get(employer_id)
    if not employer:
        return False, f'Employer with ID {employer_id} does not exist.'
    if new_company_name:
        if Employer.by_name(new_company_name):
            return False, f'Employer "{new_company_name}" already exists.'
        employer.company_name = new_company_name
    if new_password:
        employer.set_password(new_password)
    db.session.commit()
    return True, f'Employer with ID {employer_id} updated.'