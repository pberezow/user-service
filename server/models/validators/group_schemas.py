from marshmallow import Schema, fields, validates, ValidationError


class NewGroupSchema(Schema):
    licence_id = fields.Int(required=True)
    name = fields.Str(required=True)


class SetGroupDataSchema(Schema):
    licence_id = fields.Int(required=True)
    name = fields.Str(required=True)
