from fastapi import APIRouter as ArticleAPIRouter
from fastapi.encoders import jsonable_encoder
from article.models import Article
from fastapi.requests import Request
from core.routers import templates
router = ArticleAPIRouter()


@router.get('/articles/list')
async def articles(request: Request):
    article_li = await Article.all()
    return article_li


@router.post('/articles/push')
async def article(request: Request, data: dict):
    data = jsonable_encoder(data)
    print(data)


@router.get("/articles/creator")
async def article_creator(request: Request):
    return templates.TemplateResponse('edit.html', {"request": request})