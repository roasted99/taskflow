from datetime import datetime
import uuid
import enum
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class TaskStatus(enum.Enum):
    TODO= 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'
    
class TaskPriority(enum.Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    
class Task(db.Model):
    """Task model."""
    __tablename__ = 'tasks'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    priority = db.Column(db.Enum(TaskPriority), nullable=False, default = TaskPriority.MEDIUM)
    start_date = db.Column(db.Date, nullable = True)
    end_date = db.Column(db.Date, nullable=True)
    
    # Relationship with users
    assigned_to_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)
    owned_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    # Relationship definitions for easy access
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id], backref=db.backref('assigned_tasks', lazy='dynamic'))
    owned_by = db.relationship('User', foreign_keys=[owned_by_id], backref=db.backref('created_tasks', lazy='dynamic'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'priority': self.priority.value,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'owned_by': self.owned_by,
            'assigned_to': self.assigned_to,
            'owned_by_id': self.owned_by_id,
            'assgined_by_id': self.assigned_to_id
        }    
    