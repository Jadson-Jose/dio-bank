from marshmallow import fields
from src.app import ma


class UserSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    role_id = fields.Int(required=True)
