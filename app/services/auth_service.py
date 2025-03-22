import uuid
import jwt
import bcrypt
# from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from flask import current_app
from app.models.user import User
from app import db

# bcrypt = Bcrypt(app)

class AuthService:
    @staticmethod
    def register(first_name, last_name, email, password):
        """Register a new user and return JWT token."""
        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"error": "Email already registered"}, 409
        
        print(first_name, last_name, email)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        print(password_hash)
        
        new_user = User(
            id=str(uuid.uuid4()),
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password_hash,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return AuthService.login(email, password)
    
    @staticmethod
    def login(email, password):
        """Authenticate user and return JWT token."""
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return {"error": "Invalid credentials"}, 401
        
        # Check password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return {"error": "Invalid credentials"}, 401
        
        token = AuthService.generate_token(user)
        
        return {
            "token": token,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }, 200
    
    @staticmethod
    def generate_token(user):
        """Generate JWT token for user."""
        payload = {
            'sub': str(user.id),
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=1)  # Token expires in 1 day
        }
        
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    
    @staticmethod
    def verify_token(token):
        """Verify JWT token and return user."""
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            
            user_id = payload['sub']
            return User.query.get(user_id)
        except jwt.ExpiredSignatureError:
            return None  
        except jwt.InvalidTokenError:
            return None  
