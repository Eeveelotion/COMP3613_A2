from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import (
    jwt_authenticate,
    get_all_employers,
    get_all_students,
    create_employer,
    create_student,
    is_staff,
    delete_user,
    update_employer_info,
    update_student_info,
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/auth', methods=['POST'])
def authenticate():
    data = request.get_json()
    access_token = jwt_authenticate(data["name"], data["password"])
    if access_token:
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"Error": "Wrong name or password"}), 401
    
@user_views.route('/users', methods=['GET'])
@jwt_required()
def list_employers():
    if not is_staff(get_jwt_identity()):
        return jsonify({"Error": "Unauthorized"}), 403
    employers = get_all_employers()
    return jsonify(employers), 200

@user_views.route('/students', methods=['GET'])
@jwt_required()
def list_students():
    if not is_staff(get_jwt_identity()):
        return jsonify({"Error": "Unauthorized"}), 403
    students = get_all_students()
    return jsonify(students), 200

@user_views.route('/employer', methods=['POST'])
@jwt_required()
def create_employer():
    data = request.get_json()
    success, message = create_employer(data["name"], data["password"])
    status_code = 201 if success else 400
    return jsonify({"message": message}), status_code

@user_views.route('/student', methods=['POST'])
@jwt_required()
def create_student():
    if not is_staff(get_jwt_identity()):
        return jsonify({"Error": "Unauthorized"}), 403
    data = request.get_json()
    success, message = create_student(data["name"], data["password"])
    status_code = 201 if success else 400
    return jsonify({"message": message}), status_code

@user_views.route('/user', methods=['DELETE'])
@jwt_required()
def remove_user():
    if not is_staff(get_jwt_identity()):
        return jsonify({"Error": "Unauthorized"}), 403
    data = request.get_json()
    success, message = delete_user(data["id"])
    status_code = 200 if success else 404
    return jsonify({"message": message}), status_code

@user_views.route('/employer/<employer_id>', methods=['PUT'])
@jwt_required()
def update_employer(employer_id):
    if not is_staff(get_jwt_identity()):
        return jsonify({"Error": "Unauthorized"}), 403
    data = request.get_json()
    success, message = update_employer_info(employer_id, data.get("new_password"))
    status_code = 200 if success else 404
    return jsonify({"message": message}), status_code

@user_views.route('/student/<student_id>', methods=['PUT'])
@jwt_required()
def update_student(student_id):
    if not is_staff(get_jwt_identity()):
        return jsonify({"Error": "Unauthorized"}), 403
    data = request.get_json()
    success, message = update_student_info(student_id, data.get("new_password"))
    status_code = 200 if success else 404
    return jsonify({"message": message}), status_code