from fastapi import APIRouter as UserAPIRouter
from fastapi.encoders import jsonable_encoder
from user.auth_service import authenticate_user, get_token
from user.models import User
from fastapi.requests import Request

router = UserAPIRouter()


@router.get("/users/")
async def read_users():
    return [{"username": "Foo"}, {"username": "Bar"}]


@router.get("/users/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}")
async def read_user(username: str):
    return {"username": username}


@router.post("/login")
async def login(data: dict):
    data: dict = jsonable_encoder(data)
    res = await authenticate_user(data['username'], data['password'])
    if res:
        token = await get_token(res.user_name, res.id)
    return {'user_name': res.user_name, 'token': token}
