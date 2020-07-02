from fastapi import APIRouter as TagAPIRouter
from fastapi.requests import Request
from tags.models import Tag, Serializer
from fastapi.responses import JSONResponse
router = TagAPIRouter()


@router.get("/list")
async def tags():
    all_tag = await Tag.get_all()
    return JSONResponse(all_tag)


@router.post("/create")
async def create(request: Request, data: dict):
    new = await Tag.create(**data)
    new_obj = await Serializer(new).to_dict()
    return JSONResponse(new_obj)


@router.delete("/del/{id}")
async def create(request: Request, id: int):
    del_num = await Tag.filter(id=id).delete()
    return JSONResponse(del_num)

