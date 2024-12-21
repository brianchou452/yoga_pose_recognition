from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse

from yoga_pose_recognition.detection.yoga_pose_detector import YogaPoseDetector
from yoga_pose_recognition.log import configure_logging
from yoga_pose_recognition.web.api.router import api_router

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="yoga_pose_recognition",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost", "http://localhost:8888"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # Adds static directory.
    # This directory is used to access swagger files.
    # app.mount("/static", StaticFiles(directory=APP_ROOT / "static"), name="static")

    # Initialize YogaPoseDetector
    app.state.detector = YogaPoseDetector()

    return app
