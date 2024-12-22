from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, StreamingResponse

from yoga_pose_recognition.detection.yoga_pose_detector import YogaPoseDetector

router = APIRouter()

yoga_pose_detector = YogaPoseDetector()


def get_yoga_pose_detector() -> YogaPoseDetector:
    return yoga_pose_detector


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
    pose: str,
    detector: YogaPoseDetector = Depends(get_yoga_pose_detector),
) -> JSONResponse:
    try:
        await detector.set_current_pose(pose)
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"message": str(e)},
        )
    return JSONResponse(
        content={"message": "Pose set successfully"},
    )
