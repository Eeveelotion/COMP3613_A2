from App.database import db

class Internship(db.Model):
    __tablename__ = 'internships'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text, default='')
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id', ondelete='CASCADE'), nullable=False)

    shortlist_entries = db.relationship(
        'Shortlist', 
        backref='internship', 
        cascade='all, delete',
        passive_deletes=True,
        lazy=True
    )

    def __init__(self, title, description, employer_id):
        self.title = title
        self.description = description
        self.employer_id = employer_id

    # --- Lookups ---
    @classmethod
    def by_title(cls, title: str):
        return cls.query.filter_by(title=title).first()
