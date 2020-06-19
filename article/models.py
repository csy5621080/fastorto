from tortoise.models import Model
from tortoise import fields
from user.models import User


class Article(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=128)
    body = fields.TextField()
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User', related_name='author_user ')
    create_time = fields.DatetimeField(auto_now_add=True)
    img_path = fields.CharField(max_length=256, null=True)


class Comment(Model):
    id = fields.IntField(pk=True)
    article: fields.ForeignKeyRelation[Article] = fields.ForeignKeyField('models.Article', related_name='comment_article')
    parent = fields.ForeignKeyField('models.Comment', related_name='comment_parent')
    author = fields.CharField(max_length=128)
    email = fields.CharField(max_length=128, null=True)
    create_time = fields.DatetimeField(auto_now_add=True)
