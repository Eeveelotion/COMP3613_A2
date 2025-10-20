from App.database import db
from App.models.user import User

class Employer(User):
    __tablename__ = 'employers'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    internships = db.relationship(
        'Internship', 
        backref='employer', 
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    
    __mapper_args__ = {
      'polymorphic_identity': 'employer',
    }

    def __init__(self, name, password):
        self.name = name
        self.set_password(password)
        self.user_type = 'employer'

    # --- Lookups ---
    @classmethod
    def by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()