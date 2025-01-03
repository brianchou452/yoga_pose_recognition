import asyncio
import json

import aiofiles
from fastapi import APIRouter, Depends, WebSocket
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from yoga_pose_recognition.detection.yoga_pose_detector import YogaPoseDetector

router = APIRouter()

yoga_pose_detector = YogaPoseDetector()


def get_yoga_pose_detector() -> YogaPoseDetector:
    return yoga_pose_detector


class Pose(BaseModel):
    pose_id: str


class Background(BaseModel):
    path: str


@router.get("/frame", response_class=StreamingResponse)
async def get_frame(
    detector: YogaPoseDetector = Depends(get_yoga_pose_detector),
) -> StreamingResponse:

    return StreamingResponse(
        detector.get_frame(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@router.post("/pose")
async def post_pose(
    pose: Pose,
    detector: YogaPoseDetector = Depends(get_yoga_pose_detector),
) -> JSONResponse:
    try:
        await detector.set_current_pose(pose.pose_id)
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"message": str(e)},
        )
    return JSONResponse(
        content={"message": "Pose set successfully"},
    )


@router.websocket("/is_pose_wrong/ws")
async def recognition_websocket(
    *,
    websocket: WebSocket,
    detector: YogaPoseDetector = Depends(get_yoga_pose_detector),
) -> None:
    await websocket.accept()
    while True:
        await websocket.send_text(f"{detector.is_current_frame_wrong}")
        await asyncio.sleep(0.5)


@router.post("/background")
async def post_background(
    bg: Background,
    detector: YogaPoseDetector = Depends(get_yoga_pose_detector),
) -> JSONResponse:
    try:
        await detector.load_background_image(bg.path)
    except FileNotFoundError as e:
        return JSONResponse(
            status_code=400,
            content={"message": str(e)},
        )
    return JSONResponse(
        content={"message": "Background set successfully"},
    )


@router.get("/background")
async def get_background() -> JSONResponse:
    async with aiofiles.open("data/background.json", mode="r") as f:
        contents = await f.read()
        json_data = json.loads(contents)
        return JSONResponse(content=json_data)
