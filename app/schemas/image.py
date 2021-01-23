from marshmallow import Schema, fields, post_load

from app.models.image import Image


class ImageSchema(Schema):
    _id = fields.Str()
    filename = fields.Str()
    extension = fields.Str()
    created = fields.Str()
    thumbnail_task = fields.Str(allow_none=True)

    @post_load
    def make_image(self, data, **kwargs):
        return Image(**data)
