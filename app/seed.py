from app.extensions import db
from app.models.user import User
from app.models.task import Task
from datetime import datetime

def seed_database():
    # Clear existing data
    Task.query.delete()
    User.query.delete()
    
    # Sample users
    users = [
        User(
            first_name='Jan', 
            last_name='Barber', 
            email='jan@corporate.com', 
            password='securepass123'
        ),
        User(
            first_name='Roy', 
            last_name='Trenneman', 
            email='roy@corporate.com', 
            password='password456'
        ),
        User(
            first_name='Maurice', 
            last_name='Moss', 
            email='moss@corporate.com', 
            password='robotistakingover'
        ),
    ]
    
    # Add users to the session
    db.session.add_all(users)
    db.session.commit()
    
    # Sample tasks
    tasks = [
        Task(
            owned_by_id=users[0].id,
            title='Complete Project Proposal',
            description='Draft and finalize the project proposal for Q2',
            status='IN_PROGRESS',
            priority='HIGH',
            start_date=datetime.now(),
            end_date=datetime.now()
        ),
        Task(
            owned_by_id=users[1].id,
            title='Design System Review',
            description='Conduct a comprehensive review of the current design system',
            status='DONE',
            priority='LOW',
            start_date=datetime.now(),
            end_date=datetime.now()
        ),
        Task(
            owned_by_id=users[2].id,
            title='Change Button color',
            description='Change search button color to green.',
            status='TODO',
            priority='MEDIUM',
            start_date=datetime.now(),
            end_date=datetime.now()
        ),
        Task(
            owned_by_id=users[1].id,
            assigned_to_id=users[1].id,
            title='Revise Architecture plan',
            description='Conduct a review for a new system',
            status='IN_PROGRESS',
            priority='MEDIUM',
            start_date=datetime.now(),
            end_date=datetime.now()
        )
    ]
    
    # Add tasks to the session
    db.session.add_all(tasks)
    db.session.commit()