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
    article_li = await Article.all()
    return templates.TemplateResponse('index.html', {"request": request, "res": article_li})


def router_register(app):
    app.include_router(base_router)
    for view in conf.views:
        view = importlib.import_module(f'{view}.views')
        app.include_router(view.router)