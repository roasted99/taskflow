from flask import request, jsonify
from flask_restful import Resource
from app.services.user_service import UserService
from app.schemas.user import user_schema, users_schema
from flask_jwt_extended import jwt_required
from flasgger import swag_from

class UserResource(Resource):
    @jwt_required()
    @swag_from('../../docs/user/get_all_user.yml')
    def get(self):        
        users = UserService.get_all_users()
        return users_schema.dump(users)
    
