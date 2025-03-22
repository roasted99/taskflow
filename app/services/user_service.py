from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    @staticmethod
    def get_all_users():
        return User.query.all()
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def create_user(first_name, last_name, email, password):
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if not user:
            return None
        
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password_hash = generate_password_hash(data['password'])
        
        db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        return True
    
    @staticmethod
    def authenticate(email, password):
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return user
        return None