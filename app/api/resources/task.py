from flask import request, jsonify
import uuid
from flask_restful import Resource
from app.services.task_service import TaskService
from app.schemas.task import task_schema, tasks_schema
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from marshmallow import fields
from flasgger import swag_from

class TaskResource(Resource):
    @jwt_required()
    @swag_from('../../docs/task/get_all_task.yml')
    def get(self):
        # Get query parameters for filtering
        status = request.args.get('status')
        priority = request.args.get('priority')
        assigned_to_id = request.args.get('assigned_to_id', type=str)
        owned_by_id = request.args.get('owned_by_id', type=str)
        date_range = request.args.get('date_range', type=str)
        
        # Create filters dictionary
        filters = {}
        if status:
            filters['status'] = status
        if priority:
            filters['priority'] = priority
        if assigned_to_id:
            filters['assigned_to_id'] = assigned_to_id
        if owned_by_id:
            filters['owned_by_id'] = owned_by_id
        if date_range:
            filters['date_range'] = date_range
        
        print(filters)
            
        # Get tasks with filters
        tasks = TaskService.get_all_tasks(filters)
        return tasks_schema.dump(tasks)
    
    @jwt_required()
    @swag_from('../../docs/task/create_task.yml')
    # @doc(description='Create a new task', tags=['Tasks'])
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        # Get the current user from the JWT
        current_user_id = get_jwt_identity()
        
        # Set the created_by field to the current user
        json_data['owned_by_id'] = current_user_id
        
        json_data['start_date'] = json_data.get('start_date') if json_data.get('start_date').strip() else None
        json_data['end_date'] = json_data.get('end_date') if json_data.get('end_date').strip() else None
        json_data['assigned_to_id'] = json_data.get('assgined_to_id') if json_data.get('assgined_to_id') and json_data.get('assigned_to_id').strip() else None
        
        # Validate data
        try:
            data = task_schema.load(json_data)
        except Exception as e:
            return {"message": str(e)}, 422
        
        
        # Create task
        task = TaskService.create_task(
            title=json_data.get('title'),
            description=json_data.get('description'),
            status=json_data.get('status'),
            priority=json_data.get('priority'),
            start_date=json_data.get('start_date'),
            end_date=json_data.get('end_date'),
            assigned_to_id=json_data.get('assigned_to_id'),
            owned_by_id=current_user_id
        )
        
        return task_schema.dump(task), 201
    
    
class TaskItemResource(Resource):
    @jwt_required()
    @swag_from('../../docs/task/get_task.yml')
    def get(self, task_id):
        if task_id:
            return {"message": "No UUID has provided"}
        try:
            # Convert string UUID to UUID object
            task_id = uuid.UUID(task_id)
            task = TaskService.get_task_by_id(task_id)
            if not task:
                return {"message": "Task not found"}, 404
            return task_schema.dump(task)
        except ValueError:
            return {"message": "Invalid UUID format"}, 400

    @jwt_required()
    @swag_from('../../docs/task/update_task.yml')
    # @doc(description='Update an existing task', tags=['Tasks'])
    def put(self, task_id):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        # Get the current user from the JWT
        current_user_id = get_jwt_identity()
        print(current_user_id)
        
        # Check if task exists and user has permission
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return {"message": "Task not found"}, 404
        
        # # # Only the creator or the assigned user can update the task
        if str(task.owned_by_id) != current_user_id and str(task.assigned_to_id) != current_user_id:
            return {"message": "You don't have permission to update this task"}, 403
        
        # # Update task
        task = TaskService.update_task(task_id, json_data)
        
        return task_schema.dump(task)
    
    @jwt_required()
    @swag_from('../../docs/task/delete_task.yml')
    def delete(self, task_id):
        # Get the current user from the JWT
        current_user_id = get_jwt_identity()
        
        # Check if task exists and user has permission
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return {"message": "Task not found"}, 404
        
        # # Only the creator can delete the task
        if str(task.owned_by_id) != current_user_id:
            return {"message": "You don't have permission to delete this task"}, 403
        
        # Delete task
        result = TaskService.delete_task(task_id)
        
        return {"message": "Task deleted successfully"}, 200
    