from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Extract token from header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        
        # Verify token
        user = AuthService.verify_token(token)
        if not user:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        return f(user, *args, **kwargs)
    
    return decorated

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
@token_required
def get_current_user(user):
    """Example of a protected route that returns current user info"""
    return jsonify({
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }), 200
