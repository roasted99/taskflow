import uuid
from flask_jwt_extended import create_access_token
import bcrypt
from datetime import datetime, timedelta
from flask import current_app
from app.models.user import User
from app import db

class AuthService:
    @staticmethod
    def register(first_name, last_name, email, password):
        """Register a new user and return JWT token."""
        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"error": "Email already registered"}, 409
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
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
        
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(days=5)
        )
        
        return {
            "token": access_token,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }, 200
