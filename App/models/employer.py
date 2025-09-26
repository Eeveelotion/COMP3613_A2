from App.database import db

class Employer(db.Model):
    __tablename__ = 'employers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    internships = db.relationship('Internship', backref='employer', lazy=True)

    # --- Lookups ---
    @classmethod
    def by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    # --- Domain behavior (business rules) ---
    def create_internship(self, title: str, description: str = ''):
        """Create an internship owned by this employer."""
        from App.models import Internship
        if not title or not title.strip():
            return False, "Title cannot be empty."
        if Internship.query.filter_by(title=title.strip()).first():
            return False, f'Internship "{title}" already exists.'
        job = Internship(
            title=title.strip(),
            description=(description or '').strip(),
            employer_id=self.id
        )
        db.session.add(job)
        db.session.commit()
        return True, f'Internship "{title}" created by {self.name}.'

    def __repr__(self):
        return f'<Employer {self.name}>'
