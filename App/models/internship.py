from App.database import db

class Internship(db.Model):
    __tablename__ = 'internships'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text, default='')
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'), nullable=False)

    shortlist_entries = db.relationship('ShortlistEntry', backref='internship', lazy=True)

    def __init__(self, title, description, employer_id):
        self.title = title
        self.description = description
        self.employer_id = employer_id

    # --- Lookups ---
    @classmethod
    def by_title(cls, title: str):
        return cls.query.filter_by(title=title).first()

    # --- Domain behavior ---
    def __repr__(self):
        return f'<Internship {self.title}>'
