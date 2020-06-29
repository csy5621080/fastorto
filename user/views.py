from fastapi import APIRouter as UserAPIRouter
from user.models import User
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

router = UserAPIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/users/")
async def read_users():
    return [{"username": "Foo"}, {"username": "Bar"}]


@router.get("/users/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}")
async def read_user(username: str):
    return {"username": username}
