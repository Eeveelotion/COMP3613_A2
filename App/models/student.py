from App.database import db

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    shortlist_entries = db.relationship('ShortlistEntry', backref='student', lazy=True)

    # --- Lookups ---
    @classmethod
    def by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    # --- Domain behavior ---
    def shortlist_summary(self):
        """Return a list of dicts: [{internship, employer, status}, ...]."""
        from App.models import ShortlistEntry, Internship, Employer
        q = (db.session.query(
                ShortlistEntry.status.label('status'),
                Internship.title.label('title'),
                Employer.name.label('employer_name'))
             .join(Internship, ShortlistEntry.internship_id == Internship.id)
             .join(Employer, Internship.employer_id == Employer.id)
             .filter(ShortlistEntry.student_id == self.id))
        rows = q.all()
        return [{'internship': r.title, 'employer': r.employer_name, 'status': r.status} for r in rows]

    def __repr__(self):
        return f'<Student {self.name}>'
