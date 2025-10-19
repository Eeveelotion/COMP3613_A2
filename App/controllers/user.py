from App.models import User, Staff
from App.database import db

def create_user(name, password):
    newuser = User(name = name, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    users = db.session.scalars(db.select(User)).all()
    return [{'user_id': user.id, 'name': user.name, 'user_type': user.user_type} for user in users]

def get_all_users_json():
    users = db.session.scalars(db.select(User)).all()
    if not users:
        return []
    users = [user.to_json() for user in users]
    return users

def update_user(id, new_password = None):
    user = User.get.query(id)
    if not user:
        return False, f'User with ID {id} does not exist.'
    if new_password:
        user.set_password(new_password)
    db.session.commit()
    return True, f'User with ID {id} updated.'

def delete_user(id):
    user = User.query.get(id)
    if Staff.query.get(id):
        return False, f'Cannot delete Staff user with ID {id}.'
    if not user:
        return False, f'User with ID {id} does not exist.'
    db.session.delete(user)
    db.session.commit()
    return True, f'User with ID {id} deleted.'

def is_staff(id):
    user = User.query.get(id)
    return user is not None and user.user_type == "staff"

def is_student(id):
    user = User.query.get(id)
    return user is not None and user.user_type == "student"

def is_employer(id):
    user = User.query.get(id)
    return user is not None and user.user_type == "employer"