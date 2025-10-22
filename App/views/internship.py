from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import (
    get_internship_by_id,
    belongs_to_employer,
    is_employer,
    get_all_employer_internships,
    update_internship_info,
    delete_internship,
    create_internship,
)

internship_views = Blueprint('internship_views', __name__, template_folder='../templates')

@internship_views.route('/internships', methods=['GET'])
@jwt_required()
def list_internships():
    employer_id = get_jwt_identity()
    if is_employer(employer_id) is False:
        return jsonify({"Error": "Unauthorized, only employers allowed"}), 403
    internships = get_all_employer_internships(employer_id)
    return jsonify(internships), 200

@internship_views.route('/internship', methods=['POST'])
@jwt_required()
def create_new_internship():
    employer_id = get_jwt_identity()
    if is_employer(employer_id) is False:
        return jsonify({"Error": "Unauthorized, only employers allowed"}), 403
    
    data = request.get_json()

    required_fields = ['title', 'description']
    missing = [field for field in required_fields if field not in data]

    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400

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
        return jsonify({"Error": "Unauthorized, you do not own this internship"}), 403
    
    data = request.get_json()

    required_fields = ['title', 'description']
    missing = [field for field in required_fields if field not in data]

    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400

    success, message = update_internship_info(internship_id, data.get('title', None), data.get('description', None))
    status_code = 200 if success else 400
    return jsonify({"message": message}), status_code

@internship_views.route('/internship/<internship_id>', methods=['DELETE'])
@jwt_required()
def remove_internship(internship_id):
    employer_id = get_jwt_identity()
    if get_internship_by_id(internship_id) is None:
        return jsonify({"Error": "Internship not found"}), 404
    if not belongs_to_employer(internship_id, employer_id):
        return jsonify({"Error": "Unauthorized, you do not own this internship"}), 403
    success, message = delete_internship(internship_id)
    status_code = 200 if success else 400
    return jsonify({"message": message}), status_code