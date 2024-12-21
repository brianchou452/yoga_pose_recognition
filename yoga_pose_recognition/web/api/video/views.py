from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from yoga_pose_recognition.detection.yoga_pose_detector import YogaPoseDetector

router = APIRouter()


def get_yoga_pose_detector() -> YogaPoseDetector:
    return YogaPoseDetector()


@router.get("/frame", response_class=StreamingResponse)
async def get_frame(
    detector: YogaPoseDetector = Depends(get_yoga_pose_detector),
) -> StreamingResponse:

    return StreamingResponse(
        detector.run(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
