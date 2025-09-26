from App.database import db

class Internship(db.Model):
    __tablename__ = 'internships'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text, default='')
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'), nullable=False)

    shortlist_entries = db.relationship('ShortlistEntry', backref='internship', lazy=True)

    # --- Lookups ---
    @classmethod
    def by_title(cls, title: str):
        return cls.query.filter_by(title=title).first()

    # --- Domain behavior ---
    def decide(self, employer, student, decision: str):
        """Employer accepts or rejects a student for THIS internship."""
        from App.models import ShortlistEntry
        decision = (decision or '').strip().upper()
        if decision not in ("ACCEPTED", "REJECTED"):
            return False, 'Decision must be "ACCEPTED" or "REJECTED".'
        if self.employer_id != employer.id:
            return False, f'Internship "{self.title}" does not belong to employer "{employer.name}".'

        entry = ShortlistEntry.query.filter_by(
            internship_id=self.id,
            student_id=student.id
        ).first()
        if not entry:
            return False, f'{student.name} is not on the shortlist for "{self.title}".'

        entry.status = decision
        db.session.commit()
        return True, f'{student.name} {decision} for "{self.title}".'

    def __repr__(self):
        return f'<Internship {self.title}>'
