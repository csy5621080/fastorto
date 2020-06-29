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
    res = await Article.article_page()
    res.update({"request": request})
    return templates.TemplateResponse('index.html', res)


def router_register(app):
    app.include_router(base_router)
    for view_name in conf.views:
        view = importlib.import_module(f'{view_name}.views')
        app.include_router(view.router, prefix=f'/{view_name}')
