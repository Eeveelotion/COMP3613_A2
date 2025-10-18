from App.models import Staff
from App.database import db

def get_staff_by_id(staff_id):
    return Staff.query.get(staff_id)

def get_staff_by_name(name):
    return Staff.by_name(name)

def get_all_staff():
    return Staff.query.all()

def create_staff(name, password):
    if Staff.by_name(name):
        return False, f'Staff member "{name}" already exists.'
    staff = Staff(name=name, password=password)
    db.session.add(staff)
    db.session.commit()
    return True, f'Staff member "{name}" created.'

def delete_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        return False, f'Staff member with ID {staff_id} does not exist.'
    db.session.delete(staff)
    db.session.commit()
    return True, f'Staff member with ID {staff_id} deleted.'

def update_staff_info(staff_id, new_name=None, new_password=None):
    staff = Staff.query.get(staff_id)
    if not staff:
        return False, f'Staff member with ID {staff_id} does not exist.'
    if new_name:
        if Staff.by_name(new_name):
            return False, f'Staff member "{new_name}" already exists.'
        staff.name = new_name
    if new_password:
        staff.set_password(new_password)
    db.session.commit()
    return True, f'Staff member with ID {staff_id} updated.'

