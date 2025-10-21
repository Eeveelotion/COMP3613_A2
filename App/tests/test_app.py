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

def test_authenticate():
    success, message = create_staff("bob", "bobpass")
    success, message = create_student("priyanka", "pringles")
    empsuccess, message = create_employer("buff jezos", "brazil")

    assert jwt_authenticate("bob", "bobpass") != None
    assert jwt_authenticate("priyanka", "pringles") != None
    assert jwt_authenticate("buff jezos", "brazil") != None

    assert jwt_authenticate("buff jezos", "wrongpass") == None

    assert jwt_authenticate("nonexistent", "nopass") == None

def test_get_all_users():
    create_user("jalice", "jalicepass")
    create_user("bobby", "bobbypass")
    users = get_all_users()
    names = [user['name'] for user in users]
    assert "jalice" in names and "bobby" in names

def test_add_duplicate_user():
    success, message = create_staff("bob", "notbobpass")
    user1 = get_staff_by_name("bob")
    assert success is False
    assert user1 is not None

def test_update_user():
    staff = get_staff_by_name("bob")
    student = get_student_by_name("priyanka")
    employer = get_employer_by_name("buff jezos")

    success_staff, msg_staff = update_user(staff["id"], new_name="robert", new_password="robpass")
    success_student, msg_student = update_user(student["id"], new_name="dill", new_password="pickles")
    success_employer, msg_employer = update_user(employer["id"], new_name="slim pezos", new_password= "not_brazil")

    updated_staff = get_user(staff["id"])
    updated_student = get_user(student["id"])
    updated_employer = get_user(employer["id"])

    assert success_staff == True and success_student == True and success_employer == True
    assert updated_staff.name == "robert" and updated_staff.check_password("robpass")
    assert updated_student.name == "dill" and updated_student.check_password("pickles")
    assert updated_employer.name == "slim pezos" and updated_employer.check_password("not_brazil")

def test_delete_user():
    student_to_delete = get_student_by_name("dill")
    employer_to_delete = get_employer_by_name("slim pezos")

    success_student, msg_student = delete_user(student_to_delete["id"])
    success_employer, msg_employer = delete_user(employer_to_delete["id"])

    assert success_student == success_employer == True
    assert get_user(student_to_delete["id"]) == None
    assert get_user(employer_to_delete["id"]) == None

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

def test_get_all_employer_internships():
    employer = get_employer_by_name("employer1")
    success, message = create_internship(employer["id"], "Internship2", "Description1")
    internships = get_all_employer_internships(employer["id"])
    assert len(internships) == 2
    assert internships[0]['title'] == "Internship1 (employer1)"
    assert internships[1]['title'] == "Internship2 (employer1)"

def test_update_internship():
    employer = get_employer_by_name("employer1")
    internships = get_all_employer_internships(employer["id"])
    internship_id = internships[0]['id']
    success, message = update_internship_info(internship_id, title="Internship1 Updated", description="Description1 Updated")
    updated_internship = get_internship_by_id(internship_id)
    assert success == True
    assert updated_internship['title'] == "Internship1 Updated (employer1)"
    assert updated_internship['description'] == "Description1 Updated"

def test_delete_internship():
    employer = get_employer_by_name("employer1")
    success, message = create_internship(employer["id"], "InternshipToDelete", "To be deleted")
    internship = get_internship_by_title("InternshipToDelete (employer1)")
    success, message = delete_internship(internship["id"])
    assert success == True
    assert get_internship_by_id(internship["id"]) == None

def test_shortlist_nonexistent_internship():
    student = get_student_by_name("student1")
    staff = get_staff_by_name("staff1")
    success, message = create_shortlist_position(student["id"], 9999, staff["id"])
    assert success == False
    assert "Internship does not exist" in message

def test_duplicate_shortlist_entry():
    student = get_student_by_name("student1")
    internship = get_internship_by_title("Internship1 Updated (employer1)")
    staff = get_staff_by_name("staff1")
    success, message = create_shortlist_position(student["id"], internship["id"], staff["id"])
    internship_shortlist = get_shortlist_by_internship(internship["id"])
    assert success == False
    assert len(internship_shortlist) == 1

def test_delete_shortlist_postion():
    student = get_student_by_name("student1")
    internship = get_internship_by_title("Internship1 Updated (employer1)")
    shortlist_entry = get_shortlist_by_student_and_internship(student["id"], internship["id"])
    success, message = delete_shortlist_position(shortlist_entry["id"])
    assert success == True
    assert get_shortlist_by_id(shortlist_entry["id"]) is None
