from flask import Flask
from app.extensions import db, ma, migrate, jwt, swagger
from app.api.routes import register_routes
from flask_cors import CORS


def create_app(config_name="default"):
    from config import config
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # def init_swagger(app):
    #     app.config['SWAGGER'] = {
    #         'title': 'Taskflow API',
    #         'uiversion': 3,
    #         'version': '1.0',
    #         'description': 'Taskflow API documentation',
    #         'specs': [
    #             {
    #                 'endpoint': 'apispec',
    #                 'route': '/apispec.json',
    #                 'rule_filter': lambda rule: True,  # lambdas must stay in Python
    #                 'model_filter': lambda tag: True,  # lambdas must stay in Python
    #             }
    #         ],
    #         'securityDefinitions': {
    #             'Bearer': {
    #                 'type': 'apiKey',
    #                 'name': 'Authorization',
    #                 'in': 'header',
    #                 'description': 'Enter your bearer token in the format: Bearer <token>'
    #             }
    #         },
    #         'security': [
    #             {
    #                 'Bearer': []
    #             }
    #         ]
    # }
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
    
    return app