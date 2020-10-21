# from marshmallow import Schema, fields
from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):  # instead of inheriting from Schema
    class Meta:
        model = UserModel
        load_only = ("password",)  # only load "password" but do not dump it
        # because we do not want to display the user password on the screen -> security issue
        dump_only = ("id",)  # do not need to load this field, it is only for dump
        load_instance = True

        # although the required fields cannot be marked here, we can mark them in UserModel using "nullable"

    '''
    # can get rid of this using flask_marshmallow
    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    '''
