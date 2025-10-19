from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import (
    belongs_to_employer,
    get_all_employer_internships,
    get_employer_by_id,
    update_internship,
    delete_internship,
    create_internship,
    jwt_required
)

internship_views = Blueprint('internship_views', __name__, template_folder='../templates')

@internship_views.route('/internships/', methods=['GET'])
@jwt_required()
def list_internships():
    employer_id = get_jwt_identity()
    if get_employer_by_id(employer_id) is None:
        return jsonify({"Error": "Unauthorized"}), 403
    internships = get_all_employer_internships(employer_id)
    return jsonify(internships), 200

@internship_views.route('/internship', methods=['POST'])
@jwt_required()
def create_internship():
    employer_id = get_jwt_identity()
    if get_employer_by_id(employer_id) is None:
        return jsonify({"Error": "Unauthorized"}), 403
    data = request.get_json()
    success, message = create_internship(
        employer_id,
        data['title'],
        data.get('description', '')
    )
    status_code = 201 if success else 400
    return jsonify({"message": message}), status_code

@internship_views.route('/internship/<internship_id>', methods=['PUT'])
@jwt_required()
def update_internship(internship_id):
    employer_id = get_jwt_identity()
    if not belongs_to_employer(internship_id, employer_id):
        return jsonify({"Error": "Unauthorized"}), 403
    data = request.get_json()
    success, message = update_internship(data['titel', data['description']])
    status_code = 200 if success else 400
    return jsonify({"message": message}), status_code

@internship_views.route('/internship/<internship_id>', methods=['DELETE'])
@jwt_required()
def delete_internship(internship_id):
    employer_id = get_jwt_identity()
    if not belongs_to_employer(internship_id, employer_id):
        return jsonify({"Error": "Unauthorized"}), 403
    data = request.get_json()
    success, message = delete_internship(internship_id)
    status_code = 200 if success else 400
    return jsonify({"message": message}), status_code