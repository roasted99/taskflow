from flask import request, jsonify
from flask_restful import Resource
from app.services.user_service import UserService
from app.schemas.user import user_schema, users_schema
from flask_jwt_extended import jwt_required

class UserResource(Resource):
    @jwt_required()
    def get(self, user_id=None):
        if user_id:
            user = UserService.get_user_by_id(user_id)
            if not user:
                return {"message": "User not found"}, 404
            return user_schema.dump(user)
        
        users = UserService.get_all_users()
        return users_schema.dump(users)
    
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        # Validate data
        try:
            data = user_schema.load(json_data)
        except Exception as e:
            return {"message": str(e)}, 422
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=json_data.get('username')).first()
        if existing_user:
            return {"message": "User already exists"}, 409
        
        # Create user
        user = UserService.create_user(
            username=json_data.get('username'),
            email=json_data.get('email'),
            password=json_data.get('password')
        )
        
        return user_schema.dump(user), 201
    
    @jwt_required()
    def put(self, user_id):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        user = UserService.update_user(user_id, json_data)
        if not user:
            return {"message": "User not found"}, 404
        
        return user_schema.dump(user)
    
    @jwt_required()
    def delete(self, user_id):
        result = UserService.delete_user(user_id)
        if not result:
            return {"message": "User not found"}, 404
        
        return {"message": "User deleted successfully"}, 200