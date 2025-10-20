import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import *


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.name == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.to_json()
        self.assertDictEqual(user_json, {"id":None, "name": "bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)


'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

def test_authenticate():
    user = create_user("bob", "bobpass")
    assert jwt_authenticate("bob", "bobpass") != None

def test_create_staff():
    success, message = create_staff("staff1", "staffpass")
    staff = get_staff_by_name("staff1")
    assert success == True
    assert staff["name"] == "staff1" and is_staff(staff["id"]) == True

def test_create_student():
    success, message = create_student("student1", "studentpass")
    student = get_student_by_name("student1")
    assert success == True
    assert student["name"] == "student1" and is_student(student["id"]) == True

def test_create_employer():
    success, message = create_employer("employer1", "employerpass")
    employer = get_employer_by_name("employer1")
    assert success == True
    assert employer["name"] == "employer1" and is_employer(employer["id"]) == True

def test_get_all_users():
    create_user("jalice", "jalicepass")
    create_user("bobby", "bobbypass")
    users = get_all_users()
    names = [user['name'] for user in users]
    assert "jalice" in names and "bobby" in names

def test_add_duplicate_user():
    user1 = create_user("bobice", "bobicepass")
    user2 = create_user("bobice", "bobicepass2")
    assert user1 is not None
    assert user2 is None

def test_update_user():
    new_user = create_user("rob", "robpass")
    success, msg = update_user(new_user.id, new_name="robert", new_password="newpass")
    assert success == True
    updated_user = get_user(new_user.id)
    assert updated_user.name == "robert" and updated_user.check_password("newpass")

def test_delete_user():
    new_user = create_user("jane", "janepass")
    success, message = delete_user(new_user.id)
    assert success == True
    assert get_user(new_user.id) == None

def test_delete_staff_user():
    success, message = create_staff("staff2", "staffpass")
    staff = get_staff_by_name("staff2")
    success, message = delete_user(staff["id"])
    assert success == False
    assert "cannot be deleted" in message

def test_create_internship():
    employer = get_employer_by_name("employer1")
    success, message = create_internship(employer["id"], "Internship1", "Description1")
    internships = get_all_employer_internships(employer["id"])
    titles = [internship['title'] for internship in internships]
    descriptons = [internship['description'] for internship in internships]
    assert success == True
    assert "Internship1 (employer1)" in titles
    assert len(internships) == 1
    assert "Description1" in descriptons

def test_create_shortlist_postion():
    staff = get_staff_by_name("staff1")
    student = get_student_by_name("student1")
    internship = get_internship_by_title("Internship1 (employer1)")
    success, message = create_shortlist_position(student["id"], internship["id"], staff["id"])
    shortlist = get_shortlist_by_student_and_internship(student["id"], internship["id"])
    assert success == True
    assert shortlist["student_id"] == student["id"]
    assert shortlist["internship_id"] == internship["id"]
    assert shortlist["added_by_staff_id"] == staff["id"]
    assert shortlist["status"] == "PENDING"

def test_update_shortlist_status():
    student = get_student_by_name("student1")
    internship = get_internship_by_title("Internship1 (employer1)")
    shortlist = get_shortlist_by_student_and_internship(student["id"], internship["id"])
    success, message = update_shortlist_status(shortlist["id"], internship["employer_id"], "ACCEPTED")
    assert success == True
    assert get_shortlist_by_id(shortlist["id"]).status == "ACCEPTED"

def test_get_student_shortlist():
    student = get_student_by_name("student1")
    shortlist = get_shortlist_by_student(student["id"])
    assert len(shortlist) == 1
    assert shortlist[0]["employer"] == "employer1"
    assert shortlist[0]["internship"] == "Internship1 (employer1)"
    assert shortlist[0]["status"] == "ACCEPTED"
