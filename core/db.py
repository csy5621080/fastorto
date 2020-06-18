from core.config import conf
from tortoise.contrib.fastapi import register_tortoise


def init_db(app):
    register_tortoise(
        app,
        db_url=conf.db_url(),
        modules={'models': [f'{module}.models' for module in conf.modules]},
        generate_schemas=True,
        add_exception_handlers=True
    )