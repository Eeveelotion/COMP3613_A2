from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_type =  db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    __mapper_args__ = {'polymorphic_identity': 'user', 'polymorphic_on': user_type}

    def __init__(self, password):
        self.set_password(password)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            'id': self.id,
        }
