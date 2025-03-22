from app.extensions import ma
from app.models.user import User
from marshmallow import fields, validate

class UserSchema(ma.SQLAlchemyAutoSchema):
    """User schema."""
    class Meta:
        model = User
        load_instance = True
        exclude = ('password',)
    
    id = fields.UUID(dump_only=True)  
    first_name = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    last_name = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)