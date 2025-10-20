from App.database import db

class Shortlist(db.Model):
    __tablename__ = 'shortlist_entries'
    id = db.Column(db.Integer, primary_key=True)
    internship_id = db.Column(db.Integer, db.ForeignKey('internships.id',  ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id',  ondelete='CASCADE'), nullable=False)
    added_by_staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)
    status = db.Column(db.String(20), default="PENDING", nullable=False)

    __table_args__ = (db.UniqueConstraint('internship_id', 'student_id', name='shortlist_unique_pair'),)

