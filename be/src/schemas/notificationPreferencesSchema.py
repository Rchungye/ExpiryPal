from marshmallow import Schema, fields

class NotificationPreferencesSchema(Schema):
    fridge_id = fields.Int(required=True)
    expiration = fields.Int(required=True)
    unusedItem = fields.Int(required=True)
