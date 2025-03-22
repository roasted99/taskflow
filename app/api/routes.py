from flask import Blueprint
from flask_restful import Api
from app.api.resources.user import UserResource
from app.api.resources.task import TaskResource

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

def register_routes(app):
    api.add_resource(UserResource, '/users', '/users/<string:user_id>')
    
    api.add_resource(TaskResource, '/tasks', '/tasks/<string:task_id>')
    
    app.register_blueprint(api_bp)
    
     