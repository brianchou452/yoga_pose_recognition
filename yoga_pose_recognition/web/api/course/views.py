import json

import aiofiles
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/")
async def get_frame() -> JSONResponse:
    async with aiofiles.open("data/course.json", mode="r") as f:
        contents = await f.read()
        json_data = json.loads(contents)
        return JSONResponse(content=json_data)
