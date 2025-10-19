from App.database import db
from App.models.user import User

class Employer(User):
    __tablename__ = 'employers'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    internships = db.relationship('Internship', backref='employer', lazy=True)
    __mapper_args__ = {
      'polymorphic_identity': 'employer',
    }

    def __init__(self, company_name, password):
        self.name = company_name
        self.set_password(password)
        self.user_type = 'employer'

    # --- Lookups ---
    @classmethod
    def by_name(cls, comapny_name: str):
        return cls.query.filter_by(comapny_name=comapny_name).first()

    # --- Domain behavior (business rules) ---
    def __repr__(self):
        return f'<Employer {self.name}>'
    
    def to_json(self):
        return {
            'id': self.id,
            'company_name': self.name
        }
