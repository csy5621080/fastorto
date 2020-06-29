from fastapi import APIRouter as TagAPIRouter
from fastapi.requests import Request

router = TagAPIRouter()


@router.get("/tags/")
async def read_users():
    return [{"username": "Foo"}, {"username": "Bar"}]


@router.get("/tags/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/tags/{username}", tags=["tags"])
async def read_user(request: Request, username: str):
    return 1
