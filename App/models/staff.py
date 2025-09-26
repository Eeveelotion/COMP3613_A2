from App.database import db

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # --- Lookups ---
    @classmethod
    def by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    # --- Domain behavior ---
    def shortlist_student(self, student, internship):
        """Add a student to an internship shortlist as this staff member."""
        from App.models import ShortlistEntry
        exists = ShortlistEntry.query.filter_by(
            internship_id=internship.id,
            student_id=student.id
        ).first()
        if exists:
            return False, f'{student.name} is already on "{internship.title}" shortlist with status {exists.status}.'

        entry = ShortlistEntry(
            internship_id=internship.id,
            student_id=student.id,
            added_by_staff_id=self.id,
            status="PENDING"
        )
        db.session.add(entry)
        db.session.commit()
        return True, f'Added {student.name} to shortlist for "{internship.title}".'

    def __repr__(self):
        return f'<Staff {self.name}>'
