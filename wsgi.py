import sys
import click
import pytest
from flask.cli import with_appcontext, AppGroup

from App.main import create_app
from App.database import db, get_migrate


from App.models import (
    User,                 
    Employer,
    Staff,
    Student,
    Internship,
    Shortlist,
)


from App.controllers import *


app = create_app()
migrate = get_migrate(app)

# ======================================================================================
# INIT
# ======================================================================================
@app.cli.command("init", help="Drops, recreates, and seeds the database with dummy data")
def init():
    initialize()

# # ======================================================================================
# # USER COMMANDS (template)
# # ======================================================================================
# user_cli = AppGroup('user', help='User object commands (template)')

# @user_cli.command("create", help="Create a basic template user")
# @click.argument("password")
# def user_create( password):
#     create_user(password)
#     print(f'user created')

# @user_cli.command("list", help="List all template users")
# def user_list():
#     users = get_all_users()
#     print([u.toDict() for u in users])

# @user_cli.command("list-json", help="List all template users as JSON")
# def user_list_json():
#     print(get_all_users_json())

# Tests (template-style)
test_cli = AppGroup('test', help='Run tests')

@test_cli.command("all", help="Run all unit tests with pytest")
def run_all_tests():
    sys.exit(pytest.main(["-x", "App/tests"]))

# app.cli.add_command(user_cli)
app.cli.add_command(test_cli)

# ======================================================================================
# Manual creation for Employer / Staff / Student
# ======================================================================================
create_cli = AppGroup('create', help='Manually create role users (Employer/Staff/Student)')

@create_cli.command('employer', help='Create an Employer: flask create employer <name> <password>')
@click.argument('company_name')
@click.argument('password')
def create_new_employer(company_name, password):
    create_employer(company_name, password)

@create_cli.command('staff', help='Create a Staff: flask create staff <name> <password>')
@click.argument('name')
@click.argument('password')
def create_new_staff(name, password):
    create_staff(name, password)

@create_cli.command('student', help='Create a Student: flask create student <name> <password>')
@click.argument('name')
@click.argument('password')
def create_new_student(name, password):
    create_student(name, password)

app.cli.add_command(create_cli)

# ======================================================================================
# Employer CLI — uses model methods directly
# ======================================================================================
employer_cli = AppGroup('employer', help='Employer commands')

@employer_cli.command('create-position', help='Create an internship: flask employer create-position <employer_name> <title> [description]')
@click.argument('employer_name')
@click.argument('title')
@click.argument('description', required=False, default='')
def employer_create_position(employer_name, title, description):
    employer = Employer.by_name(employer_name)
    if not employer:
        print(f'Employer "{employer_name}" not found.')
        return
    ok, msg = employer.create_internship(title, description)
    print(msg)

@employer_cli.command('decide', help='Accept/Reject a student: flask employer decide <employer_name> <internship_title> <student_name> <ACCEPTED|REJECTED>')
@click.argument('employer_name')
@click.argument('internship_title')
@click.argument('student_name')
@click.argument('decision')
def employer_decide(employer_name, internship_title, student_name, decision):
    employer = Employer.by_name(employer_name)
    if not employer:
        print(f'Employer "{employer_name}" not found.')
        return
    internship = Internship.by_title(internship_title)
    if not internship:
        print(f'Internship "{internship_title}" not found.')
        return
    student = Student.by_name(student_name)
    if not student:
        print(f'Student "{student_name}" not found.')
        return
    ok, msg = internship.decide(employer, student, decision)
    print(msg)

app.cli.add_command(employer_cli)

# ======================================================================================
# Staff CLI — uses model methods directly
# ======================================================================================
staff_cli = AppGroup('staff', help='Staff commands')

@staff_cli.command('shortlist', help='Add student to internship shortlist: flask staff shortlist <staff_name> <student_name> <internship_title>')
@click.argument('staff_name')
@click.argument('student_name')
@click.argument('internship_title')
def staff_shortlist(staff_name, student_name, internship_title):
    staff = Staff.by_name(staff_name)
    if not staff:
        print(f'Staff "{staff_name}" not found.')
        return
    student = Student.by_name(student_name)
    if not student:
        print(f'Student "{student_name}" not found.')
        return
    internship = Internship.by_title(internship_title)
    if not internship:
        print(f'Internship "{internship_title}" not found.')
        return
    ok, msg = staff.shortlist_student(student, internship)
    print(msg)

app.cli.add_command(staff_cli)

# ======================================================================================
# Student CLI — uses model methods directly
# ======================================================================================
student_cli = AppGroup('student', help='Student commands')

@student_cli.command('view-shortlist', help='View shortlist: flask student view-shortlist <student_name>')
@click.argument('student_name')
def student_view_shortlist(student_name):
    student = Student.by_name(student_name)
    if not student:
        print(f'Student "{student_name}" not found.')
        return
    items = student.shortlist_summary()
    print(f'Found {len(items)} shortlist item(s) for {student_name}.')
    if not items:
        print('No shortlist entries.')
        return
    for i, row in enumerate(items, start=1):
        print(f'{i}. {row["internship"]} @ {row["employer"]} -> {row["status"]}')

app.cli.add_command(student_cli)
