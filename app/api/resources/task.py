from flask import request, jsonify
import uuid
from flask_restful import Resource
from app.services.task_service import TaskService
from app.schemas.task import task_schema, tasks_schema
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
# from flask_apispec import use_kwargs, marshal_with, doc
from marshmallow import fields

class TaskResource(Resource):
    @jwt_required()
    # @doc(description='Get a task or list of tasks', tags=['Tasks'])
    def get(self, task_id=None):
        if task_id:
            try:
                # Convert string UUID to UUID object
                task_id = uuid.UUID(task_id)
                task = TaskService.get_task_by_id(task_id)
                if not task:
                    return {"message": "Task not found"}, 404
                return task_schema.dump(task)
            except ValueError:
                return {"message": "Invalid UUID format"}, 400

        
        # Get query parameters for filtering
        status = request.args.get('status')
        priority = request.args.get('priority')
        assigned_to_id = request.args.get('assigned_to_id', type=str)
        created_by_id = request.args.get('created_by_id', type=str)
        
        # Create filters dictionary
        filters = {}
        if status:
            filters['status'] = status
        if priority:
            filters['priority'] = priority
        if assigned_to_id:
            filters['assigned_to_id'] = assigned_to_id
        if created_by_id:
            filters['created_by_id'] = created_by_id
            
        # Get tasks with filters
        tasks = TaskService.get_all_tasks(filters)
        return tasks_schema.dump(tasks)
    
    @jwt_required()
    # @doc(description='Create a new task', tags=['Tasks'])
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        # Get the current user from the JWT
        current_user_id = get_jwt_identity()
        
        # Set the created_by field to the current user
        json_data['created_by_id'] = current_user_id
        
        # Validate data
        try:
            data = task_schema.load(json_data)
        except Exception as e:
            return {"message": str(e)}, 422
        
        # Create task
        task = TaskService.create_task(
            title=json_data.get('title'),
            body=json_data.get('body'),
            status=json_data.get('status'),
            priority=json_data.get('priority'),
            start_date=json_data.get('start_date'),
            end_date=json_data.get('end_date'),
            assigned_to_id=json_data.get('assigned_to_id'),
            created_by_id=current_user_id
        )
        
        return task_schema.dump(task), 201
    
    @jwt_required()
    # @doc(description='Update an existing task', tags=['Tasks'])
    def put(self, task_id):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        # Get the current user from the JWT
        current_user_id = get_jwt_identity()
        
        # Check if task exists and user has permission
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return {"message": "Task not found"}, 404
        
        # # Only the creator or the assigned user can update the task
        if task.created_by_id != current_user_id and task.assigned_to_id != current_user_id:
            return {"message": "You don't have permission to update this task"}, 403
        
        # # Update task
        task = TaskService.update_task(task_id, json_data)
        
        return task_schema.dump(task)
    
    @jwt_required()
    # @doc(description='Delete a task', tags=['Tasks'])
    def delete(self, task_id):
        # Get the current user from the JWT
        current_user_id = get_jwt_identity()
        
        # Check if task exists and user has permission
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return {"message": "Task not found"}, 404
        
        # # Only the creator can delete the task
        if task.created_by_id != current_user_id:
            return {"message": "You don't have permission to delete this task"}, 403
        
        # Delete task
        result = TaskService.delete_task(task_id)
        
        return {"message": "Task deleted successfully"}, 200