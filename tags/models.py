from tortoise.models import Model
from tortoise import fields


class Tag(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128)
    create_time = fields.DatetimeField(auto_now_add=True)
