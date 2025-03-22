from flask import Flask
from app.extensions import db, ma, migrate, jwt
from app.api.routes import register_routes
from flask_jwt_extended import JWTManager
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

def create_app(config_name="default"):
    from config import config
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    register_routes(app)
    
    return app