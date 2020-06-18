from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128, null=True)
    user_name = fields.CharField(max_length=128, null=False)
    pass_word = fields.CharField(max_length=256, null=False)

    class Meta:
        db_table = 'user'
