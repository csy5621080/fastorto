from fastapi import APIRouter as ArticleAPIRouter
from fastapi.encoders import jsonable_encoder
from article.models import Article
from fastapi.requests import Request
from core.routers import templates
from fastapi import UploadFile, File
from fastapi.responses import Response
import json
router = ArticleAPIRouter()


@router.get('/articles/list')
async def articles(request: Request):
    article_li = await Article.all()
    return article_li


@router.post('/articles/push')
async def article(request: Request, data: dict):
    data = jsonable_encoder(data)
    data['author_id'] = 1
    res = await Article.create(**data)
    return templates.TemplateResponse('edit.html', {"request": request, 'res': res})


@router.get("/articles/creator")
async def article_creator(request: Request):
    return templates.TemplateResponse('edit.html', {"request": request})


@router.post('/upload_img/')
async def upload_img(file: UploadFile = File(...)):
    contents = await file.read()
    save_path = '/static/img/' + file.filename
    relative_path = '.' + save_path
    with open(relative_path, 'wb+') as img:
        img.write(contents)
    return Response(content=json.dumps({"errno": 0, "data": [save_path]}))