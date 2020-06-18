from fastapi import FastAPI
from core.db import init_db
from core.routers import router_register
from fastapi.staticfiles import StaticFiles


def create_app():
    app = FastAPI()
    init_db(app)
    router_register(app)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    return app