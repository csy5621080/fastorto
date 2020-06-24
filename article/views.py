from fastapi import APIRouter as ArticleAPIRouter
from fastapi.encoders import jsonable_encoder
from article.models import Article, Comment
from fastapi.requests import Request
from core.routers import templates
from fastapi import UploadFile, File
from fastapi.responses import Response
import json
router = ArticleAPIRouter()


@router.get('/articles/list/{page_num}')
async def articles(request: Request, page_num: int):
    article_li = await Article.all().order_by('-id').limit(10).offset((page_num-1)*10)
    res = []
    for art in article_li:
        comment_count: int = await art.comment_article.all().count()
        art.comment_count = comment_count
        res.append(art)
    count = await Article.all().count()
    return templates.TemplateResponse('index.html',
                                      {"request": request, "res": res, "page_num": page_num,
                                       "count": count, "pages": count//10 + 1}
                                      )


@router.get('/article/detail/{pk}')
async def article(request: Request, pk: int):
    res = await Article.get(id=pk)
    comments = await Comment.filter(article_id=pk).order_by('-create_time')
    return templates.TemplateResponse('article.html', {"request": request, 'res': res, 'comments': comments})


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
    try:
        contents = await file.read()
        save_path = '/static/img/' + file.filename
        relative_path = '.' + save_path
        with open(relative_path, 'wb+') as img:
            img.write(contents)
        return Response(content=json.dumps({"errno": 0, "data": [save_path]}))
    except Exception as e:
        return Response(content=str(e))


@router.post('/article/{article_id}/comment')
async def comment(request: Request, data: dict, article_id: int):
    ip = request.client.host
    data = jsonable_encoder(data)
    data['ip'] = ip
    data['article_id'] = article_id
    comment = await Comment.create(**data)
    return comment