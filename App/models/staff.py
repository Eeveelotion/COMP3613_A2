from App.database import db
from App.models.user import User

class Staff(User):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    __mapper_args__ = {
      'polymorphic_identity': 'staff',
    }

    # --- Lookups ---
    @classmethod
    def by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    # --- Domain behavior ---
    def __init__(self, name, password):
        self.name = name
        self.set_password(password)
        self.user_type = 'staff'

    def __repr__(self):
        return f'<Staff {self.name}>'
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.company_name
        }
