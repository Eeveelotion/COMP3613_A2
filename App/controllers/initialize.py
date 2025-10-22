from .user import create_user
from App.database import db
from App.models import Employer, Staff, Student, Internship, Shortlist

from sqlalchemy import event
from sqlalchemy.engine import Engine

def initialize():
    """
    Drops and recreates all tables, then seeds basic data.
    Keeps your original demo user from user.py (bob/bobpass).
    """
    db.drop_all()
    db.create_all()

    # --- Employers ---
    e1 = Employer(name='Umbrella Corporation', password='pass')
    e2 = Employer(name='Vault-Tec',   password='pass')

    # --- Staff ---
    s1 = Staff(name='Alice', password='pass')
    s2 = Staff(name='Bob',   password='pass')

    # --- Students ---
    st1 = Student(name='Shania',  password='pass')
    st2 = Student(name='Priyanka',  password='pass')
    st3 = Student(name='Diaz', password='pass')

    db.session.add_all([e1, e2, s1, s2, st1, st2, st3])
    db.session.commit()

    # --- Internships ---
    i1 = Internship(
        title='Backend Intern (Umbrella Corporation)',
        description='Flask + SQLAlchemy basics',
        employer_id=e1.id
    )
    i2 = Internship(
        title='UX Dev Intern (Vault-Tec)',
        description='Development and design of user interfaces',
        employer_id=e2.id
    )

    db.session.add_all([i1, i2])
    db.session.commit()

    shortlist1 = Shortlist(
        internship_id = i1.id,
        student_id = st3.id,
        added_by_staff_id = s1.id
    )

    db.session.add(shortlist1)
    db.session.commit()

    print("Database initialized and seeded with Employers, Staff, Students, and Internships.")

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()