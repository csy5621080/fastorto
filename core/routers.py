from fastapi import APIRouter as BaseRouter
from core.config import conf
import importlib
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
templates = Jinja2Templates(directory="templates")

base_router = BaseRouter()


@base_router.get("/")
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request, "res": {'name': 'yanyan'}})


def router_register(app):
    app.include_router(base_router)
    for view in conf.views:
        view = importlib.import_module(f'{view}.views')
        app.include_router(view.router)