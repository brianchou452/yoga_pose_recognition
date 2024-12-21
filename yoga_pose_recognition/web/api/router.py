from fastapi.routing import APIRouter

from yoga_pose_recognition.web.api import video

api_router = APIRouter()
api_router.include_router(video.router, prefix="/video", tags=["video"])
