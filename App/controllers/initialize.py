from .user import create_user
from App.database import db
from App.models import Employer, Staff, Student, Internship

def initialize():
    """
    Drops and recreates all tables, then seeds basic data.
    Keeps your original demo user from user.py (bob/bobpass).
    """
    db.drop_all()
    db.create_all()

   
    create_user('bob', 'bobpass')

    # --- Employers ---
    e1 = Employer(company_name='Umbrella Corporation', password='pass')
    e2 = Employer(company_name='Vault-Tec',   password='pass')

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
        title='Backend Intern',
        description='Flask + SQLAlchemy basics',
        employer_id=e1.id
    )
    i2 = Internship(
        title='UX Dev Intern',
        description='Development and design of user interfaces',
        employer_id=e2.id
    )

    db.session.add_all([i1, i2])
    db.session.commit()

    print("Database initialized and seeded with Employers, Staff, Students, and Internships.")
