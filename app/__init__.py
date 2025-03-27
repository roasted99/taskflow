from flask import Flask
from app.extensions import db, ma, migrate, jwt, swagger
from app.api.routes import register_routes
from flask_cors import CORS
from app.seed import seed_database
from flask.cli import with_appcontext


def create_app(config_name="default"):
    from config import config
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.config['SWAGGER']={
        'title': 'Taskflow API',
        'uiversion': 3,
        'version': '1.0',
        'description': 'Taskflow API documentation',
        'specs': [
            {
                'endpoint': 'apispec',
                'route': '/apispec.json',
                'rule_filter': lambda rule: True,  # lambdas must stay in Python
                'model_filter': lambda tag: True,  # lambdas must stay in Python
            }
        ],
        'securityDefinitions': {
            'Bearer': {
                'type': 'apiKey',
                    'name': 'Authorization',
                    'in': 'header',
                    'description': 'Enter your bearer token in the format: Bearer <token>'
                }
            },
            'security': [
                {
                    'Bearer': []
                }
            ]
    }
    swagger.init_app(app) 
    CORS(app)
    
    register_routes(app)

        # CLI command for seeding
    @app.cli.command('seed-db')
    @with_appcontext
    def seed_db_command():
        """Clear the existing data and create new data."""
        with app.app_context():
            # Create all tables
            db.create_all()
            # Seed the database
            seed_database()
            print('Database seeded successfully.')
    
    return app