from app.extensions import ma
from app.models.task import Task, TaskPriority, TaskStatus
from marshmallow import fields, validate, validates_schema, ValidationError
from app.schemas.user import UserSchema
from datetime import datetime

class TaskSchema(ma.SQLAlchemyAutoSchema):
    """Task schema."""
    class Meta:
        model = Task
        include_fk = True
        load_instance = True
        
    id = fields.UUID(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=3, max=200))
    description = fields.Str(require=False)
    status = fields.Str(required=False, validate=validate.OneOf([status.value for status in TaskStatus]))
    priority = fields.Str(required=False, validate=validate.OneOf([priority.value for priority in TaskPriority]))
    start_date = fields.Date(required=False)
    end_date = fields.Date(required=False)    
    assigned_to_id = fields.UUID(required=False, allow_none=True)  
    owned_by_id = fields.UUID(required=True) 
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True) 
    
    # Include user details in the response
    assigned_to = fields.Nested(UserSchema(only=('id', 'first_name', 'last_name')), dump_only=True)
    owned_by = fields.Nested(UserSchema(only=('id', 'first_name', 'last_name')), dump_only=True)
    
    @validates_schema
    def validate_dates(self, data, **kwargs):
        if 'start_date' in data and 'end_date' in data and data['start_date'] and data['end_date']:
            if data['start_date'] > data['end_date']:
                raise ValidationError("End date must be after start date")



task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
    
    
    
    