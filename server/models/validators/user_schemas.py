from marshmallow import Schema, fields, validates, ValidationError


class CreateUserSchema(Schema):    
    licence_id = fields.Int(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True)
    is_admin = fields.Bool(required=True)
    phone_number = fields.Str(required=False)
    address = fields.Str(required=False)
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    position = fields.Str(required=False)

    # @validates('username')
    # def validate_username(value):
    #     if len(value) < 6:
    #         raise ValidationError('Username is too short!')
    #     elif len(value) > 30:
    #         raise ValidationError('Username is too long!')

    # @validates('password')
    # def validate_password(value):
    #     if len(value) < 8:
    #         raise ValidationError('Password is too short!')


class LoginUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    
    # @validates('username')
    # def validate_username(value):
    #     if len(value) < 6:
    #         raise ValidationError('Username is too short!')
    #     elif len(value) > 30:
    #         raise ValidationError('Username is too long!')

    # @validates('password')
    # def validate_password(value):
    #     if len(value) < 8:
    #         raise ValidationError('Password is too short!')


class SetPasswordUserSchema(Schema):
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True)


class SetUserDataSchema(Schema):  # only admin
    username = fields.Str(required=False)
    email = fields.Email(required=False)
    is_admin = fields.Bool(required=False)
    phone_number = fields.Str(required=False)
    address = fields.Str(required=False)
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    position = fields.Str(required=False)


class SetUserGroupsSchema(Schema):
    groups = fields.List(fields.Str(), required=True)