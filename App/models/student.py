from App.database import db
from App.models.user import User

class Student(User):
    __tablename__ = 'students'
    name = db.Column(db.String(120), unique=True, nullable=False)

    shortlist_entries = db.relationship('ShortlistEntry', backref='student', lazy=True)
    __mapper_args__ = {
      'polymorphic_identity': 'student',
    }

    def __init__(self, name, password):
        self.name = name
        self.set_password(password)
        self.user_type = 'student'

    # --- Lookups ---
    @classmethod
    def by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    # --- Domain behavior ---
    def __repr__(self):
        return f'<Student {self.name}>'
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }
