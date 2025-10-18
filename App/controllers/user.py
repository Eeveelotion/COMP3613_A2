from App.models import User
from App.database import db

def create_user( password):
    newuser = User( password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, new_password = None):
    user = User.get.query(id)
    if not user:
        return False, f'User with ID {id} does not exist.'
    if new_password:
        user.set_password(new_password)
    db.session.commit()
    return True, f'User with ID {id} updated.'
