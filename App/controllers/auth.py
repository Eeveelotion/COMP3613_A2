from flask_jwt_extended import create_access_token, JWTManager

from App.models import User, Staff, Student, Employer
from App.database import db

def jwt_authenticate(name, password):
  user = User.query.filter_by(name=name).first()
  if user and user.check_password(password):
    return create_access_token(identity=str(user.id))
  return None


def setup_jwt(app):
  jwt = JWTManager(app)

  # Always store a string user id in the JWT identity (sub),
  # whether a User object or a raw id is passed.
  @jwt.user_identity_loader
  def user_identity_lookup(identity):
    user_id = getattr(identity, "id", identity)
    return str(user_id) if user_id is not None else None

  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    # Cast back to int primary key
    try:
      user_id = int(identity)
    except (TypeError, ValueError):
      return None
    return db.session.get(User, user_id)

  return jwt