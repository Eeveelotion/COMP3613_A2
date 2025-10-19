from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import (
    belongs_to_employer,
    get_shortlist_by_id,
    is_staff,
    is_employer,
    is_student,
    get_shortlist_by_internship,
    get_shortlist_by_student,
    create_shortlist_position,
    delete_shortlist_position,
    update_shortlist_status,
)

shortlist_views = Blueprint('shortlist_views', __name__, template_folder='../templates')

@shortlist_views.route('/shortlist/internship/<internship_id>', methods=['GET'])
@jwt_required()
def get_internship_shortlist(internship_id):
    employer_id = get_jwt_identity()
    if not belongs_to_employer(internship_id, employer_id):
        return jsonify({"Error": "Unauthorized"}), 403
    shortlisted_students = get_shortlist_by_internship(internship_id)
    return jsonify(shortlisted_students), 200

@shortlist_views.route('/shortlist/student/<student_id>', methods=['GET'])
@jwt_required()
def get_student_shortlist(student_id):
    student_id = get_jwt_identity()
    if is_student(student_id) is False:
        return jsonify({"Error": "Unauthorized"}), 403
    shortlisted_positions = get_shortlist_by_student(student_id)
    return jsonify(shortlisted_positions), 200

@shortlist_views.route('/shortlist', methods=['POST'])
@jwt_required()
def create_new_shortlist_position():
    staff_id = get_jwt_identity()
    if is_staff(staff_id) is False:
        return jsonify({"Error": "Unauthorized"}), 403
    data = request.get_json()
    success, message = create_shortlist_position(
        data['student_id'],
        data['internship_id'],
        staff_id
    )
    status_code = 201 if success else 400
    return jsonify({"message": message}), status_code

@shortlist_views.route('/shortlist/<shortlist_id>', methods=['DELETE'])
@jwt_required()
def remove_shortlist_position(shortlist_id):
    staff_id = get_jwt_identity()

    if get_shortlist_by_id(shortlist_id) is None:
        return jsonify({"Error": "Shortlist position not found"}), 404

    if is_staff(staff_id) is None:
        return jsonify({"Error": "Unauthorized"}), 403
    success, message = delete_shortlist_position(shortlist_id)
    status_code = 200 if success else 400
    return jsonify({"message": message}), status_code

@shortlist_views.route('/shortlist/<shortlist_id>', methods=['PUT'])
@jwt_required()
def change_shortlist_status(shortlist_id):
    employer_id = get_jwt_identity()
    if is_employer(employer_id) is False:
        return jsonify({"Error": "Unauthorized"}), 403
    data = request.get_json()
    success, message = update_shortlist_status(
        shortlist_id,
        employer_id,
        data['status']
    )
    status_code = 200 if success else 400
    return jsonify({"message": message}), status_code