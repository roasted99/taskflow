from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from app.services.auth_service import AuthService
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    print(data)
    # Validate input
    if not all(key in data for key in ['first_name', 'last_name', 'email', 'password']):
        return jsonify({"error": "Missing required fields"}), 400

    # Register user
    result, status_code = AuthService.register(
        data['first_name'],
        data['last_name'],
        data['email'],
        data['password']
    )
    
    return jsonify(result), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate input
    if not all(key in data for key in ['email', 'password']):
        return jsonify({"error": "Missing email or password"}), 400
    
    # Login user
    result, status_code = AuthService.login(
        data['email'],
        data['password']
    )
    
    return jsonify(result), status_code

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Example of a protected route that returns current user info"""
    
    return jsonify({
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name
    }), 200
