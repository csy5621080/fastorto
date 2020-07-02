from tortoise.models import Model
from tortoise import fields
from user.models import User
from core.serializer import Serializer
from tags.models import Tag


class Article(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=128)
    body = fields.TextField()
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User', related_name='author_user')
    create_time = fields.DatetimeField(auto_now_add=True)
    img_path = fields.CharField(max_length=256, null=True)
    is_public = fields.BooleanField(default=True)
    summary = fields.CharField(max_length=500)
    article_tag: fields.ManyToManyRelation["Tag"] = fields.ManyToManyField('models.Tag',
                                                                           related_name='articles',
                                                                           through="article_tag")

    @classmethod
    async def article_page(cls, page_num: int = 1, page_size: int = 10, backend: bool = False):
        article_li: list = await Article.all().order_by('-id').limit(page_size).offset((page_num - 1) * 10)
        res = []
        for art in article_li:
            other_ = dict()
            if not backend:
                comment_count: int = await art.comment_article.all().count()
                other_ = dict(comment_count=comment_count)
            art = await Serializer(art, with_relate=True).to_dict()
            art.update(other_)
            res.append(art)
        count = await Article.all().count()
        return dict(res=res, count=count, page_num=page_num, pages=count // 10 + 1)

    @classmethod
    async def article_detail(cls, pk, backend=False):
        res: Article = await Article.get(id=pk)
        res: dict = await Serializer(res, with_relate=True).to_dict()
        if not backend:
            comments: list = await Comment.filter(article_id=pk).order_by('-create_time')
            comments = [await Serializer(comment, with_relate=True).to_dict() for comment in comments]
            res.update(dict(comments=comments))
        return res

    @classmethod
    async def creator(cls, **kwargs):
        art = await Article.create(title=kwargs.get('title'),
                                   body=kwargs.get('body'),
                                   author_id=kwargs.get('author_id'),
                                   is_public=kwargs.get('is_public', True),
                                   summary=kwargs.get('summary'))
        tags = kwargs.get('tags')
        [await art.article_tag.add(await Tag.get(id=tag_id)) for tag_id in tags]
        return await Serializer(art, with_relate=True).to_dict()

    @classmethod
    async def updater(cls, pk, **kwargs):
        await Article.filter(id=pk).update(title=kwargs.get('title'),
                                           body=kwargs.get('body'),
                                           is_public=kwargs.get('is_public', True),
                                           summary=kwargs.get('summary'))
        art = await Article.get(id=pk)
        await art.article_tag.clear()
        tags = kwargs.get('tags')
        [await art.article_tag.add(await Tag.get(id=tag)) for tag in tags]
        return await Serializer(art, with_relate=True).to_dict()


class Comment(Model):
    id = fields.IntField(pk=True)
    article: fields.ForeignKeyRelation[Article] = fields.ForeignKeyField('models.Article',
                                                                         related_name='comment_article')
    parent = fields.ForeignKeyField('models.Comment', related_name='comment_parent', null=True)
    author = fields.CharField(max_length=128, null=True)
    email = fields.CharField(max_length=128, null=True)
    create_time = fields.DatetimeField(auto_now_add=True)
    content = fields.CharField(max_length=2000, null=False)
    ip = fields.CharField(max_length=128)
