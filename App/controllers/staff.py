from App.models import Staff
from App.database import db

def get_staff_by_id(staff_id):
    staff = Staff.query.get(staff_id)
    return {'id': staff.id, 'name': staff.name} if staff else None

def get_staff_by_name(name):
    staff = Staff.by_name(name)
    return {'id': staff.id, 'name': staff.name} if staff else None

def get_all_staff():
    staff = Staff.query.all()
    return [{"name": s.name, "id": s.id} for s in staff]

def create_staff(name, password):
    if Staff.by_name(name):
        return False, f'Staff member "{name}" already exists.'
    staff = Staff(name=name, password=password)
    db.session.add(staff)
    db.session.commit()
    return True, f'Staff member "{name}" created.'