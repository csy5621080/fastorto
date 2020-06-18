from tortoise.models import Model
from tortoise import fields
from user.models import User


class Article(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=128)
    body = fields.TextField()
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User', related_name='author_user')
    create_time = fields.DatetimeField(auto_now_add=True)
