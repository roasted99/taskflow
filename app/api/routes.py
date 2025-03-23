from flask import Blueprint
from flask_restful import Api
from app.api.resources.user import UserResource
from app.api.resources.task import TaskResource, TaskItemResource


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

def register_routes(app):
    from app.api.auth_controller import auth_bp

    app.register_blueprint(auth_bp)
    
    api.add_resource(UserResource, '/users')
    
    api.add_resource(TaskResource, '/tasks')
    api.add_resource(TaskItemResource, '/tasks/<string:task_id>')
    
    app.register_blueprint(api_bp)
    
     