from fastapi import APIRouter as ArticleAPIRouter
from fastapi.encoders import jsonable_encoder
from article.models import Article, Comment
from fastapi.requests import Request
from core.routers import templates
from fastapi import UploadFile, File
from fastapi.responses import Response, JSONResponse
import json

router = ArticleAPIRouter()


@router.get('/list/{page_num}')
async def articles(request: Request, page_num: int):
    res = await Article.article_page(page_num)
    return JSONResponse(res)


@router.get('/admin/list/{page_num}')
async def admin_articles(request: Request, page_num: int):
    res = await Article.article_page(page_num, backend=True)
    return JSONResponse(res)


@router.get('/detail/{pk}')
async def article(request: Request, pk: int):
    res: Article = await Article.get(id=pk)
    comments: list = await Comment.filter(article_id=pk).order_by('-create_time')
    author = await res.author
    return templates.TemplateResponse('article.html',
                                      {"request": request, 'res': res, 'comments': comments, 'author': author})


@router.get('/admin/detail/{pk}')
async def article(request: Request, pk: int):
    res: dict = await Article.article_detail(pk, backend=True)
    return JSONResponse(res)


@router.post('/push')
async def article(request: Request, data: dict):
    data: dict = jsonable_encoder(data)
    data['author_id'] = 1
    res = await Article.create(**data)
    return templates.TemplateResponse('edit.html', {"request": request, 'res': res})


@router.get("/creator")
async def article_creator(request: Request):
    return templates.TemplateResponse('edit.html', {"request": request})


@router.post('/upload_img/')
async def upload_img(file: UploadFile = File(...)):
    try:
        contents: bytes = await file.read()
        save_path = '/static/img/' + file.filename
        relative_path = '.' + save_path
        with open(relative_path, 'wb+') as img:
            img.write(contents)
        return Response(content=json.dumps({"errno": 0, "data": [save_path]}))
    except Exception as e:
        return Response(content=str(e))


@router.post('/{article_id}/comment')
async def comment(request: Request, data: dict, article_id: int):
    ip = request.client.host
    data = jsonable_encoder(data)
    data['ip'] = ip
    data['article_id'] = article_id
    comment = await Comment.create(**data)
    return comment
