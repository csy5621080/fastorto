from tortoise.models import Model
from tortoise import fields
from core.serializer import Serializer


class Tag(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128)
    create_time = fields.DatetimeField(auto_now_add=True)

    @classmethod
    async def get_all(cls):
        tags = await Tag.all()
        tag_li = [await Serializer(tag, with_relate=True).to_dict() for tag in tags]
        return tag_li
