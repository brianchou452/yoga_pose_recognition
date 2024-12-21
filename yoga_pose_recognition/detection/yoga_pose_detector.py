import asyncio
import threading
import time
from typing import Any, AsyncGenerator

import cv2
import mediapipe as mp
import numpy as np
from loguru import logger
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python.vision.pose_landmarker import PoseLandmarkerResult

from yoga_pose_recognition.detection.utils.camera import Camera

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


class YogaPoseDetector:
    _instance = None
    current_frame = None
    current_mask_frame = None

    def __new__(
        cls,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> "YogaPoseDetector":
        if cls._instance is None:
            cls._instance = super(YogaPoseDetector, cls).__new__(
                cls,
                *args,
                **kwargs,
            )
            logger.info("YogaPoseDetector instance created")
        return cls._instance

    def __init__(self) -> None:
        self.cam = Camera(1)
        self.options = PoseLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path="models/pose_landmarker_full.task",
                delegate=BaseOptions.Delegate.CPU,
            ),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.on_get_result,
            output_segmentation_masks=True,
        )
        self.landmarker = PoseLandmarker.create_from_options(self.options)
        self.lock = threading.Lock()

    def __del__(self) -> None:
        self.cam.release()
        if self.landmarker:
            self.landmarker.close()

    def draw_landmarks_on_image(
        self,
        rgb_image: np.ndarray,
        detection_result: PoseLandmarkerResult,
    ) -> np.ndarray:
        pose_landmarks_list = detection_result.pose_landmarks
        annotated_image = np.copy(rgb_image)
        for idx in range(len(pose_landmarks_list)):
            pose_landmarks = pose_landmarks_list[idx]
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend(
                [
                    landmark_pb2.NormalizedLandmark(
                        x=landmark.x,
                        y=landmark.y,
                        z=landmark.z,
                    )
                    for landmark in pose_landmarks
                ],
            )
            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                pose_landmarks_proto,
                solutions.pose.POSE_CONNECTIONS,
                solutions.drawing_styles.get_default_pose_landmarks_style(),
            )
        return annotated_image

    def on_get_result(
        self,
        result: PoseLandmarkerResult,
        output_image: mp.Image,
        timestamp_ms: int,
    ) -> None:
        if result.segmentation_masks is not None and len(result.segmentation_masks) > 0:
            segmentation_mask = result.segmentation_masks[0].numpy_view()
            visualized_mask = (
                np.repeat(segmentation_mask[:, :, np.newaxis], 3, axis=2) * 255
            ).astype(np.uint8)
            self.current_mask_frame = visualized_mask

            masked_frame = cv2.bitwise_and(
                output_image.numpy_view().astype(np.uint8),
                visualized_mask,
            )
            self.current_frame = self.draw_landmarks_on_image(
                masked_frame,
                result,
            )

    async def generate_frame(self) -> None:
        frame = self.cam.get_frame()
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame,
        )
        self.landmarker.detect_async(mp_image, int(time.time() * 1000))

    async def get_frame(self) -> AsyncGenerator[bytes, None]:
        try:
            while True:
                await self.generate_frame()

                if self.current_frame is None:
                    self.current_frame = self.cam.get_frame()

                success, buffer = cv2.imencode(".jpg", self.current_frame)

                if success:
                    frame_bytes = buffer.tobytes()
                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
                    )
                else:
                    logger.warning("Frame encoding failed.")

                await asyncio.sleep(0)

        except (asyncio.CancelledError, GeneratorExit):
            logger.warning("Frame generation cancelled.")
        finally:
            logger.info("Frame generator exited.")
