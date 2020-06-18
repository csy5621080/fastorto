from fastapi import APIRouter as UserAPIRouter
from user.models import User
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

router = UserAPIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/tags/")
async def read_users():
    return [{"username": "Foo"}, {"username": "Bar"}]


@router.get("/tags/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/tags/{username}", tags=["tags"])
async def read_user(request: Request, username: str):
    res = await User.filter(user_name=username).first()
    return res
