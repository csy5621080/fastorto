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

    @classmethod
    async def article_page(cls, page_num: int = 1, page_size: int = 10):
        article_li: list = await Article.all().order_by('-id').limit(page_size).offset((page_num - 1) * 10)
        res = []
        for art in article_li:
            comment_count: int = await art.comment_article.all().count()
            art.comment_count = comment_count
            author = await art.author
            art.author = author
            res.append(art)
        count = await Article.all().count()
        return dict(res=res, count=count, page_num=page_num, pages=count // 10 + 1)


class Comment(Model):
    id = fields.IntField(pk=True)
    article: fields.ForeignKeyRelation[Article] = fields.ForeignKeyField('models.Article', related_name='comment_article')
    parent = fields.ForeignKeyField('models.Comment', related_name='comment_parent', null=True)
    author = fields.CharField(max_length=128, null=True)
    email = fields.CharField(max_length=128, null=True)
    create_time = fields.DatetimeField(auto_now_add=True)
    content = fields.CharField(max_length=2000, null=False)
    ip = fields.CharField(max_length=128)