from App.database import db

class ShortlistEntry(db.Model):
    __tablename__ = 'shortlist_entries'
    id = db.Column(db.Integer, primary_key=True)
    internship_id = db.Column(db.Integer, db.ForeignKey('internships.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    added_by_staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    status = db.Column(db.String(20), default="PENDING", nullable=False)

    __table_args__ = (db.UniqueConstraint('internship_id', 'student_id', name='uq_shortlist_unique_pair'),)

    def __repr__(self):
        return f'<Shortlist internship={self.internship_id} student={self.student_id} status={self.status}>'
