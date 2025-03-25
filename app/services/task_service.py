from app.extensions import db
from app.models.task import Task, TaskStatus, TaskPriority
from datetime import datetime
from sqlalchemy import and_, or_

class TaskService:
    @staticmethod
    def get_all_tasks(filters=None):
        """
        Get all tasks with optional filtering
        
        Args:
            filters (dict): Dictionary of filters to apply
                - status: Status to filter by
                - priority: Priority to filter by
                - assigned_to_id: Filter by assigned user
                - created_by_id: Filter by creator
        """
        query = Task.query
        
        if filters:
            # Apply status filter
            if 'status' in filters and filters['status']:
                query = query.filter(Task.status == filters['status'])
            
            # Apply priority filter
            if 'priority' in filters and filters['priority']:
                query = query.filter(Task.priority == filters['priority'])
            
            # Apply assigned_to filter
            if 'assigned_to_id' in filters and filters['assigned_to_id']:
                query = query.filter(Task.assigned_to_id == filters['assigned_to_id'])
            
            # Apply created_by filter
            if 'owned_by_id' in filters and filters['owned_by_id']:
                query = query.filter(Task.owned_by_id == filters['ownedby_id'])
                
            # Apply date range filter
            if 'date_range' in filters and filters['date_range']:
                start, end = filters['date_range']
                if start and end:
                    # Tasks that overlap with the date range
                    query = query.filter(
                        or_(
                            and_(Task.start_date <= end, Task.end_date >= start),
                            and_(Task.start_date <= end, Task.end_date.is_(None)),
                            and_(Task.start_date.is_(None), Task.end_date >= start),
                        )
                    )
        
        # Order by priority (highest first) and creation date (newest first)
        tasks = query.order_by(Task.priority.desc(), Task.created_at.desc()).all()
        task_list = [task.to_dict() for task in tasks]

        return task_list
    
    @staticmethod
    def get_task_by_id(task_id):
        return Task.query.get(task_id)
    
    @staticmethod
    def create_task(title, description, status, priority, start_date, end_date, assigned_to_id, owned_by_id):
        task = Task(
            title=title,
            description=description,
            status=status,
            priority=priority,
            start_date=start_date,
            end_date=end_date,
            assigned_to_id=assigned_to_id,
            owned_by_id=owned_by_id
        )
        db.session.add(task)
        db.session.commit()
        return task.to_dict()
    
    @staticmethod
    def update_task(task_id, data):
        task = Task.query.get(task_id)
        if not task:
            return None
        
        # Update fields if provided
        if 'title' in data:
            task.title = data['title']
        if 'body' in data:
            task.body = data['body']
        if 'status' in data:
            task.status = data['status']
        if 'priority' in data:
            task.priority = data['priority']
        if 'start_date' in data:
            task.start_date = data['start_date']
        if 'end_date' in data:
            task.end_date = data['end_date']
        if 'assigned_to_id' in data:
            task.assigned_to_id = data['assigned_to_id']
        
        db.session.commit()
        return task.to_dict()
    
    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return False
        
        db.session.delete(task)
        db.session.commit()
        return True