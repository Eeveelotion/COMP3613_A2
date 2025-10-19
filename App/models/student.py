from App.database import db
from App.models.user import User

class Student(User):
    __tablename__ = 'students'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    
    shortlist_entries = db.relationship(
        'Shortlist', 
        backref='student', 
        cascade='all, delete',
        passive_deletes=True,
        lazy=True
    )

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
