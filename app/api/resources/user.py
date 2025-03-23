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
        # if user_id:
        #     user = UserService.get_user_by_id(user_id)
        #     if not user:
        #         return {"message": "User not found"}, 404
        #     return user_schema.dump(user)
        
        users = UserService.get_all_users()
        return users_schema.dump(users)
    
# class UserItemResource(Resource):
    
#     @jwt_required()
#     def put(self, user_id):
#         json_data = request.get_json()
#         if not json_data:
#             return {"message": "No input data provided"}, 400
        
#         user = UserService.update_user(user_id, json_data)
#         if not user:
#             return {"message": "User not found"}, 404
        
#         return user_schema.dump(user)
