from fastapi import APIRouter as BaseRouter
from core.config import conf
import importlib
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from article.models import Article
templates = Jinja2Templates(directory="templates")

base_router = BaseRouter()


@base_router.get("/")
async def index(request: Request):
    article_li = await Article.all().order_by('-id').limit(10).offset(0)
    count = await Article.all().count()
    return templates.TemplateResponse('index.html',
                                      {"request": request, "res": article_li, "page_num": 1,
                                       "count": count, "pages": count//10 + 1}
                                      )


def router_register(app):
    app.include_router(base_router)
    for view in conf.views:
        view = importlib.import_module(f'{view}.views')
        app.include_router(view.router)